
import login
from PyQt5 import QtCore, QtGui, QtWidgets
import settings_window
import join_meeting
import new_meeting_dialog


class Ui_MainPage(object):
    #מציג את דף ההתחברות
    def show_login(self, main_page):
        self.window = QtWidgets.QMainWindow()
        self.ui = login.Ui_login()
        self.ui.setupUi(self.window)
        self.window.show()
        main_page.close()
    #מציג את דף ההגדרות
    def show_settings_page(self, main_page):
        self.window = QtWidgets.QMainWindow()
        self.ui = settings_window.Ui_settings_page()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.username.setText(self.username.text())
        self.ui.username_msg.setText("YOUR CURRENT USERNAME IS: "+self.username.text())
        main_page.close()

    # פתיחת דף יצירת פגישה
    def open_meeting(self, main_page):
        self.window = QtWidgets.QMainWindow()
        self.ui = new_meeting_dialog.Ui_new_meeting_dialog()
        self.ui.setupUi(self.window)
        self.ui.username.setText(self.username.text())
        self.window.show()
        main_page.close()

        #פתיחת דף הצטרפות לפגישה
    def join_meeting(self, main_page):
        self.window = QtWidgets.QMainWindow()
        self.ui = join_meeting.Ui_Dialog()
        self.ui.setupUi(self.window)
        self.ui.username.setText(self.username.text().upper())
        self.window.show()
        main_page.close()

    # מגדיר את חלון הדף הראשי ע"י לחצנים ותמונות

    def setupUi(self, MainPage):
        MainPage.setObjectName("MainPage")
        MainPage.resize(972, 664)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./pics/new_logom1.PNG"),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainPage.setWindowIcon(icon)
        MainPage.setAutoFillBackground(False)
        MainPage.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint)
        MainPage.setStyleSheet("background-color: rgb(66, 186, 240);")
        self.centralwidget = QtWidgets.QWidget(MainPage)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(220, 0, 3, 664))
        self.line.setStyleSheet("color: rgb(255, 255, 255);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.icon = QtWidgets.QLabel(self.centralwidget)
        self.icon.setGeometry(QtCore.QRect(0, 10, 220, 196))
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap("./pics/logox.PNG"))
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")
        self.username = QtWidgets.QLabel(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(0, 185, 220, 50))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.username.setFont(font)
        self.username.setAutoFillBackground(True)
        self.username.setStyleSheet("font: 15pt \"Century Gothic\";\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "")
        self.username.setAlignment(QtCore.Qt.AlignCenter)
        self.username.setObjectName("username")
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
        self.log_out_btn.clicked.connect(lambda checked: self.show_login(MainPage))
        self.log_out_btn.setAutoDefault(True)
        self.log_out_btn.setDefault(True)
        self.log_out_btn.setFlat(False)
        self.log_out_btn.setObjectName("log_out_btn")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 610, 221, 16))
        self.line_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.join_a_meeting_symbol = QtWidgets.QLabel(self.centralwidget)
        self.join_a_meeting_symbol.setGeometry(QtCore.QRect(286, 131, 268, 246))
        self.join_a_meeting_symbol.setPixmap(QtGui.QPixmap("./pics/lets-go.png"))
        self.join_a_meeting_symbol.setScaledContents(True)
        self.join_a_meeting_symbol.setObjectName("join_a_meeting_symbol")
        self.start_a_meeting_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_a_meeting_btn.setGeometry(QtCore.QRect(300, 170, 241, 161))
        self.start_a_meeting_btn.setFlat(True)
        self.start_a_meeting_btn.setObjectName("start_a_meeting_btn")
        self.start_a_meeting_btn.clicked.connect(lambda checked: self.open_meeting(MainPage))
        self.join_a_meeting_symbol_2 = QtWidgets.QLabel(self.centralwidget)
        self.join_a_meeting_symbol_2.setGeometry(QtCore.QRect(634, 131, 268, 246))
        self.join_a_meeting_symbol_2.setText("")
        self.join_a_meeting_symbol_2.setPixmap(QtGui.QPixmap("./pics/join.png"))
        self.join_a_meeting_symbol_2.setScaledContents(True)
        self.join_a_meeting_symbol_2.setObjectName("join_a_meeting_symbol_2")
        self.join_a_meeting_btn = QtWidgets.QPushButton(self.centralwidget)
        self.join_a_meeting_btn.setGeometry(QtCore.QRect(650, 170, 241, 161))
        self.join_a_meeting_btn.setGeometry(QtCore.QRect(650, 170, 150, 150))
        self.join_a_meeting_btn.setText("")
        self.join_a_meeting_btn.setFlat(True)
        self.join_a_meeting_btn.setObjectName("join_a_meeting_btn")
        self.join_a_meeting_btn.clicked.connect(lambda checked: self.join_meeting(MainPage))
        self.settings_symbol = QtWidgets.QLabel(self.centralwidget)
        #self.settings_symbol.setGeometry(QtCore.QRect(450, 370, 268, 246))
        self.settings_symbol.setGeometry(QtCore.QRect(500, 410, 150, 150))
        self.settings_symbol.setText("")
        self.settings_symbol.setPixmap(QtGui.QPixmap("./pics/settings.png"))
        self.settings_symbol.setScaledContents(True)
        self.settings_symbol.setObjectName("settings_symbol")
        self.welcome_msg = QtWidgets.QLabel(self.centralwidget)
        self.welcome_msg.setGeometry(QtCore.QRect(240, 10, 561, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.welcome_msg.setFont(font)
        self.welcome_msg.setAutoFillBackground(False)
        self.welcome_msg.setStyleSheet("font: 12pt  \"Century Gothic\";\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "")
        self.welcome_msg.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.welcome_msg.setObjectName("welcome_msg")
        self.settings_btn = QtWidgets.QPushButton(self.centralwidget)
        self.settings_btn.setGeometry(QtCore.QRect(460, 410, 241, 161))
        self.settings_btn.setText("")
        self.settings_btn.setFlat(True)
        self.settings_btn.setObjectName("settings_btn")
        self.settings_btn.clicked.connect(lambda checked: self.show_settings_page(MainPage))
        self.start_a_meeting_msg = QtWidgets.QLabel(self.centralwidget)
        self.start_a_meeting_msg.setGeometry(QtCore.QRect(315, 340, 204, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.start_a_meeting_msg.setFont(font)
        self.start_a_meeting_msg.setAutoFillBackground(False)
        self.start_a_meeting_msg.setStyleSheet("font: 12pt  \"Century Gothic\";\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "")
        self.start_a_meeting_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.start_a_meeting_msg.setObjectName("start_a_meeting_msg")
        self.join_a_meeting_msg = QtWidgets.QLabel(self.centralwidget)
        self.join_a_meeting_msg.setGeometry(QtCore.QRect(670, 340, 204, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.join_a_meeting_msg.setFont(font)
        self.join_a_meeting_msg.setAutoFillBackground(False)
        self.join_a_meeting_msg.setStyleSheet("font: 12pt  \"Century Gothic\";\n"
                                              "color: rgb(255, 255, 255);\n"
                                              "")
        self.join_a_meeting_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.join_a_meeting_msg.setObjectName("join_a_meeting_msg")
        self.settings_msg = QtWidgets.QLabel(self.centralwidget)
        self.settings_msg.setGeometry(QtCore.QRect(485, 590, 204, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.settings_msg.setFont(font)
        self.settings_msg.setAutoFillBackground(False)
        self.settings_msg.setStyleSheet("font: 12pt  \"Century Gothic\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "")
        self.settings_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_msg.setObjectName("settings_msg")
        MainPage.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainPage)
        QtCore.QMetaObject.connectSlotsByName(MainPage)

    # משמשת להגדרת טקסטים בדף הראשי

    def retranslateUi(self, MainPage):
        _translate = QtCore.QCoreApplication.translate
        MainPage.setWindowTitle(_translate("MainPage", "M&Y "))
        self.username.setText(_translate("MainPage", "USERNAME"))
        self.log_out_btn.setText(_translate("MainPage", "LOG OUT"))
        self.welcome_msg.setText(_translate("MainPage", "HELLO USERNAME, NICE TO SEE YOU :)"))
        self.start_a_meeting_msg.setText(_translate("MainPage", "START A MEETING"))
        self.join_a_meeting_msg.setText(_translate("MainPage", "JOIN A MEETING"))
        self.settings_msg.setText(_translate("MainPage", "SETTINGS"))


