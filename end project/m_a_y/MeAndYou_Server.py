import struct #מחזיר את כמות הסטרינגים לפי הפורמט
import magic_strings #קלאס שיצרנו בשביל לאחד את כל המשתנים שהם אותו הדבר
import encryption   #הצפנה
import pyaudio      # אחראי על האדיו(שמע)
import socket       #  מודול לממשק עם תכנות רשת
import threading    #מה שאחראי על הדברים שרצים ברקע

from Meeting import Meeting, Me_A_You_Client

LOGIN_PORT = magic_strings.LOGIN_PORT
VIDEO_PORT = magic_strings.VIDEO_PORT
SOUND_PORT = magic_strings.SOUND_PORT
SHARING_PORT = magic_strings.SHARING_PORT
REGISTER_PORT = magic_strings.REGISTER_PORT
CHAT_PORT = magic_strings.CHAT_PORT
INFO_PORT = magic_strings.INFO_PORT
END_PORT = magic_strings.END_PORT
IP = "0.0.0.0"
KEY = magic_strings.KEY
SIZE = 4096
CHUNK = 1024
CHANNELS = magic_strings.CHANNELS
RATE = 10240
INPUT = True
FORMAT = pyaudio.paInt16
MAX_CONNECTIONS = 10
VIDEO_SOCKETS = []
SOUND_SOCKETS = []
CHAT_CLIENTS = []
MEETINGS = []
FRAMES = []
END = "CLOSE AND END"
CREATE_MEETING = "CREATE_MEETING"
JOIN_MEETING = "JOIN_MEETING"
END_MEETING = "END_MEETING"
CONFIRM = "YES"
UNCONFIRMED = "NO!"
TAKEN = "TAKEN"
LOCKED = "LOCKED"
WRONG = "WRONG"
CONNECT = "CONNECT"
CONNECTED = "CONNECTED"
LOGIN_ERROR = "LOG IN FAILED"
REGISTER = "REGISTER"
NOT_FOUND = "NOT FOUND"
WRONG_PASS = "WRONG_PASS"
USERNAME_LEN = "USERNAME_LEN"
PASSWORD_LEN = "PASS_LEN"
LOGIN = "LOG IN"
LOGIN_ERROR_MESSAGE = "INCORRECT USERNAME OR PASSWORD"
USERNAME_ERROR = "NO USERNAME ENTERED"
USERNAME_ERROR_MSG = "PLEASE ENTER A USERNAME"
PASSWORD_ERROR = "NO PASSWORD ENTERED"
PASSWORD_ERROR_MSG = "PLEASE ENTER A PASSWORD"
CHANGE_PASS = "CHANGE_PASS"
CHANGE_USERNAME = "CHANGE_USERNAME"
END_THE_VIDEO = "END_THE_VIDEO!!!"
CLIENTS = []
aes_key = None
aes_iv = None

#טיפול בלקוח פגישה קיימת/יצירת פגישה חדשה

