import socket
import struct
import numpy as np
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

"""Параметры DH"""
DH_PARAMS = [
    (0, 0.21, np.pi / 2),
    (-0.8, 0.193, 0),
    (-0.598, -0.16, 0),
    (0, 0.25, np.pi / 2),
    (0, 0.25, -np.pi / 2),
    (0, 0.25, 0)
]


@dataclass
class KinematicData:
    timestamp: int
    thetas: list


def send_message(message: str, server_address: tuple):
    list_data = []
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), server_address)
        for _ in range(5):
            data = receive_data(sock)
            list_data.append(data)
    return list_data


def receive_data(sock):
    data, _ = sock.recvfrom(1024)
    return data


def calculate_forward_kinematics(thetas):
    T = np.eye(4)
    for i, (a, d, alpha) in enumerate(DH_PARAMS):
        theta = np.radians(thetas[i])
        T_i = np.array([
            [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
            [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]
        ])
        T = T @ T_i
    return T[0:3, 3]  # Возвращаем позицию (x, y, z)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kinematics Result")
        self.tree = ttk.Treeview(self, columns=("Timestamp", "Position"), show='headings')
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Position", text="Position (x, y, z)")
        self.tree.column("Timestamp", width=50, anchor='center')
        self.tree.column("Position", width=250, anchor='center')

    def insert_data(self, timestamp, position):
        self.tree.insert("", "end", values=(timestamp, position))
        self.tree.pack(expand=True, fill='both')


def main():
    """GUI"""
    gui = GUI()

    server_address = ('localhost', 8088)
    list_data = send_message("get", server_address)

    for data in list_data:
        timestamp, *thetas = struct.unpack('>Q6d', data)
        kinematic_data = KinematicData(timestamp, thetas)
        position = calculate_forward_kinematics(kinematic_data.thetas)
        gui.insert_data(kinematic_data.timestamp, position)

    gui.mainloop()


if __name__ == "__main__":
    main()
