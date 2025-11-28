import time
import socket

def find(info: str):
    first = None
    for num, sign in enumerate(info):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = info[first + 1:second].split(",")
            return result
    return ""

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(("192.168.0.194", 15000))
main_socket.setblocking(False)
main_socket.listen(5)
print("Сокет создан")

players = []

server_works = True
while server_works:
    try:
        new_sock, addr = main_socket.accept()
        print("Подключен", addr)
        new_sock.setblocking(False)
        players.append(new_sock)
    except BlockingIOError:
        pass
    for sock in players:
        try:
            data = sock.recv(1024).decode()
            data = find(data)
            print("Получил", data)
        except:
            pass
    time.sleep(1)