def handle_client(client_socket):
    print("enterd handle client")
    print(client_socket.getpeername())
    private_key, public_key = encryption.create_rsa_keys(client_socket)
    print(private_key)
    print("created rsa keys")
    size = int.from_bytes(client_socket.recv(4), "big")
    keys = client_socket.recv(size)
    print("keys" + str(keys))
    print("size" + str(size))
    keys = encryption.rsa_decryption(private_key, keys).decode()
    global aes_key
    aes_key = keys.split("/")[0].encode()
    global aes_iv
    aes_iv = keys.split("/")[1].encode()
    con = True
    while con:
        size = int.from_bytes(client_socket.recv(4), "big")
        request = client_socket.recv(size)
        request = encryption.do_decrypt(aes_key, aes_iv, request).decode()
        print(request)
        if CREATE_MEETING in request:
            print("create")
            request = str(request).replace(CREATE_MEETING, "")
            request = request.split("/")
            meeting_id = request[1]
            password = request[2]
            print("meeting id " + str(meeting_id))
            flag = True
            for meeting in MEETINGS:
                if meeting.id == meeting_id:
                    msg = encryption.do_encrypt(aes_key, aes_iv, TAKEN.encode())
                    client_socket.send(len(msg).to_bytes(4, "big") + msg)
                    flag = False
                elif client_socket in meeting.clients:
                    msg = encryption.do_encrypt(aes_key, aes_iv, UNCONFIRMED.encode())
                    client_socket.send(len(msg).to_bytes(4, "big") + msg)
                    flag = False
            if flag:
                meet = Meeting(meeting_id, password)
                for c in CLIENTS:
                    if c.info_socket == client_socket:
                        if c.connected:
                            msg = encryption.do_encrypt(aes_key, aes_iv, UNCONFIRMED.encode())
                            client_socket.send(len(msg).to_bytes(4, "big") + msg)
                            flag = False
                        else:
                            meet.clients.append(c)
                            c.connected = True
                if flag:
                    MEETINGS.append(meet)
                    msg = encryption.do_encrypt(aes_key, aes_iv, CONFIRM.encode())
                    client_socket.send(len(msg).to_bytes(4, "big") + msg)
                    con = False
                else:
                    msg = encryption.do_encrypt(aes_key, aes_iv, UNCONFIRMED.encode())
                    client_socket.send(len(msg).to_bytes(4, "big") + msg)
        elif JOIN_MEETING in request:
            request = str(request).replace(JOIN_MEETING, "")
            request = request.split("/")
            meeting_id = request[1]
            password = request[2]
            print("meeting id " + str(meeting_id))
            flag = False
            client = None
            locked = False
            for c in CLIENTS:
                if c.info_socket == client_socket:
                    client = c
            if not client.connected:
                for meeting in MEETINGS:
                    if meeting.id == meeting_id and meeting.password == password:
                        if meeting.locked:
                            msg = encryption.do_encrypt(aes_key, aes_iv, LOCKED.encode())
                            client_socket.send(len(msg).to_bytes(4, "big") + msg)
                            locked = True
                        else:
                            meeting.clients.append(client)
                            client.connected = True
                            meeting.locked = True
                            flag = True
                if not locked:
                    if not flag:
                        msg = encryption.do_encrypt(aes_key, aes_iv, WRONG.encode())
                        client_socket.send(len(msg).to_bytes(4, "big") + msg)
                    else:
                        msg = encryption.do_encrypt(aes_key, aes_iv, CONFIRM.encode())
                        client_socket.send(len(msg).to_bytes(4, "big") + msg)
                        con = False
            else:
                msg = encryption.do_encrypt(aes_key, aes_iv, UNCONFIRMED.encode())
                client_socket.send(len(msg).to_bytes(4, "big") + msg)

# מטפלת בהפצת הודעות בין לקוחות

def get_msg(chat_socket, client):
    client_chat_socket, client_address = chat_socket.accept()
    for c in CLIENTS:
        print(c.address)
        if c.address == client_address[0]:
            print("change")
            c.chat_socket = client_chat_socket
    print("connected")
    while client.connected is True:
        try:
            client_name = client_chat_socket.recv(16)
            size = int.from_bytes(client_chat_socket.recv(4), "big")
            data = client_chat_socket.recv(size)
            print("the client name " + str(client_name))
            print(data)
            meet = None
            for meeting in MEETINGS:
                for client in meeting.clients:
                    if client.chat_socket == client_chat_socket:
                        meet = meeting
            for c in meet.clients:
                c.chat_socket.sendall(client_name + size.to_bytes(4, "big") + data)
            print("message sent")
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass

# מטפלת בהפצת תמונת וידאו בזמן אמת

def get_pics(client_socket, client):
    payload_size = struct.calcsize("16s I")
    data = b""
    flag = True
    while client.connected is True:
        try:
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("16s I", packed_msg_size)
            name = msg_size[0]
            msg_size = msg_size[1]
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            meet = None
            for meeting in MEETINGS:
                for client in meeting.clients:
                    if client.video_socket == client_socket:
                        meet = meeting
            if meet:
                for c in meet.clients:
                    if c.video_socket != client_socket:
                        if c.video_socket:
                            print(c.video_socket.getpeername())
                            c.video_socket.send(struct.pack("16s I", name, len(frame_data)) + frame_data)
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass

# מטפלת בהפצת המסך בין הלקוחות

def get_share_screen(sharing_socket, client):
    client_socket, client_address = sharing_socket.accept()
    for c in CLIENTS:
        if c == client:
            print("change")
            c.share_socket = client_socket
    payload_size = struct.calcsize("16s I")
    data = b""
    while client.connected is True:
        print("waiting")
        try:
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("16s I", packed_msg_size)
            name = msg_size[0]
            msg_size = msg_size[1]
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            meet = None
            for meeting in MEETINGS:
                for client in meeting.clients:
                    if client.share_socket == client_socket:
                        meet = meeting
            number = 1
            if meet:
                for c in meet.clients:
                    if c.share_socket != client_socket:
                        c.share_socket.send(struct.pack("16s I", name, len(frame_data)) + frame_data)
                        print("sent the screenshot")
                        print("client" + str(number))
                        number += 1
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass

