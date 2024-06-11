import binascii  #קשור הצפנה
import hashlib      #קשור להצפנה
import os          #קשור להרצת פקודות במערכת הפעלה , שייך גם להצפנה
import login
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit

import main_page
import sqlite3

NO_NEW_NAME_ERROR = "PLEASE ENTER A USERNAME"
NEW_NAME = "NEW USERNAME"
USERNAME_TAKEN = "USERNAME TAKEN"
USERNAME_TAKEN_ERROR = "USERNAME IS ALREADY TAKEN, PLEASE TRY ANOTHER ONE"
WRONG_PASSWORD = "THE CURRENT PASSWORD IS WRONG"
WRONG_PASSWORD_MSG = "PLEASE ENTER THE CURRENT PASSWORD AGAIN"
NOT_CONFIRMED = "PASSWORDS DON'T MATCH"
NOT_CONFIRMED_MSG = "PLEASE ENTER CONFIRM PASSWORD AGAIN"
CHANGED = "YAY!"
CHANGED_NAME_MAG = "WE HAVE SUCCESSFULLY CHANGED YOUR USERNAME"
CHANGED_PASSWORD_MAG = "WE HAVE SUCCESSFULLY CHANGED YOUR PASSWORD"
NO_CURRENT = "PLEASE ENTER YOUR CURRENT PASSWORD"
NO_NEW_PASSWORD = "PLEASE ENTER NEW PASSWORD"
NOT_CONFIRM_PASSWORD = "PLEASE CONFIRM THE PASSWORD"
OOPS = "OOPS!"
WELCOME_MSG1 = "HELLO "
WELCOME_MSG2 = ", NICE TO SEE YOU :)"

#יוצרת סיסמא מוצפנת

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

#משווה בין הסיסמא שסופקה לסיסמא שמאוחסנת

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class Ui_settings_page(object):

# פותחת את מסך ההתחברות וסוגרת את עמוד ההגדרות

    def show_login(self, settings):
        self.window = QtWidgets.QMainWindow()
        self.ui = login.Ui_login()
        self.ui.setupUi(self.window)
        self.window.show()
        settings.close()

# משנה את סיסמת המשתמש

    def change_password(self, current, new_password, confirm):
        if len(current) == 0:
            self.message(OOPS, NO_CURRENT)
        elif len(new_password) == 0:
            self.message(OOPS, NO_NEW_PASSWORD)
        elif len(confirm) == 0:
            self.message(OOPS, NOT_CONFIRM_PASSWORD)
        else:
            conn = sqlite3.connect('UsersForm.db')
            with conn:
                cursor = conn.cursor()
            query = "SELECT Password FROM users WHERE Username = ?"
            cursor.execute(query, [self.username.text()])
            if not verify_password(cursor.fetchall()[0][0], current):
                self.message(WRONG_PASSWORD, WRONG_PASSWORD_MSG)
            else:
                if confirm != new_password:
                    self.message(NOT_CONFIRMED, NOT_CONFIRMED_MSG)
                else:
                    new_password = hash_password(new_password)
                    cursor.execute(
                        "UPDATE users\nSET Password = '" + new_password + "'\nWHERE Username = '" + self.username.text() +
                        "'")
                    conn.commit()
                    self.message(CHANGED, CHANGED_PASSWORD_MAG)

# משנה את שם המשתמש

    def change_username(self, username, replace_username):
        print(username)
        print(replace_username)
        print("here u change the UserName")
        if not replace_username:
            self.message(NEW_NAME, NO_NEW_NAME_ERROR)
        else:
            conn = sqlite3.connect('UsersForm.db')
            with conn:
                cursor = conn.cursor()
            query = "SELECT * FROM users WHERE Username = ?"
            cursor.execute(query, [replace_username])
            if len(cursor.fetchall()) > 0:
                self.message(USERNAME_TAKEN, USERNAME_TAKEN_ERROR)
            else:
                cursor.execute("UPDATE users\nSET Username = '" + replace_username + "'\nWHERE Username = '" + username + "'")
                conn.commit()
                print("Changed UserName Successfully")
                self.username_msg.setText("YOUR CURRENT USERNAME IS: " + replace_username)
                self.username.setText(replace_username)
                self.message(CHANGED, CHANGED_NAME_MAG)
            cursor.execute("SELECT * FROM users")
            print(cursor.fetchall())

