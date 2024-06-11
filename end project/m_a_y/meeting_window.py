import pickle
import struct
import imutils
import pyaudio
import pyautogui
import time

import MeAndYou_Server
from PIL import ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import cv2
import socket
import threading
import encryption
import main_page
import numpy
import new_meeting_dialog
import join_meeting
import magic_strings



SCREENSHOT_KEY = "SCREENSHOT"
IP = magic_strings.IP
VIDEO_PORT = magic_strings.VIDEO_PORT
SOUND_PORT = magic_strings.SOUND_PORT
SHARING_PORT = magic_strings.SHARING_PORT
CHAT_PORT = magic_strings.CHAT_PORT
END_PORT = magic_strings.END_PORT
KEY = magic_strings.KEY
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
CHUNK_SIZE = magic_strings.CHUNK_SIZE
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = magic_strings.CHANNELS
RATE = magic_strings.RATE
CAMERA_OPEN = "TY MEETING"
CAMERA_OPEN_MSG = "HI! PLEASE WAIT 'TILL CAMERA OPEN IN A FEW SECONDS"
END_MEETING = "END_MEETING"
CONFIRM = "YES"
UNCONFIRMED = "NO!"
END_MEETING_ERROR = "OOPS!"
END_MEETING_MSG = "WE COULDN'T HANG UP THE MEETING, PLEASE TRY AGAIN (:"
END_THE_SHARING = "END THE SHARING!"
END_THE_VIDEO = "END_THE_VIDEO!!!"
WELCOME_MSG1 = "HELLO "
WELCOME_MSG2 = ", NICE TO SEE YOU :)"
keep_going = True
sharing = False
aes_key = None
aes_iv = None

# קובע את מפתחות ההצפנה

def set_keys():
    key, iv = new_meeting_dialog.get_keys()
    global aes_key, aes_iv
    if key and iv:
        aes_key = key
        aes_iv = iv
    else:
        key, iv = join_meeting.get_keys()
        aes_key = key
        aes_iv = iv
    print(aes_key, aes_iv)

#מקבל ומפענח נתוני וידאו מהשרת

def receiving_video(my_socket):
    data = b""
    payload_size = struct.calcsize("16s I")
    end = encryption.do_encrypt(aes_key, aes_iv, END_THE_VIDEO.encode())
    global keep_going
    while keep_going and end not in data:
        try:
            if end in data:
                cv2.destroyWindow(client_name + "'S VIDEO")
                data = b""
                print("ending the video")
            while len(data) < payload_size:
                data += my_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("16s I", packed_msg_size)
            client_name = msg_size[0]
            client_name = encryption.do_decrypt(aes_key, aes_iv, client_name).decode()
            client_name = str(client_name).replace("%", '')
            msg_size = msg_size[1]
            while len(data) < msg_size:
                data += my_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = encryption.do_decrypt(aes_key, aes_iv, frame_data)
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(client_name + "'S VIDEO", frame)
            cv2.waitKey(1)
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass
    #cv2.destroyAllWindows()

#שולח הודעות צ'אט מוצפנות לשרת

def msgs_send(chat_socket, msg, name, msg_text):
    name += "%" * (16 - len(name))
    client_name = encryption.do_encrypt(aes_key, aes_iv, name.encode())
    size = len(msg.encode())
    msg = encryption.do_encrypt(aes_key, aes_iv, msg.encode())
    chat_socket.send(client_name + size.to_bytes(4, "big") + msg)
    print("sent msg")
    msg_text.clear()

# מקבל הודעות צ'אט מהשרת ומציג אותן בתיבת צ'אט

