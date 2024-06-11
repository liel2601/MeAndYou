import socket
from Crypto.PublicKey import RSA
import main_page
import encryption
import meeting_window
import magic_strings
from PyQt5 import QtCore, QtGui, QtWidgets

NO_ID = "NO ID ENTERED"
NO_ID_ERROR = "PLEASE ENTER A MEETING ID"
NO_PASSWORD = "NO PASSWORD ENTERED"
NO_PASSWORD_ERROR = "PLEASE ENTER THE MEETING PASSWORD"
IP = magic_strings.IP
INFO_PORT = magic_strings.INFO_PORT
JOIN_MEETING = "JOIN_MEETING"
CONFIRM = "YES"
UNCONFIRMED = "NO!"
FAIL = "NEW MEETING ERROR"
FAIL_MSG = "COULDN'T OPEN A NEW MEETING, TRY AGAIN LATER"
LOCKED_TITLE = "MEETING IS LOCKED"
LOCKED_MSG = "SORRY, THIS MEETING IS LOCKED"
WRONG_TITLE = "WRONG MEETING DETAILS"
WRONG_MSG = "PLEASE ENTER MEETING DETAILS AGAIN :)"
LOCKED = "LOCKED"
WRONG = "WRONG"
WELCOME_MSG1 = "HELLO "
WELCOME_MSG2 = ", NICE TO SEE YOU :)"
aes_key = None
aes_iv = None


def get_keys():
    global aes_iv, aes_key
    return aes_key, aes_iv


class Ui_Dialog(object):

    def show_main_page(self, win):
        """the function opens the main_page and closes the join_meeting"""
        self.window = QtWidgets.QMainWindow()
        self.ui = main_page.Ui_MainPage()
        self.ui.setupUi(self.window)
        self.ui.username.setText(self.username.text())
        self.ui.welcome_msg.setText(WELCOME_MSG1 + self.username.text().upper() + WELCOME_MSG2)
        self.window.show()
        win.close()

    def message(self, title, msg):
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle(title)
        mb.setText(msg)
        mb.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mb.exec_()

    def open_meeting(self, dialog):
        meet_id = self.id.text()
        meet_pass = self.password.text()
        if not meet_id:
            self.message(NO_ID, NO_ID_ERROR)
        elif not meet_pass:
            self.message(NO_PASSWORD, NO_PASSWORD_ERROR)
        else:
            try:
                info_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                info_socket.connect((IP, INFO_PORT))
                global aes_key
                aes_key = b"MEANDYOUPROJ:)__"
                global aes_iv
                aes_iv = b"YAY!!!!!!!!!!!!!"
                print("yaya")
                size = int.from_bytes(info_socket.recv(4), "big")
                rsa_key = info_socket.recv(size)
                print(rsa_key)
                rsa_key = RSA.import_key(rsa_key)
                print(rsa_key)
                keys = encryption.rsa_encryption(rsa_key, aes_key + b"/" + aes_iv)
                info_socket.send(len(keys).to_bytes(4, "big") + keys)
                print("sent")
                msg = JOIN_MEETING + "/" + meet_id + "/" + meet_pass
                msg = encryption.do_encrypt(aes_key, aes_iv, msg.encode())
                info_socket.send(len(msg).to_bytes(4, "big") + msg)
                size = int.from_bytes(info_socket.recv(4), "big")
                data = info_socket.recv(size)
                data = encryption.do_decrypt(aes_key, aes_iv, data).decode()
                print(data)
                if data == UNCONFIRMED:
                    self.message(FAIL, FAIL_MSG)
                elif data == LOCKED:
                    self.message(LOCKED_TITLE, LOCKED_MSG)
                elif data == WRONG:
                    self.message(WRONG_TITLE, WRONG_MSG)
                elif data == CONFIRM:
                    self.window = QtWidgets.QMainWindow()
                    self.ui = meeting_window.Ui_meeting_window()
                    self.ui.setupUi(self.window)
                    self.ui.username.setText(self.username.text().upper())
                    self.ui.meeting_id.setText(self.ui.meeting_id.text() + " " + meet_id)
                    self.ui.meeting_password.setText(self.ui.meeting_password.text() + " " + meet_pass)
                    self.window.show()
                    info_socket.close()
                    dialog.close()
            except ConnectionAbortedError:
                pass
            except ConnectionResetError:
                pass

