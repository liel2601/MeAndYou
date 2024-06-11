import binascii #המרה בין נתונים בינאריים לאסקי  קשור להצפנה
import hashlib   #קשור להצפנה

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QLineEdit
import main_page
import register_page
import magic_strings
import sqlite3 #הקמת אחסון נתונים

#INFO_PORT = magic_strings.INFO_PORT
#IP = magic_strings.IP


LOGIN_ERROR = "LOG IN FAILED"
REGISTER = "REGISTER"
WRONG_PASS = "WRONG_PASS"
USERNAME_LEN = "USERNAME_LEN"
PASSWORD_LEN = "PASS_LEN"
LOGIN = "LOG IN"
LOGIN_ERROR_MESSAGE = "INCORRECT USERNAME OR PASSWORD"
USERNAME_ERROR = "NO USERNAME ENTERED"
USERNAME_ERROR_MSG = "PLEASE ENTER A USERNAME"
PASSWORD_ERROR = "NO PASSWORD ENTERED"
PASSWORD_ERROR_MSG = "PLEASE ENTER A PASSWORD"
WELCOME_MSG1 = "HELLO "
WELCOME_MSG2 = ", NICE TO SEE YOU :)"
CONNECTED = "CONNECTED"


def make_database_connection():
    conn = sqlite3.connect('UsersForm.db')
    with conn:
        cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (Username TEXT,Fname TEXT,Lname TEXT,Password '
        'TEXT)')
    conn.commit()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())

#אימות סיסמא

def verify_password(stored_password, provided_password):
    # Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',provided_password.encode('utf-8'),
    salt.encode('ascii'),100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# מציג הודעת שגיאה או מידע למשתמש

def message(title, msg):
    mb = QtWidgets.QMessageBox()
    mb.setWindowTitle(title)
    mb.setText(msg)
    mb.setStandardButtons(QtWidgets.QMessageBox.Ok)
    mb.exec_()

# סוגר את חלון ההתחברות ופותח את החלון הראשי של המערכת

def show_main_page(login, username):
    window = QtWidgets.QMainWindow()
    ui = main_page.Ui_MainPage()
    ui.setupUi(window)
    window.show()
    ui.username.setText(username)
    ui.welcome_msg.setText(WELCOME_MSG1 + username.upper() + WELCOME_MSG2)
    login.close()

# בודקת אם שם המשתמש והסיסמא מתאימים לבסיס הנתונים

def login_function(ui, username, password):
    print(username)
    print(password)
    if len(username) > 0 and len(password) > 0:
        with sqlite3.connect("UsersForm.db") as db:
            cursor = db.cursor()
        query = "SELECT Password FROM users WHERE Username = ?"
        cursor.execute(query, [username])
        stored_password = cursor.fetchall()
        if not stored_password:
            message(LOGIN_ERROR, LOGIN_ERROR_MESSAGE)
        else:
            print(stored_password[0][0])
            if verify_password(stored_password[0][0], password):
                show_main_page(ui, username)
            else:
                message(LOGIN_ERROR, LOGIN_ERROR_MESSAGE)
    elif len(username) == 0:
        message(USERNAME_ERROR, USERNAME_ERROR_MSG)
    else:
        message(PASSWORD_ERROR, PASSWORD_ERROR_MSG)

#כוללת פונקציות ומשתנים שמגדירים את חלון ההתחברות

class Ui_login(object):

    #פותחת את חלון ההרשמה

    def open_register(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = register_page.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    #מגדיר את חלון ההתחברות ע"י לחצנים ותמונות

    def setupUi(self, login):
        login.setObjectName("login")
        login.setEnabled(True)
        login.resize(700, 640)
        login.setStyleSheet("background-color: rgb(20, 160, 233);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./pics/new_logom1.PNG"),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        login.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(login)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(160, 77, 380, 486))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.symbol_camcall = QtWidgets.QLabel(self.frame)
        self.symbol_camcall.setGeometry(QtCore.QRect(120, 30, 150, 150))
        self.symbol_camcall.setFrameShape(QtWidgets.QFrame.VLine)
        self.symbol_camcall.setLineWidth(1)
        self.symbol_camcall.setMidLineWidth(0)
        self.symbol_camcall.setText("")
        self.symbol_camcall.setPixmap(QtGui.QPixmap("./pics/logox.PNG"))
        self.symbol_camcall.setScaledContents(True)
        self.symbol_camcall.setObjectName("symbol_camcall")
        self.password = QtWidgets.QLineEdit(self.frame)
        self.password.setObjectName("password")
        self.password.setGeometry(QtCore.QRect(110, 260, 171, 21))
        self.password.setStyleSheet("color: rgb(81, 139, 141);")
        self.password.setFrame(False)
        font2 = QtGui.QFont()
        font2.setFamily("Century Gothic")
        font2.setPointSize(5)
        self.password.setFont(font2)
        self.password.setEchoMode(QLineEdit.Password)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(64, 230, 252, 2))
        self.line.setAutoFillBackground(False)
        self.line.setStyleSheet("color: rgb(0,0,0);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setGeometry(QtCore.QRect(64, 290, 252, 2))
        self.line_2.setAutoFillBackground(False)
        self.line_2.setStyleSheet("color: rgb(0,0,0);")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 180, 60, 60))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./pics/user.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(58, 240, 60, 60))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("./pics/padlock.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.login_button = QtWidgets.QPushButton(self.frame)
        self.login_button.setGeometry(QtCore.QRect(64, 330, 252, 35))
        self.login_button.clicked.connect(lambda checked: login_function(login, self.username.text(),
                                                                         self.password.text()))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("background-color: rgb(20, 160, 233);\n"
                                        "color: rgb(255,255,255);")
        self.login_button.setAutoDefault(True)
        self.login_button.setDefault(True)
        self.login_button.setFlat(False)
        self.login_button.setObjectName("login_button")
        self.register_button = QtWidgets.QPushButton(self.frame)
        self.register_button.setGeometry(QtCore.QRect(64, 385, 252, 35))
        self.register_button.clicked.connect(self.open_register)
        self.register_button.clicked.connect(login.close)

        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.register_button.setFont(font)
        self.register_button.setAutoFillBackground(False)
        self.register_button.setStyleSheet("border :1px solid; "
                                           "color: rgb(81, 139, 141);\n"
                                           "border-color: rgb(81, 139, 141);")
        self.register_button.setCheckable(False)
        self.register_button.setAutoDefault(False)
        self.register_button.setDefault(True)
        self.register_button.setFlat(True)
        self.register_button.setObjectName("register_button")
        self.username = QtWidgets.QLineEdit(self.frame)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QtCore.QRect(110, 200, 171, 22))
        font1 = QtGui.QFont()
        font1.setFamily(u"Century Gothic")
        font1.setPointSize(10)
        self.username.setStyleSheet(u"color: rgb(81,139, 141);")
        self.username.setFrame(False)
        self.username.setEchoMode(QLineEdit.Normal)
        self.symbol_camcall.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_2.setMaximumSize(50, 50)
        self.label_3.setMaximumSize(50, 50)
        self.line.raise_()
        self.line_2.raise_()
        self.password.raise_()
        self.login_button.raise_()
        self.register_button.raise_()
        self.username.raise_()
        login.setCentralWidget(self.centralwidget)

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)
        #תתחבר לתוך הבסיס נתונים DB
        make_database_connection()

    #מגדירה מחדש את חלון ההתחברות מלחצנים וטקסט

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "LOGIN"))
        self.login_button.setText(_translate("login", "LOG IN"))
        self.register_button.setText(_translate("login", "REGISTER"))
