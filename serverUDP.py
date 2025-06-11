import socket
import struct
import time

# Константы
PORT = 8088
BUFFER_SIZE = 1024


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', PORT))
    print(f"Сервер запущен на порту {PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode()

            if message == "get":
                print("Получено сообщение 'get' от клиента.")
                for i in range(5):
                    timestamp = i + 1
                    thetas = [30.0 * (i + 1), 45.0 * (i + 1), 60.0 * (i + 1),
                              90.0 * (i + 1), 120.0 * (i + 1), 150.0 * (i + 1)]

                    message_data = struct.pack('>Q6d', timestamp, *thetas)

                    sock.sendto(message_data, addr)
                    print(f"Отправлено: timestamp={timestamp}, thetas={thetas}")
                    time.sleep(1)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