def msgs_recv(chat_socket, chat_box):
    global keep_going
    while keep_going:
        try:
            client_name = chat_socket.recv(16)
            client_name = encryption.do_decrypt(aes_key, aes_iv, client_name).decode()
            client_name = str(client_name).replace("%", '')
            print("got client name")
            size = int.from_bytes(chat_socket.recv(4), "big")
            data = chat_socket.recv(size)
            data = encryption.do_decrypt(aes_key, aes_iv, data).decode()
            if END_THE_VIDEO in data:
                cv2.destroyWindow(client_name + "'S VIDEO")
            if data and client_name:
                line = client_name + ":\n" + data
                print("adding text")
                chat_box.append(line)
        except ConnectionAbortedError:
            #print("in ex 129")
            print("error connection aborted")
        except ConnectionResetError:
            #print ("in ex 129")
            print("error reser error")

#מקבלת מהשרת נתוני מסך ומציג אותו

def receiving_share_screen(share_socket):
    data = b""
    end = encryption.do_encrypt(aes_key, aes_iv, END_THE_SHARING.encode())
    payload_size = struct.calcsize("16s I")
    global keep_going
    while keep_going:
        print("sharing screen")
        try:
            while len(data) < payload_size:
                data += share_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("16s I", packed_msg_size)
            client_name = msg_size[0]
            print(client_name)
            if client_name:
                client_name = encryption.do_decrypt(aes_key, aes_iv, client_name).decode()
                client_name = str(client_name).replace("%", '')
                print("this is my client name " + client_name)
                msg_size = msg_size[1]
                while len(data) < msg_size:
                    data += share_socket.recv(4096)
                if end in data:
                    cv2.destroyWindow(client_name + "'S SCREEN")
                    data = b""
                    print("ending the share")
                else:
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame_data = encryption.do_decrypt(aes_key, aes_iv, frame_data)
                    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                    frame = numpy.fromstring(frame, numpy.uint8)
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    cv2.imshow(client_name + "'S SCREEN", imutils.resize(frame, width=1200))
                    cv2.waitKey(1)
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass
    # cv2.destroyAllWindows()

# שולח נתוני קול מהלקוח לשרת

def sound_recording(sound_socket, recording_stream):
    global keep_going
    while keep_going:
        try:
            data = recording_stream.read(1024)
            sound_socket.sendall(data)
            print("sending")
        except socket.error:
            pass

#מקבל נתוני קול מהשרת ומשמיע אותם

def sound_receiving(sound_socket, playing_stream):
    global keep_going
    while keep_going :
        try:
            data = sound_socket.recv(1024)
            playing_stream.write(data)
            print("sound")
        except socket.error:
            pass

#שולח תמונת מסך מהלקוח לשרת ומצפינה אותו

def screen_share(share_socket, name):
    global keep_going, sharing
    print(sharing)
    while keep_going and sharing:
        image = pyautogui.screenshot()
        image = draw_mouse(image)
        image = cv2.cvtColor(numpy.array(image),
                             cv2.COLOR_RGB2BGR)
        frame = cv2.imencode('.jpg', image)
        data = frame[1].tostring()
        data = pickle.dumps(data, 0)
        data = encryption.do_encrypt(aes_key, aes_iv, data)
        size = len(data)
        name += "%" * (16 - len(name))
        client_name = encryption.do_encrypt(aes_key, aes_iv, name.encode())
        if share_socket:
            share_socket.sendall(struct.pack('16s I', client_name, size) + data)
            print("sent screenshot")
    name += "%" * (16 - len(name))
    client_name = encryption.do_encrypt(aes_key, aes_iv, name.encode())
    data = encryption.do_encrypt(aes_key, aes_iv, END_THE_SHARING.encode())
    size = len(data)
    share_socket.sendall(struct.pack('16s I', client_name, size) + data)
    # cv2.destroyAllWindows()

#מתחיל את תהליך שיתוף המסך

def open_screenshare(share_socket, name, start_btn, end_btn):
    print("open screenshare")
    start_btn.setEnabled(False)
    end_btn.setDisabled(False)
    end_btn.setChecked(False)
    print("name: " + name)
    global sharing
    sharing = True
    sharing_screen = threading.Thread(target=screen_share, args=[share_socket, name])
    sharing_screen.start()




