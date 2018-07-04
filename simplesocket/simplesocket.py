from abc import ABC
import socket as sck
from threading import Thread
from datetime import datetime


class SimpleSocket(ABC):
    def __init__(self, socket=None, host=None, port=None):
        self.socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM) if socket is None else socket
        self.host = sck.gethostname() if host is None else host
        self.port = 9999 if port is None else port
        self.thread = None

    def set_host_port(self, host=None, port=None):
        self.host = host if host is not None else sck.gethostname()
        self.port = port if port is not None else 9999

    def close(self):
        self.socket.close()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.socket == other.socket and self.host == other.host and self.port == other.port
        return False

    def __hash__(self):
        return hash((self.socket, self.host, self.port))


class SimpleClient(SimpleSocket):
    def __init__(self, socket=None, host=None, port=None):
        super(SimpleClient, self).__init__(socket, host, port)
        self.save_messages = False
        self.sent_messages = list()
        self.received_messages = list()

    def send(self, msg, enc="UTF-8"):
        if self.save_messages:
            self.sent_messages.append([msg, enc, datetime.now()])
        self.socket.send(msg.encode(enc))

    def receive(self, msg_len=2048, enc="UTF-8"):
        msg = self.socket.recv(msg_len)
        if self.save_messages:
            self.received_messages.append([msg, enc, datetime.now()])
        return msg.decode(enc)

    def connect(self, host=None, port=None):
        host = self.host if host is None else host
        port = self.port if port is None else port
        try:
            self.socket.connect((host, port))
        except Exception as exc:
            if host is None or port is None:
                raise RuntimeError("Server not defined.") from exc
            else:
                raise RuntimeError("Can not connect to {}:{}".format(host, port)) from exc

    def run(self, func, host=None, port=None):
        self.connect(host, port)
        self.thread = Thread(target=func, args=(self,))
        self.thread.start()

    def __str__(self):
        return "Client on {}:{}".format(self.host, self.port)

    @staticmethod
    def client_from_string(string):
        host, port = None, None
        try:
            if ':' in string:
                host, port = string.split(':')[0], string.split(':')[1]
            elif string.isdigit():
                host, port = None, string
            elif '.' in string:
                host, port = string, None
        except Exception as exc:
            raise Warning("Can not defining Client host and port from {}".format(string)) from exc
        return SimpleClient(None, host, port)


class SimpleServer(SimpleSocket):
    def __init__(self, socket=None, host=None, port=None):
        super(SimpleServer, self).__init__(socket, host, port)
        self.clients = list()

    def broadcast(self, msg, enc="UTF-8"):
        for client in self.clients:
            client.send(msg, enc)

    def listen(self, max_connections=5, host=None, port=None):
        host = self.host if host is None else host
        port = self.port if port is None else port
        try:
            self.socket.bind((host, port))
            self.socket.listen(int(max_connections))
        except Exception as exc:
            raise RuntimeError("Can not listen to {}:{}".format(host, port)) from exc

    def accept(self):
        client, client_address = self.socket.accept()
        return SimpleClient(socket=client, host=client_address[0], port=client_address[1])

    def accept_thread(self, func):
        while True:
            client = self.accept()
            self.clients.append(client)
            Thread(target=func, args=(client, self)).start()

    def run(self, func, max_connections=5, host=None, port=None):
        self.listen(max_connections, host, port)
        self.thread = Thread(self.accept_thread(func))
        self.thread.start()
        self.thread.join()

    def __str__(self):
        return "Server on {}:{}".format(self.host, self.port)

    @staticmethod
    def server_from_string(string):
        host, port = None, None
        try:
            if ':' in string:
                host, port = string.split(':')[0], string.split(':')[1]
            elif string.isdigit():
                host, port = None, string
            elif '.' in string:
                host, port = string, None
        except Exception as exc:
            raise Warning("Can not defining Server host and port from {}".format(string)) from exc
        return SimpleServer(None, host, port)
