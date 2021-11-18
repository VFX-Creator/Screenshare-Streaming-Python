import time
import socket
import os
from PyQt6 import QtCore, QtGui, QtWidgets
import random
import cv2
import pyautogui
import numpy as np

class Recver_Thread(QtCore.QThread):

    frame_changed = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def recv_msg(self):
        msg_length = self.client_socket.recv(64).decode()
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client_socket.recv(msg_length).decode()

            return msg

    def recv_file(self, file_name):
        counter_position = int(self.recv_msg())
        with open(file_name, "wb") as f:
            bytes_recv = self.client_socket.recv(1024)
            counter = 0
            while True:
                counter += 1
                f.write(bytes_recv)
                if counter == counter_position:
                    break
                bytes_recv = self.client_socket.recv(1024)

    def run(self):

        while True:
            self.client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.client_socket.connect((ui.HOST_RECVER, ui.PORT_RECVER))
            rand_int = random.randint(1000, 9999)
            self.recv_file(f"frame_Client_Recver_{rand_int}.jpg")
            pixmap = QtGui.QPixmap(f"frame_Client_Recver_{rand_int}.jpg")
            ui.pixmap_resized = pixmap.scaled(ui.label.width(), ui.label.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.frame_changed.emit('%s' % (f"frame_Client_Recver_{rand_int}.jpg"))
            time.sleep(0.001)

class Sender_Thread(QtCore.QThread):

    frame_changed = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def send_file(self, filename):
        msg = str(-(-int(os.path.getsize(filename)) // 1024))
        message = msg.encode()
        msg_length = len(message)
        send_length = str(msg_length).encode()
        send_length += b" " * (64 - len(send_length))
        self.client_socket.send(send_length)
        self.client_socket.send(message)
        counter = 0
        with open(filename, "rb") as f:
            while True:
                counter += 1
                file_bytes = f.read(1024)
                if not file_bytes:
                    break
                self.client_socket.sendall(file_bytes)

    def run(self):

        while True:
            self.client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.client_socket.connect((ui.HOST_SENDER, ui.PORT_SENDER))
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            rand_int = random.randint(1000, 9999)
            cv2.imwrite(f"frame_Client_Sender_{rand_int}.jpg", image)
            try:
                self.send_file(f"frame_Client_Sender_{rand_int}.jpg")
            except:
                pass
            os.remove(f"frame_Client_Sender_{rand_int}.jpg")
            #self.frame_changed.emit('%s' % ("0"))
            time.sleep(0.001)

class Ui_Form(QtWidgets.QWidget):
    def __init__(self, host_recver, port_recver, host_sender, port_sender):
        super().__init__()
        self.setObjectName("Form")
        self.resize(800, 400)
        self.setMinimumSize(800, 400)
        self.setWindowTitle("RECEVING VIDEO")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.HOST_RECVER = host_recver
        self.PORT_RECVER = port_recver

        self.HOST_SENDER = host_sender
        self.PORT_SENDER = port_sender

    def show_frame(self, data):
        self.label.setPixmap(self.pixmap_resized)
        os.remove(data)

    def send_frame(self):
        pass

    def start_recver(self):

        self.recver = Recver_Thread()
        self.recver.frame_changed.connect(self.show_frame)
        self.recver.start()

    def start_sender(self):
        self.sender = Sender_Thread()
        self.sender.frame_changed.connect(self.send_frame)
        self.sender.start()

    def closeEvent(self, event):
        print("[CLIENT] stopped")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Form("::1", 54537, "::1", 54536) #::1
    ui.show()
    ui.start_recver()
    ui.start_sender()
    sys.exit(app.exec())
