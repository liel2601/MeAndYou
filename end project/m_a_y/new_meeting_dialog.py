import socket
import encryption
import main_page
import magic_strings
from Crypto.PublicKey import RSA
from PyQt5 import QtCore, QtGui, QtWidgets
import meeting_window

NO_ID = "NO ID ENTERED"
NO_ID_ERROR = "PLEASE ENTER A MEETING ID"
NO_PASSWORD = "NO PASSWORD ENTERD"
NO_PASSWORD_ERROR = "PLEASE ENTER A PASSWORD"
IP = magic_strings.IP
INFO_PORT = magic_strings.INFO_PORT
CREATE_MEETING = "CREATE_MEETING"
CONFIRM = "YES"
UNCONFIRMED = "NO!"
FAIL = "NEW MEETING ERROR"
FAIL_MSG = "COULDN'T OPEN A NEW MEETING, TRY AGAIN LATER"
TAKEN = "TAKEN"
TAKEN_ERROR = "TAKEN MEETING NAME"
TAKEN_ERROR_MSG = "PLEASE ENTER A DIFFERENT MEETING NAME"
WELCOME_MSG1 = "HELLO "
WELCOME_MSG2 = ", NICE TO SEE YOU :)"
aes_key = None
aes_iv = None


#מפתח אחד מצפין את ההודעה והמפתח השני פותח את ההודעה
#שוב- רק מפתח אחד יכול להצפין ורק מפתח אחד יכול לפתוח
#ה Public Key מצפין את המידע ואילו ה Private Key פותח את המידע

def get_keys():
    global aes_iv, aes_key
    return aes_key, aes_iv


class Ui_new_meeting_dialog(object):

# פותחת את העמוד הראשי וסוגרת את הדיאלוג

    def show_main_page(self, win):
        """the function opens the main page and closes the current settings page"""
        self.window = QtWidgets.QMainWindow()
        self.ui = main_page.Ui_MainPage()
        self.ui.setupUi(self.window)
        self.ui.username.setText(self.username.text())
        self.ui.welcome_msg.setText(WELCOME_MSG1 + self.username.text().upper() + WELCOME_MSG2)
        self.window.show()
        win.close()

# מציג הודעות טקסט שהועברו

    def message(self, title, msg):
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle(title)
        mb.setText(msg)
        mb.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mb.exec_()

        #פתיחת פגישה חדשה
    def open_new_meeting(self, dialog):
        print("open")
        meet_id = self.id.text()
        meet_pass = self.password.text()
        if not meet_id:
            self.message(NO_ID, NO_ID_ERROR)
        elif not meet_pass:
            self.message(NO_PASSWORD, NO_PASSWORD_ERROR)
        else:
            try:
                global aes_key
                aes_key = b"MEANDYOUPROJ:)__"
                global aes_iv
                aes_iv = b"YAY!!!!!!!!!!!!!"
                info_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                info_socket.connect((IP, INFO_PORT))
                print("open the window of the dialog")
                size = int.from_bytes(info_socket.recv(4), "big")
                rsa_key = info_socket.recv(size)

                rsa_key = RSA.import_key(rsa_key)
                print(rsa_key)
                keys = encryption.rsa_encryption(rsa_key, aes_key + b"/" + aes_iv)
                info_socket.send(len(keys).to_bytes(4, "big") + keys)
                print("sent")
                msg = CREATE_MEETING + "/" + meet_id + "/" + meet_pass
                msg = encryption.do_encrypt(aes_key, aes_iv, msg.encode())
                info_socket.send(len(msg).to_bytes(4, "big") + msg)
                size = int.from_bytes(info_socket.recv(4), "big")
                data = info_socket.recv(size)
                data = encryption.do_decrypt(aes_key, aes_iv, data).decode()
                print(data)
                if data == UNCONFIRMED:
                    self.message(FAIL, FAIL_MSG)
                elif data == TAKEN:
                    self.message(TAKEN_ERROR, TAKEN_ERROR_MSG)
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

