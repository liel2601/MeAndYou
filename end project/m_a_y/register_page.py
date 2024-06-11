import binascii
import hashlib
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QLineEdit

import login

TAKEN = "TAKEN"
TAKEN_USERNAME_ERROR = "TAKEN"
NO_USERNAME = "USERNAME ERROR"
NO_USERNAME_MSG = "PLEASE ENTER A USERNAME"
NO_NAME = "NAME ERROR"
REGISTER_PORT = 2121
LOGIN_PORT = 7474
IP = "127.0.0.1"
NO_NAME_MSG = "PLEASE ENTER A NAME"
NO_LAST_NAME = "LAST NAME ERROR"
NO_LAST_NAME_MSG = "PLEASE ENTER A LAST NAME"
NO_PASSWORD = "PASSWORD ERROR"
NO_PASSWORD_MSG = "PLEASE ENTER A PASSWORD"
NO_CONFIRM = "PLEASE CONFIRM THE PASSWORD"
NO_CONFIRM_ERROR = "OOPS"
PASSWORDS_DONT_MATCH = "OOPPS!"
PASSWORDS_DONT_MATCH_MSG = "PLEASE ENTER CONFIRM PASSWORD AGAIN"
TAKEN_USERNAME_MSG = "PLEASE ENTER A DIFFERENT USERNAME BECAUSE THIS ONE IS TAKEN ALREADY"
REGISTERED = "YAY!"
REGISTERED_MSG = "YOU HAVE SUCCESSFULLY REGISTERED"
REGISTER = "REGISTER"
CONNECTED = "CONNECTED"
TOO_LONG = "OOPS! USERNAME TOO LONG"
TOO_LONG_MSG = "PLEASE ENTER A SHORTER USERNAME"

#מציג את תיבת ההודעה

def message(title, msg):
    # present a message with information for the user
    mb = QtWidgets.QMessageBox()
    mb.setWindowTitle(title)
    mb.setText(msg)
    mb.setStandardButtons(QtWidgets.QMessageBox.Ok)
    mb.setIcon(QtWidgets.QMessageBox.Information)
    mb.exec_()

# פותחת את מסך ההתחברות

def to_login():
    # opens login screen
    window = QtWidgets.QMainWindow()
    ui = login.Ui_login()
    ui.setupUi(window)
    window.show()

# מצפינה את הסיסמא לצורך שמירה בבסיס הנתונים

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

#רושמת משתמש חדש במערכת

def register(username, first_name, last_name, password, confirm_password):
    if len(username) == 0:
        message(NO_USERNAME, NO_USERNAME_MSG)
    elif len(username) > 16:
        message(TOO_LONG, TOO_LONG_MSG)
    elif len(first_name) == 0:
        message(NO_NAME, NO_NAME_MSG)
    elif len(last_name) == 0:
        message(NO_LAST_NAME, NO_LAST_NAME_MSG)
    elif len(password) == 0:
        message(NO_PASSWORD, NO_PASSWORD_MSG)
    elif len(confirm_password) == 0:
        message(NO_CONFIRM_ERROR, NO_CONFIRM)
    elif confirm_password == password:

        conn = sqlite3.connect('UsersForm.db')
        with conn:
            cursor = conn.cursor()

        query = "SELECT * FROM users WHERE Username = ?"
        cursor.execute(query, [username])

        if len(cursor.fetchall()) > 0:
            message(TAKEN_USERNAME_ERROR, TAKEN_USERNAME_MSG)
        else :
            password = hash_password(password)
            cursor.execute('INSERT INTO users (Username,Fname,Lname,Password) VALUES(?,?,?,?)',
                       (username, first_name, last_name, password,))
            conn.commit()
            cursor.execute("SELECT * FROM users")
            message(REGISTERED, REGISTERED_MSG)



class Ui_MainWindow(object):

