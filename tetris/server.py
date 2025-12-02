import time
import socket
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
s = Session()


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "gamers"
    name = Column(String, primary_key=True)
    password = Column(String(30))
    score = Column(Integer, default=0)

    def __init__(self, name, password):
        self.name = name
        self.password = password


Base.metadata.create_all(bind=engine)

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
            if data:
                player = Player(data[0], data[1])
                s.add(player)
                s.commit()
                sock.send("<0>".encode())
        except IntegrityError:
            s.rollback()
            player = s.get(Player, data[0])
            if data[1] == player.password:
                print("Вход в игру выполнен")
                sock.send(f"<{player.score}>".encode())
            else:
                print("Неверный пароль")
                sock.send("<-1>".encode())
                break
    time.sleep(1)