# מגדירה את ממשק המשתמש עבור יצירת דיאלוג לפגישה חדשה

    def setupUi(self, new_meeting_dialog):
        new_meeting_dialog.setObjectName("new_meeting_dialog")
        new_meeting_dialog.resize(640, 403)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pics/official_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        new_meeting_dialog.setWindowIcon(icon)
        new_meeting_dialog.setStyleSheet("background-color: rgb(66, 186, 240);")
        self.msg = QtWidgets.QLabel(new_meeting_dialog)
        new_meeting_dialog.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint)
        self.msg.setGeometry(QtCore.QRect(20, 40, 591, 71))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.msg.setFont(font)
        self.msg.setStyleSheet("color: rgb(255, 255, 255);")
        self.msg.setObjectName("msg")
        self.username = QtWidgets.QLabel(new_meeting_dialog)
        self.username.setGeometry(QtCore.QRect(20, 20, 150, 22))
        self.username.setFont(font)
        self.username.setStyleSheet("color: rgb(255, 255, 255);")
        self.username.setObjectName("username")
        self.id = QtWidgets.QLineEdit(new_meeting_dialog)
        self.id.setGeometry(QtCore.QRect(20, 140, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        self.id.setFont(font)
        self.id.setStyleSheet("border-color: rgb(0, 0, 0);\n" "color: rgb(255, 255, 255);")
        self.id.setFrame(True)
        self.id.setClearButtonEnabled(False)
        self.id.setObjectName("id")
        self.password = QtWidgets.QLineEdit(new_meeting_dialog)
        self.password.setGeometry(QtCore.QRect(20, 220, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(11)
        self.password.setFont(font)
        self.password.setStyleSheet("color: rgb(255, 255, 255);")
        self.password.setObjectName("password")
        self.id_label = QtWidgets.QLabel(new_meeting_dialog)
        self.id_label.setGeometry(QtCore.QRect(22, 120, 68, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setBold(True)
        font.setWeight(75)
        self.id_label.setFont(font)
        self.id_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.id_label.setObjectName("id_label")
        self.password_label = QtWidgets.QLabel(new_meeting_dialog)
        self.password_label.setGeometry(QtCore.QRect(22, 200, 101, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.password_label.setObjectName("password_label")
        self.ok_btn = QtWidgets.QPushButton(new_meeting_dialog)
        self.ok_btn.setGeometry(QtCore.QRect(502, 337, 101, 41))
        self.ok_btn.setStyleSheet("color: rgb(81, 139, 141);\n" "background-color: rgb(255, 255, 255);")
        self.ok_btn.setAutoDefault(True)
        self.ok_btn.setDefault(False)
        self.ok_btn.setFlat(False)
        self.ok_btn.setObjectName("ok_btn")
        self.ok_btn.clicked.connect(lambda checked: self.open_new_meeting(new_meeting_dialog))
        self.back_to_home_btn = QtWidgets.QPushButton(new_meeting_dialog)
        self.back_to_home_btn.setGeometry(QtCore.QRect(530, 20, 111, 28))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.back_to_home_btn.setFont(font)
        self.back_to_home_btn.setStyleSheet("color: rgb(255, 255, 255);")
        self.back_to_home_btn.setFlat(True)
        self.back_to_home_btn.setObjectName("back_to_home_btn")
        self.back_to_home_btn.clicked.connect(lambda checked: self.show_main_page(new_meeting_dialog))
        self.retranslateUi(new_meeting_dialog)
        QtCore.QMetaObject.connectSlotsByName(new_meeting_dialog)

    # מגדיר את הטקסטים בשפה הרצויה

    def retranslateUi(self, new_meeting_dialog):
        _translate = QtCore.QCoreApplication.translate
        new_meeting_dialog.setWindowTitle(_translate("new_meeting_dialog", "NEW MEETING"))
        self.msg.setText(_translate("new_meeting_dialog", "HI! PLEASE CHOOSE AN ID AND PASSWORD FOR YOUR\n""NEW MEETING :)"))
        self.username.setText(_translate("new_meeting_dialog", "username"))
        self.id_label.setText(_translate("new_meeting_dialog", "ID:"))
        self.password_label.setText(_translate("new_meeting_dialog", "PASSWORD:"))
        self.ok_btn.setText(_translate("new_meeting_dialog", "OK"))
        self.back_to_home_btn.setText(_translate("new_meeting_dialog", "HOME →"))

#פה התוכנית מתחילה לרוץ

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    new_meeting_dialog = QtWidgets.QDialog()
    ui = Ui_new_meeting_dialog()
    ui.setupUi(new_meeting_dialog)
    new_meeting_dialog.show()
    sys.exit(app.exec_())