def draw_mouse(img):
    # generate Draw object for PIL image
    draw = ImageDraw.Draw(img)
    # find current position of mouse pointer
    pos = pyautogui.position()
    # coordinates of ellipse
    ax, ay, bx, by = pos[0], pos[1], pos[0] + 10, pos[1] + 10
    # draw ellipse on image
    draw.ellipse((ax, ay, bx, by), fill="yellow")
    return img


#

def message(title, msg):
    # present a message with information for the user
    mb = QtWidgets.QMessageBox()
    mb.setWindowTitle(title)
    mb.setText(msg)
    mb.setStandardButtons(QtWidgets.QMessageBox.Ok)
    mb.exec_()


def end_share(s_btn):
    global sharing
    sharing = False
    s_btn.setChecked(True)
    s_btn.setDisabled(True)


def show_main_page(meeting_window, user_name):
    # closes the current login page and open the main page
    window = QtWidgets.QMainWindow ()
    ui = main_page.Ui_MainPage ()
    ui.setupUi (window)
    window.show (user_name)
    ui.username.setText ()
    meeting_window.close ()
    ##pass


class Ui_meeting_window(object):

    # מציג את הדף הראשי וסוגר את חלון הפגישה

    def sending_image(self, my_socket):
        global keep_going
        video_capture_object = cv2.VideoCapture(0)
        video_capture_object.set(3, 250)
        while keep_going is True:
            ret, frame = video_capture_object.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow("MY VIDEO", frame)
            cv2.waitKey(1)
            name = self.username.text()
            name += "%" * (16 - len(name))
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(frame, 0)
            data = encryption.do_encrypt(aes_key, aes_iv, data)
            size = len(data)
            name = encryption.do_encrypt(aes_key, aes_iv, name.encode())
            if my_socket:
                try:
                    my_socket.sendall(struct.pack('16s I', name, size) + data)
                except socket.error:
                    pass
        video_capture_object.release()
        # cv2.destroyAllWindows()

# עוזרת לסיים את הפגישה וסוגרת את הסוקטים

    def ending_meeting(self, meeting_win, video_socket, sound_socket, share_socket, chat_socket):
        try:
            data = encryption.do_encrypt (aes_key, aes_iv, END_THE_VIDEO.encode ())
            size = len (data)
            video_socket.sendall (struct.pack ('16s I', data, size) + data)
            end_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            end_socket.connect((IP, END_PORT))
            msg = END_MEETING + "/" + self.meeting_id.text().replace("MEETING ID: ", "") + "/" + self.username.text()
            msg = encryption.do_encrypt(aes_key, aes_iv, msg.encode())
            end_socket.send(len(msg).to_bytes(4, "big") + msg)
            size = int.from_bytes(end_socket.recv(4), "big")
            data = end_socket.recv(size)
            data = encryption.do_decrypt(aes_key, aes_iv, data).decode()
            if data != CONFIRM:
                message(END_MEETING_ERROR, END_MEETING_MSG)
            else:
                global keep_going
                sound_socket.close()
                share_socket.close()
                video_socket.close()
                chat_socket.close()
                end_socket.close()
                print("closed")
                keep_going = False
                self.window = QtWidgets.QMainWindow()
                self.ui = main_page.Ui_MainPage()
                self.ui.setupUi(self.window)
                self.ui.username.setText(self.username.text())
                meeting_win.close()
                self.ui.welcome_msg.setText (WELCOME_MSG1 + self.username.text().upper () + WELCOME_MSG2)
                self.window.show()
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass
        #time.sleep(1)
        #cv2.destroyAllWindows()