# מטפלת בהפצת נתוני שמע

def broadcast_sound(sound_socket, data):
    meet = None
    for meeting in MEETINGS:
        for client in meeting.clients:
            if client.sound_socket == sound_socket:
                meet = meeting
    if meet:
        for client in meet.clients:
            if client.sound_socket != sound_socket:
                if client.sound_socket:
                    try:
                        client.sound_socket.send(data)
                    except socket.error:
                        sound_socket.close()

# מטפלת בקבלת נתוני שמע

def get_sound(sound_socket, client):
    while client.connected is True:
        try:
            data = sound_socket.recv(1024)
            broadcast_sound(sound_socket, data)
        except socket.error:
            sound_socket.close()

# מטפלת בסיום המפגש

def ending_meeting(end_socket, client):
    client_end_socket, client_address = end_socket.accept()
    while client.connected is True:
        try:
            size = int.from_bytes(client_end_socket.recv(4), "big")
            data = client_end_socket.recv(size)
            global aes_key, aes_iv
            request = encryption.do_decrypt(aes_key, aes_iv, data).decode()
            if END_MEETING in request:
                request = str(request).replace(END_MEETING, "")
                request = request.split("/")
                print(request)
                meeting_id = request[1]
                name = request[2]
                print("this is my name")
                name += "%" * (16 - len(name))
                print(name)
                flag = False
                for meeting in MEETINGS:
                    print(meeting.id)
                    print(meeting_id)
                    if meeting.id == meeting_id:
                        meeting.clients.remove(client)
                        meeting.locked = False
                        if not meeting.clients:
                            print("remove")
                            MEETINGS.remove(meeting)
                        else:
                            for c in meeting.clients:
                                data = encryption.do_encrypt(aes_key, aes_iv, END_THE_VIDEO.encode())
                                size = len(data)
                                name = encryption.do_encrypt(aes_key, aes_iv, name.encode())
                                c.chat_socket.sendall(name + size.to_bytes(4, "big") + data)
                                print("sent ending")
                        flag = True
                if not flag:
                    msg = encryption.do_encrypt(aes_key, aes_iv, UNCONFIRMED.encode())
                    client_end_socket.send(len(msg).to_bytes(4, "big") + msg)
                else:
                    msg = encryption.do_encrypt(aes_key, aes_iv, CONFIRM.encode())
                    client_end_socket.send(len(msg).to_bytes(4, "big") + msg)
                    client.connected = False
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass

#

def main():
    #bind- בעצם מקשר בין הIP למידע המבוקש וקושר אותו לצד של השרת
    info_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    info_socket.bind((IP, INFO_PORT))
    info_socket.listen(100)
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_socket.bind((IP, VIDEO_PORT))
    video_socket.listen(100)
    sound_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sound_socket.bind((IP, SOUND_PORT))
    sound_socket.listen(100)
    end_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_socket.bind((IP, END_PORT))
    end_socket.listen(100)
    sharing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sharing_socket.bind((IP, SHARING_PORT))
    sharing_socket.listen(100)
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket.bind((IP, CHAT_PORT))
    chat_socket.listen(100)
    while True:
        print("WAITING FOR CLIENTS")
        client_info_socket, client_address = info_socket.accept()
        client = Me_A_You_Client(client_info_socket)
        CLIENTS.append(client)
        handling_client = threading.Thread(target=handle_client, args=[client_info_socket])
        handling_client.start()
        client_socket, client_address = video_socket.accept()
        print(client_address)
        print(client_socket.getpeername()[0])
        client_sound_socket, client_address = sound_socket.accept()
        for c in CLIENTS:
            if c == client:
                c.video_socket = client_socket
                c.sound_socket = client_sound_socket
        getting_pic = threading.Thread(target=get_pics, args=[client_socket, client])
        getting_pic.start()
        getting_sound = threading.Thread(target=get_sound, args=[client_sound_socket, client])
        getting_sound.start()
        getting_share_screen = threading.Thread(target=get_share_screen, args=[sharing_socket, client])
        getting_share_screen.start()
        getting_msgs = threading.Thread(target=get_msg, args=[chat_socket, client])
        getting_msgs.start()
        ending = threading.Thread(target=ending_meeting, args=[end_socket, client])
        ending.start()

if __name__ == '__main__' :
    main()