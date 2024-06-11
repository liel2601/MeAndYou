
class Meeting:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.clients = []
        self.locked = False


class Me_A_You_Client:
    def __init__(self, info_socket):
        self.video_socket = None
        self.info_socket = info_socket
        self.sound_socket = None
        self.chat_socket = None
        self.share_socket = None
        self.address = info_socket.getpeername()[0]
        self.connected = False

    def printing(self):
        return "address = " + self.address