#מגדיר את החלון פגישה ע"י אובייקטים ונתונים

    def setupUi(self, meeting_window):
        meeting_window.setObjectName("meeting_window")
        meeting_window.resize(442, 674)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(meeting_window.sizePolicy().hasHeightForWidth())
        meeting_window.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./pics/new_logom1.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        meeting_window.setWindowIcon(icon)
        meeting_window.setStyleSheet("background-color: rgb(66,186,230);")
        self.centralwidget = QtWidgets.QWidget(meeting_window)
        meeting_window.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint)
        self.centralwidget.setObjectName("centralwidget")
        self.share_screen_btn = QtWidgets.QPushButton(self.centralwidget)
        self.share_screen_btn.setObjectName("share_screen_btn")
        self.share_screen_btn.setGeometry(QtCore.QRect(30, 80, 191, 31))
        font = QtGui.QFont()
        font.setFamily(u"Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.share_screen_btn.setFont(font)
        self.share_screen_btn.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                            "\n"
                                            "color: rgb(81, 139, 141);")
        self.share_screen_btn.setCheckable(True)
        self.share_screen_btn.setChecked(False)
        self.share_screen_btn.setAutoDefault(True)
        self.share_screen_btn.setFlat(False)
        self.share_screen_btn.setObjectName("share_screen_btn")
        self.share_screen_btn.clicked.connect(lambda checked: open_screenshare(share_socket, self.username.text(),
                                                                               self.share_screen_btn,
                                                                               self.end_share_btn))
        self.end_share_btn = QtWidgets.QPushButton(self.centralwidget)
        self.end_share_btn.setObjectName("end_share_btn")
        self.end_share_btn.setGeometry(QtCore.QRect(230, 80, 191, 31))
        self.end_share_btn.setFont(font)
        self.end_share_btn.setCheckable(True)
        self.end_share_btn.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(170, 0, 0);\n"
                                         "color: rgb(255, 255, 255);")
        self.end_share_btn.setCheckable(True)
        self.end_share_btn.setChecked(False)
        self.end_share_btn.setAutoDefault(True)
        self.end_share_btn.setFlat(False)
        self.end_share_btn.setDisabled(True)
        self.end_share_btn.clicked.connect(lambda checked: end_share(self.share_screen_btn))
        self.username = QtWidgets.QLabel(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(20, 10, 101, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.username.setFont(font)
        self.username.setStyleSheet("color: rgb(255, 255, 255);")
        self.username.setObjectName("username")
        self.meeting_id = QtWidgets.QLabel(self.centralwidget)
        self.meeting_id.setGeometry(QtCore.QRect(20, 30, 341, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.meeting_id.setFont(font)
        self.meeting_id.setStyleSheet("color: rgb(255, 255, 255);")
        self.meeting_id.setObjectName("meeting_id")
        self.meeting_password = QtWidgets.QLabel(self.centralwidget)
        self.meeting_password.setGeometry(QtCore.QRect(20, 50, 341, 19))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.meeting_password.setFont(font)
        self.meeting_password.setStyleSheet("color: rgb(255, 255, 255);")
        self.meeting_password.setObjectName("meeting_password")
        self.phone_symbol = QtWidgets.QLabel(self.centralwidget)
        self.phone_symbol.setGeometry(QtCore.QRect(360, 0, 60, 60))
        self.phone_symbol.setPixmap(QtGui.QPixmap("./pics/end_met.png"))
        self.phone_symbol.setScaledContents(True)
        self.phone_symbol.setObjectName("phone_symbol")
        self.end_meeting_btn = QtWidgets.QPushButton(self.centralwidget)
        self.end_meeting_btn.setGeometry(QtCore.QRect(380, 20, 41, 41))
        self.end_meeting_btn.setFlat(True)
        self.end_meeting_btn.setObjectName("end_meeting_btn")
        self.end_meeting_btn.clicked.connect(lambda checked: self.ending_meeting(meeting_window, video_socket,
                                                                                 sound_socket, share_socket,
                                                                                 chat_socket))
        self.chat_text = QtWidgets.QTextEdit(self.centralwidget)
        self.chat_text.setGeometry(QtCore.QRect(30, 120, 391, 461))
        self.chat_text.setStyleSheet("color: rgb(81, 139, 141);\n"
                                    "background-color: rgb(255, 255, 255);")
        self.chat_text.setFrameShape(QtWidgets.QFrame.Box)
        self.chat_text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.chat_text.setReadOnly(True)
        self.chat_text.setObjectName("chat_text")
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.chat_text.setFont(font)
        self.msg_text = QtWidgets.QTextEdit(self.centralwidget)
        self.msg_text.setGeometry(QtCore.QRect(30, 600, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.msg_text.setFont(font)
        self.msg_text.setStyleSheet("color: rgb(81, 139, 141);\n"
                                   "background-color: rgb(255, 255, 255);")
        self.msg_text.setFrameShape(QtWidgets.QFrame.Box)
        self.msg_text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.msg_text.setObjectName("msg_text")
        self.send_btn = QtWidgets.QPushButton(self.centralwidget)
        self.send_btn.setGeometry(QtCore.QRect(340, 600, 81, 41))
        self.send_btn.clicked.connect(lambda checked: msgs_send(chat_socket, self.msg_text.toPlainText(),
                                                                self.username.text(), self.msg_text))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.send_btn.setFont(font)
        self.send_btn.setStyleSheet("color: rgb(81, 139, 141);\n"
                                    "background-color: rgb(255, 255, 255);")
        self.send_btn.setAutoDefault(True)
        self.send_btn.setDefault(True)
        self.send_btn.setFlat(False)
        self.send_btn.setObjectName("send_btn")
        self.phone_symbol.raise_()
        self.share_screen_btn.raise_()
        self.username.raise_()
        self.meeting_id.raise_()
        self.meeting_password.raise_()
        self.end_meeting_btn.raise_()
        self.chat_text.raise_()
        self.msg_text.raise_()
        self.send_btn.raise_()
        meeting_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(meeting_window)
        QtCore.QMetaObject.connectSlotsByName(meeting_window)

        global keep_going
        keep_going = True
        print("opened client")
        set_keys()
        video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        video_socket.connect((IP, VIDEO_PORT))
        sound_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sound_socket.connect((IP, SOUND_PORT))
        chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chat_socket.connect((IP, CHAT_PORT))
        print("yay connected")
        share_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        share_socket.connect((IP, 1234))
        audio = pyaudio.PyAudio()
        playing_stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True,
                                    frames_per_buffer=CHUNK_SIZE)
        recording_stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True,
                                      frames_per_buffer=CHUNK_SIZE)
        receiving_share = threading.Thread(target=receiving_share_screen, args=[share_socket])
        receiving_share.start()
        receiving_msgs = threading.Thread(target=msgs_recv, args=[chat_socket, self.chat_text])
        receiving_msgs.start()
        sending = threading.Thread(target=self.sending_image, args=[video_socket])
        sending.start()
        receiving = threading.Thread(target=receiving_video, args=[video_socket])
        receiving.start()
        audio = threading.Thread(target=sound_recording, args=[sound_socket, recording_stream])
        audio.start()
        playing = threading.Thread(target=sound_receiving, args=[sound_socket, playing_stream])
        playing.start()

# מגדיר את הטקסטים בשפה הרצויה

    def retranslateUi(self, meeting_window):
        _translate = QtCore.QCoreApplication.translate
        meeting_window.setWindowTitle(_translate("meeting_window", "M&Y MEETING"))
        self.share_screen_btn.setText(_translate("meeting_window", "START SHARE SCREEN"))
        self.end_share_btn.setText(_translate("meeting_window", "END SHARE SCREEN"))
        self.username.setText(_translate("meeting_window", "USERNAME "))
        self.meeting_id.setText(_translate("meeting_window", "MEETING ID:"))
        self.meeting_password.setText(_translate("meeting_window", "MEETING PASSWORD:"))
        self.send_btn.setText(_translate("meeting_window", "SEND"))