# מגדיר את המשתמש הראשי של חלון הרישום

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(896, 650)
        MainWindow.setStyleSheet("background-color: rgb(180,210,170);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./pics/new_logom1.PNG"),QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.welcome_image = QtWidgets.QLabel(self.centralwidget)
        self.welcome_image.setGeometry(QtCore.QRect(0, -10, 441, 751))
        self.welcome_image.setMinimumSize(QtCore.QSize(0, 751))
        self.welcome_image.setMaximumSize(QtCore.QSize(16777215, 751))
        self.welcome_image.setAutoFillBackground(False)
        self.welcome_image.setText("")
        self.welcome_image.setPixmap(QtGui.QPixmap("./pics/welcome.png"))
        self.welcome_image.setScaledContents(True)
        self.welcome_image.setObjectName("welcome_image")
        self.create_account = QtWidgets.QLabel(self.centralwidget)
        self.create_account.setGeometry(QtCore.QRect(541, 63, 271, 71))
        self.create_account.setStyleSheet("color: rgb(81, 139, 141);\n"
                                          "font: 75 18pt \"Century Gothic\";")
        self.create_account.setObjectName("create_account")
        self.its_free = QtWidgets.QLabel(self.centralwidget)
        self.its_free.setGeometry(QtCore.QRect(585, 125, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.its_free.setFont(font)
        self.its_free.setStyleSheet("color: rgb(81, 139, 141);")
        self.its_free.setObjectName("its_free")
        self.first_name = QtWidgets.QTextEdit(self.centralwidget)
        self.first_name.setGeometry(QtCore.QRect(541, 193, 270, 30))
        self.first_name.setStyleSheet("QTextEdit {\n"
                                      "    border: 1px solid rgb(81, 139, 141);\n"
                                      "}")
        self.first_name.setObjectName("first_name")
        self.last_name = QtWidgets.QTextEdit(self.centralwidget)
        self.last_name.setGeometry(QtCore.QRect(541, 251, 270, 30))
        self.last_name.setStyleSheet("QTextEdit {\n"
                                     "    border: 1px solid rgb(81, 139, 141);\n"
                                     "}")
        self.last_name.setObjectName("last_name")
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(541, 309, 270, 30))
        self.username.setStyleSheet("QLineEdit {\n"
                                    "    border: 1px solid rgb(81, 139, 141);\n"
                                    "}")
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(541, 367, 270, 30))
        self.password.setStyleSheet("QLineEdit {\n"
                                    "    border: 1px solid rgb(81, 139, 141);\n"
                                    "}")
        self.password.setObjectName("password")
        self.password.setEchoMode(QLineEdit.Password)
        self.confirmpassword = QtWidgets.QLineEdit(self.centralwidget)
        self.confirmpassword.setGeometry(QtCore.QRect(541, 425, 270, 30))
        self.confirmpassword.setStyleSheet("QLineEdit {\n"
                                           "    border: 1px solid rgb(81, 139, 141);\n"
                                           "}")
        self.confirmpassword.setObjectName("confirmpassword")
        self.confirmpassword.setEchoMode(QLineEdit.Password)
        self.fullname_text = QtWidgets.QLabel(self.centralwidget)
        self.fullname_text.setGeometry(QtCore.QRect(541, 172, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.fullname_text.setFont(font)
        self.fullname_text.setStyleSheet("color: rgb(81, 139, 141);")
        self.fullname_text.setObjectName("fullname_text")
        self.username_text = QtWidgets.QLabel(self.centralwidget)
        self.username_text.setGeometry(QtCore.QRect(540, 232, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.username_text.setFont(font)
        self.username_text.setStyleSheet("color: rgb(81, 139, 141);")
        self.username_text.setObjectName("username_text")
        self.email_text = QtWidgets.QLabel(self.centralwidget)
        self.email_text.setGeometry(QtCore.QRect(541, 290, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.email_text.setFont(font)
        self.email_text.setStyleSheet("color: rgb(81, 139, 141);")
        self.email_text.setObjectName("email_text")
        self.password_text = QtWidgets.QLabel(self.centralwidget)
        self.password_text.setGeometry(QtCore.QRect(541, 350, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.password_text.setFont(font)
        self.password_text.setStyleSheet("color: rgb(81, 139, 141);")
        self.password_text.setObjectName("password_text")
        self.confirm_text = QtWidgets.QLabel(self.centralwidget)
        self.confirm_text.setGeometry(QtCore.QRect(540, 405, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.confirm_text.setFont(font)
        self.confirm_text.setStyleSheet("color: rgb(81, 139, 141);")
        self.confirm_text.setObjectName("confirm_text")
        self.register_btn = QtWidgets.QPushButton(self.centralwidget)
        self.register_btn.setGeometry(QtCore.QRect(540, 490, 270, 30))
        self.register_btn.clicked.connect(lambda checked: register(self.username.text(), self.first_name.toPlainText(),
                                                                   self.last_name.toPlainText(), self.password.text(),
                                                                   self.confirmpassword.text()))
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.register_btn.setDefault(True)
        self.register_btn.setFlat(False)
        self.register_btn.setObjectName("register_btn")
        self.back_to_login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_to_login_btn.setGeometry(QtCore.QRect(540, 540, 270, 30))
        self.register_btn.setFont(font)
        self.register_btn.setStyleSheet("background-color: rgb(81, 139, 141);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border: 3px white;")
        self.register_btn.setAutoDefault(True)
        self.back_to_login_btn.clicked.connect(to_login)
        self.back_to_login_btn.clicked.connect(MainWindow.close)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.back_to_login_btn.setFont(font)
        self.back_to_login_btn.setStyleSheet("background-color: rgb(81, 139, 141);\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "border: 3px white;")
        self.back_to_login_btn.setAutoDefault(True)
        self.back_to_login_btn.setDefault(True)
        self.back_to_login_btn.setFlat(False)
        self.back_to_login_btn.setObjectName("back_to_login_btn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#  מגדיר את הטקסטים בשפה הרצויה

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "REGISTER"))
        self.create_account.setText(_translate("MainWindow", "CREATE ACCOUNT"))
        self.its_free.setText(_translate("MainWindow", "IT\'S COMPLETELY FREE"))
        self.fullname_text.setText(_translate("MainWindow", "FIRST NAME:"))
        self.username_text.setText(_translate("MainWindow", "LAST NAME:"))
        self.email_text.setText(_translate("MainWindow", "USERNAME:"))
        self.password_text.setText(_translate("MainWindow", "PASSWORD:"))
        self.confirm_text.setText(_translate("MainWindow", "COMFIRM PASSWORD"))
        self.register_btn.setText(_translate("MainWindow", "REGISTER"))
        self.back_to_login_btn.setText(_translate("MainWindow", "GO TO LOG IN "))


