from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import socket
import time
import sys


def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = list(map(float, vector[first + 1:second].split(",")))
            return result
    return ""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 671)
        MainWindow.setMinimumSize(QtCore.QSize(420, 671))
        MainWindow.setMaximumSize(QtCore.QSize(420, 671))
        MainWindow.setWindowIcon(QtGui.QIcon("files/icon.ico"))

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 421, 81))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 180, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 270, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 360, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.ip_row = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.ip_row.setGeometry(QtCore.QRect(70, 210, 301, 31))
        self.ip_row.setObjectName("ip_row")

        self.name_row = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.name_row.setGeometry(QtCore.QRect(70, 300, 301, 31))
        self.name_row.setObjectName("name_row")

        self.pass_row = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.pass_row.setGeometry(QtCore.QRect(70, 390, 301, 31))
        self.pass_row.setObjectName("pass_row")

        self.enter_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.enter_button.setGeometry(QtCore.QRect(110, 510, 221, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.enter_button.setFont(font)
        self.enter_button.setObjectName("enter_button")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Вход в игру"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:26pt; color:#ffffff;\">Вход в "
                                      "игру</span></p><p><br/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "IP-адрес"))
        self.label_3.setText(_translate("MainWindow", "Никнейм"))
        self.label_4.setText(_translate("MainWindow", "Пароль"))
        self.enter_button.setText(_translate("MainWindow", "Вход"))


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.name = None
        self.pasw = None
        self.ip = None
        self.port = None
        self.setupUi(self)
        self.enter_button.clicked.connect(self.connect_to_serv)

    def ip_check(self):
        row = self.ip_row.text()
        self.ip, self.port = row.split(":")
        self.ip = self.ip.split(".")
        if not (self.port.isnumeric() and int(self.port) in range(1024, 65536)):
            return False
        for byte in self.ip:
            if not (byte.isnumeric() and int(byte) in range(0, 256)):
                return False
        return True

    def empty_check(self):
        self.name = self.name_row.text()
        self.pasw = self.pass_row.text()
        result = [None, None]
        if self.name == "":
            result[0] = False
        else:
            result[0] = True
        if self.pasw == "":
            result[1] = False
        else:
            result[1] = True
        return tuple(result)

    def connect_to_serv(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        empty = self.empty_check()
        if not all(empty):
            print("Поля пустые")
            return
        if not self.ip_check():
            print("Неправильный IP или порт")
            return
        self.ip = '.'.join(self.ip)
        self.port = int(self.port)
        try:
            sock.connect((self.ip, self.port))
            info = f"<{self.name},{self.pasw}>".encode()
            sock.send(info)
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return


stylesheet = """
QMainWindow {
    background-image: url('back.jpg');
    background-repeat: no-repeat;
    background-position: center;
}
"""


def application():
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    application()