# מציגה את תיבת ההודעה

    def message(self, title, msg):
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle(title)
        mb.setText(msg)
        mb.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mb.exec_()

# פותחת את העמוד הראשי וסוגרת את עמוד ההגדרות

    def show_main_page(self, settings):
        """the function opens the main page and closes the current settings page"""
        self.window = QtWidgets.QMainWindow()
        self.ui = main_page.Ui_MainPage()
        self.ui.setupUi(self.window)
        self.ui.username.setText(self.username.text())
        self.window.show()
        self.ui.welcome_msg.setText(WELCOME_MSG1 + self.username.text().upper() + WELCOME_MSG2)
        settings.close()

# מגדיר אצל המשתמש את עמוד ההגדרות

    def setupUi(self, settings_page):
        settings_page.setObjectName("settings_page")
        settings_page.resize(972, 664)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./pics/logox.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        settings_page.setWindowIcon(icon)
        settings_page.setLayoutDirection(QtCore.Qt.RightToLeft)
        settings_page.setStyleSheet("background-color: rgb(66, 186, 240);")
        settings_page.setTabShape(QtWidgets.QTabWidget.Rounded)
        settings_page.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint)
        self.centralwidget = QtWidgets.QWidget(settings_page)
        self.centralwidget.setObjectName("centralwidget")
        self.username = QtWidgets.QLabel(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(10, 250, 200, 55))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.username.setFont(font)
        self.username.setAutoFillBackground(False)
        self.username.setStyleSheet("font: 10pt \"Century Gothic\";\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "")
        self.username.setAlignment(QtCore.Qt.AlignCenter)
        self.username.setObjectName("USERNAME")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 610, 221, 16))
        self.line_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.user_symbol = QtWidgets.QLabel(self.centralwidget)
        self.user_symbol.setGeometry(QtCore.QRect(75, 180, 70, 70))
        self.user_symbol.setPixmap(QtGui.QPixmap("./pics/USER.png"))
        self.user_symbol.setScaledContents(True)
        self.user_symbol.setObjectName("user_symbol")
        self.settings_msg_2 = QtWidgets.QLabel(self.centralwidget)
        self.settings_msg_2.setGeometry(QtCore.QRect(240, 10, 561, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.settings_msg_2.setFont(font)
        self.settings_msg_2.setAutoFillBackground(False)
        self.settings_msg_2.setStyleSheet("font: 12pt  \"Century Gothic\";\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "")
        self.settings_msg_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.settings_msg_2.setObjectName("settings_msg_2")
        self.icon = QtWidgets.QLabel(self.centralwidget)
        self.icon.setGeometry(QtCore.QRect(5, 0, 220, 196))
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap("./pics/logox.PNG"))
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(220, 0, 3, 664))
        self.line.setStyleSheet("color: rgb(255, 255, 255);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.log_out_btn = QtWidgets.QPushButton(self.centralwidget)
        self.log_out_btn.setGeometry(QtCore.QRect(0, 620, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.log_out_btn.setFont(font)
        self.log_out_btn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.log_out_btn.setStyleSheet("background-color: rgb(66, 186, 240);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "border: 3px white;")
        self.log_out_btn.setAutoDefault(True)
        self.log_out_btn.setDefault(True)
        self.log_out_btn.setFlat(False)
        self.log_out_btn.setObjectName("log_out_btn")
        self.log_out_btn.clicked.connect(lambda checked: self.show_login(settings_page))
        self.username_msg = QtWidgets.QLabel(self.centralwidget)
        self.username_msg.setGeometry(QtCore.QRect(240, 90, 711, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setItalic(True)
        self.username_msg.setFont(font)
        self.username_msg.setStyleSheet("color: rgb(255, 255, 255);")
        self.username_msg.setObjectName("USERNAME")
        self.username_msg_2 = QtWidgets.QLabel(self.centralwidget)
        self.username_msg_2.setGeometry(QtCore.QRect(240, 115, 711, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setItalic(True)
        self.username_msg_2.setFont(font)
        self.username_msg_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.username_msg_2.setObjectName("username_msg_2")
        self.change_name_btn = QtWidgets.QRadioButton(self.centralwidget)
        self.change_name_btn.setGeometry(QtCore.QRect(520, 114, 20, 20))
        self.change_name_btn.setText("")
        self.change_name_btn.setObjectName("change_name_btn")
        self.password_change_msg = QtWidgets.QLabel(self.centralwidget)
        self.password_change_msg.setGeometry(QtCore.QRect(240, 230, 711, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setItalic(True)
        self.password_change_msg.setFont(font)
        self.password_change_msg.setStyleSheet("color: rgb(255, 255, 255);")
        self.password_change_msg.setObjectName("password_change_msg")
        self.current_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.current_pass.setGeometry(QtCore.QRect(250, 290, 270, 30))
        self.current_pass.setStyleSheet("QTextEdit {\n"
                                        "    border: 1px solid white;\n"
                                        "}")
        self.current_pass.setObjectName("current_pass")
        self.current_pass.setEchoMode(QLineEdit.Password)
        self.password_text = QtWidgets.QLabel(self.centralwidget)
        self.password_text.setGeometry(QtCore.QRect(250, 270, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.password_text.setFont(font)
        self.password_text.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font:bold 8pt \"Century Gothic\";")
        self.password_text.setObjectName("password_text")
        self.new_username = QtWidgets.QLineEdit(self.centralwidget)
        self.new_username.setGeometry(QtCore.QRect(490, 110, 270, 30))
        self.new_username.setStyleSheet("QTextEdit {\n"
                                        "    border: 1px solid white;\n"
                                        "}")
        self.new_username.setObjectName("new_username")
        self.password_text_2 = QtWidgets.QLabel(self.centralwidget)
        self.password_text_2.setGeometry(QtCore.QRect(250, 340, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.password_text_2.setFont(font)
        self.password_text_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "font:bold 8pt \"Century Gothic\";")
        self.password_text_2.setObjectName("password_text_2")
        self.new_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pass.setGeometry(QtCore.QRect(250, 360, 270, 30))
        self.new_pass.setStyleSheet("QTextEdit {\n"
                                    "    border: 1px solid white;\n"
                                    "}")
        self.new_pass.setObjectName("new_pass")
        self.new_pass.setEchoMode(QLineEdit.Password)
        self.confirmpassword = QtWidgets.QLineEdit(self.centralwidget)
        self.confirmpassword.setGeometry(QtCore.QRect(250, 430, 270, 30))
        self.confirmpassword.setStyleSheet("QTextEdit {\n"
                                           "    border: 1px solid white;\n"
                                           "}")
        self.confirmpassword.setObjectName("confirmpassword")
        self.confirmpassword.setEchoMode(QLineEdit.Password)
        self.password_text_3 = QtWidgets.QLabel(self.centralwidget)
        self.password_text_3.setGeometry(QtCore.QRect(250, 410, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.password_text_3.setFont(font)
        self.password_text_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "font:bold 8pt \"Century Gothic\";")
        self.password_text_3.setObjectName("password_text_3")
        self.change_password_btn = QtWidgets.QPushButton(self.centralwidget)
        self.change_password_btn.setGeometry(QtCore.QRect(250, 487, 271, 35))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.change_password_btn.setFont(font)
        self.change_password_btn.setStyleSheet("color: rgb(81, 139, 141);\n"
                                               "background-color: rgb(255, 255, 255);")
        self.change_password_btn.setAutoDefault(True)
        self.change_password_btn.setDefault(True)
        self.change_password_btn.setFlat(False)
        self.change_password_btn.setObjectName("change_password_btn")
        self.change_password_btn.clicked.connect(lambda checked: self.change_password(self.current_pass.text(),
                                                                                      self.new_pass.text(),
                                                                                      self.confirmpassword.text()))
        self.change_username_btn = QtWidgets.QPushButton(self.centralwidget)
        self.change_username_btn.setGeometry(QtCore.QRect(240, 150, 221, 35))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.change_username_btn.setFont(font)
        self.change_username_btn.setStyleSheet("color: rgb(81, 139, 141);\n"
                                               "background-color: rgb(255, 255, 255);")
        self.change_username_btn.setAutoDefault(True)
        self.change_username_btn.setDefault(True)
        self.change_username_btn.setFlat(False)
        self.change_username_btn.setObjectName("change_username_btn")
        self.change_username_btn.clicked.connect(
            lambda checked: self.change_username(self.username.text(), self.new_username.text()))
        self.back_to_home_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_to_home_btn.setGeometry(QtCore.QRect(850, 20, 111, 28))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.back_to_home_btn.setFont(font)
        self.back_to_home_btn.setStyleSheet("color: rgb(255, 255, 255);")
        self.back_to_home_btn.setFlat(True)
        self.back_to_home_btn.setObjectName("back_to_home_btn")
        self.back_to_home_btn.clicked.connect(lambda checked: self.show_main_page(settings_page))
        self.icon.raise_()
        self.username.raise_()
        self.line_2.raise_()
        self.user_symbol.raise_()
        self.settings_msg_2.raise_()
        self.line.raise_()
        self.log_out_btn.raise_()
        self.username_msg.raise_()
        self.username_msg_2.raise_()
        self.change_name_btn.raise_()
        self.password_change_msg.raise_()
        self.current_pass.raise_()
        self.password_text.raise_()
        self.new_username.raise_()
        self.password_text_2.raise_()
        self.new_pass.raise_()
        self.confirmpassword.raise_()
        self.password_text_3.raise_()
        self.change_password_btn.raise_()
        self.change_username_btn.raise_()
        self.back_to_home_btn.raise_()
        settings_page.setCentralWidget(self.centralwidget)

        self.retranslateUi(settings_page)
        QtCore.QMetaObject.connectSlotsByName(settings_page)

    # מגדיר את הטקסטים בשפה הרצויה

    def retranslateUi(self, settings_page):
        _translate = QtCore.QCoreApplication.translate
        settings_page.setWindowTitle(_translate("settings_page", "MainWindow"))
        self.username.setText(_translate("settings_page", "USERNAME"))
        self.settings_msg_2.setText(_translate("settings_page", "Settings:"))
        self.log_out_btn.setText(_translate("settings_page", "LOG OUT"))
        self.username_msg.setText("YOUR CURRENT USERNAME IS: "+self.username.text())
        self.username_msg_2.setText(_translate("settings_page", "YOU CAN CHANGE IT HERE >"))
        self.password_change_msg.setText(_translate("settings_page", "YOU CAN ALSO CHANGE YOUR PASSWORD OVER HERE:"))
        self.password_text.setText(_translate("settings_page", "CURRENT PASSWORD"))
        self.password_text_2.setText(_translate("settings_page", "NEW PASSWORD"))
        self.password_text_3.setText(_translate("settings_page", "CONFIRM NEW PASSWORD"))
        self.change_password_btn.setText(_translate("settings_page", "CHANGE PASSWORD "))
        self.change_username_btn.setText(_translate("settings_page", "CHANGE USERNAME "))
        self.back_to_home_btn.setText(_translate("settings_page", "HOME →"))