# פונצקיה שמגדירה את חלון הדיאלוג ע"י הגדרות עיצוב ולחצנים

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog") #שם האובייקט
        Dialog.resize(640, 386)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pics/official_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("background-color: rgb(66, 186, 240);")
        Dialog.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint)
        self.msg = QtWidgets.QLabel(Dialog)
        self.msg.setGeometry(QtCore.QRect(38, 33, 591, 71))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.msg.setFont(font)
        self.msg.setStyleSheet("color: rgb(255, 255, 255);")
        self.msg.setObjectName("msg")
        self.username = QtWidgets.QLabel(Dialog)
        self.username.setGeometry(QtCore.QRect(20, 20, 150, 22))
        self.username.setFont(font)
        self.username.setStyleSheet("color: rgb(255, 255, 255);")
        self.username.setObjectName("username")
        self.id = QtWidgets.QLineEdit(Dialog)
        self.id.setGeometry(QtCore.QRect(38, 133, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        self.id.setFont(font)
        self.id.setStyleSheet("border-color: rgb(0, 0, 0);\n"
                              "color: rgb(255, 255, 255);")
        self.id.setFrame(True)
        self.id.setClearButtonEnabled(False)
        self.id.setObjectName("id")
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(38, 213, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        self.password.setFont(font)
        self.password.setStyleSheet("color: rgb(255, 255, 255);")
        self.password.setObjectName("password")
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setGeometry(QtCore.QRect(40, 193, 101, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.password_label.setObjectName("password_label")
        self.id_label = QtWidgets.QLabel(Dialog)
        self.id_label.setGeometry(QtCore.QRect(40, 113, 68, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setBold(True)
        font.setWeight(75)
        self.id_label.setFont(font)
        self.id_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.id_label.setObjectName("id_label")
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        self.ok_btn.setGeometry(QtCore.QRect(520, 330, 101, 41))
        self.ok_btn.setStyleSheet("color: rgb(81, 139, 141);\n"
                                  "background-color: rgb(255, 255, 255);")
        self.ok_btn.setAutoDefault(True)
        self.ok_btn.setDefault(False)
        self.ok_btn.setFlat(False)
        self.ok_btn.setObjectName("ok_btn")
        self.ok_btn.clicked.connect(lambda checked: self.open_meeting(Dialog))
        self.back_to_home_btn = QtWidgets.QPushButton(Dialog)
        self.back_to_home_btn.setGeometry(QtCore.QRect(530, 20, 111, 28))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.back_to_home_btn.setFont(font)
        self.back_to_home_btn.setStyleSheet("color: rgb(255, 255, 255);")
        self.back_to_home_btn.setFlat(True)
        self.back_to_home_btn.setObjectName("back_to_home_btn")
        self.back_to_home_btn.clicked.connect(lambda checked: self.show_main_page(Dialog))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

# משמשת להגדרת טקסטים בדיאלוג

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "JOIN A MEETING"))
        self.msg.setText(_translate("Dialog", "HI! PLEASE CHOOSE AN ID AND PASSWORD FOR THE\n"
                                              "MEETING YOU WANNA JOIN:)"))
        self.username.setText(_translate("new_meeting_dialog", "username"))
        self.password_label.setText(_translate("Dialog", "PASSWORD:"))
        self.id_label.setText(_translate("Dialog", "ID:"))
        self.ok_btn.setText(_translate("Dialog", "JOIN"))
        self.back_to_home_btn.setText(_translate("Dialog", "HOME →"))


