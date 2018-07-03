"""
    SimpleSocket v0.2
    simple implementation of python socket for creating server/client based programs supporting threading.
    YES! i already know about socketserver, coming with python, but just trying make a new one, simpler!
    (for more information about socketserver check out: https://docs.python.org/3/library/socketserver.htm )
    open for any contributions, issue reporting. even if you have any idea about this package you are warmly accepted!
    just check out: https://github.com/aasmpro/simplesocket
"""

import socket
from threading import Thread


class SimpleSocket:
    def __init__(self, sock=None, host=None, port=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if sock is None else sock
        self.host = socket.gethostname() if host is None else host
        self.port = 9999 if port is None else port

    def set_host_port(self, host=None, port=None):
        self.host = host if host is not None else socket.gethostname()
        self.port = port if port is not None else 9999

    def send(self, msg, enc="UTF-8"):
        self.sock.send(msg.encode(enc))

    def receive(self, msg_len=2048, enc="UTF-8"):
        return (self.sock.recv(msg_len)).decode(enc)

    def close(self):
        self.sock.close()

    def __str__(self):
        return "Socket on {}:{}".format(self.host, self.port)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.sock == other.sock and self.host == other.host and self.port == other.port
        return False

    def __hash__(self):
        return hash((self.sock, self.host, self.port))

    @staticmethod
    def socket_from_string(string):
        host, port = None, None
        try:
            if ':' in string:
                host, port = string.split(':')[0], string.split(':')[1]
            elif string.isdigit():
                host, port = None, string
            else:
                host, port = string, None
        except Exception as exc:
            raise Warning("Can not defining Socket host and port from {}".find(string)) from exc
        return SimpleSocket(None, host, port)


class SimpleClientSocket(SimpleSocket):
    def connect(self, host=None, port=None):
        host = self.host if host is None else host
        port = self.port if port is None else port
        try:
            self.sock.connect((host, port))
        except Exception as exc:
            if host is None or port is None:
                raise RuntimeError("Server not defined.") from exc
            else:
                raise RuntimeError("Can not connect to {}:{}".format(host, port)) from exc

    def __str__(self):
        return "Client on {}:{}".format(self.host, self.port)

    def __repr__(self):
        return self.__str__()

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
        return SimpleClientSocket(None, host, port)


class SimpleServerSocket(SimpleSocket):
    def __init__(self, sock=None, host=None, port=None):
        super(SimpleServerSocket, self).__init__(sock, host, port)
        self.clients = list()
        self.received_messages = list()

    def broadcast(self, msg, enc="UTF-8"):
        for client in self.clients:
            client.send(msg, enc)

    def listen(self, host=None, port=None, max_connections=5):
        host = self.host if host is None else host
        port = self.port if port is None else port
        try:
            self.sock.bind((host, port))
            self.sock.listen(int(max_connections))
        except Exception as exc:
            raise RuntimeError("Can not listen to {}:{}".format(host, port)) from exc

    def accept(self):
        client, client_address = self.sock.accept()
        return SimpleClientSocket(sock=client, host=client_address[0], port=client_address[1])

    def accept_thread(self, thread_func, main_func=None):
        while True:
            client, client_address = self.sock.accept()
            client = SimpleClientSocket(sock=client, host=client_address[0], port=client_address[1])
            self.clients.append(client)
            if main_func is not None:
                try:
                    main_func(client, self)
                except:
                    pass
            Thread(target=thread_func, args=(client, self)).start()

    def __str__(self):
        return "Server on {}:{}".format(self.host, self.port)

    def __repr__(self):
        return self.__str__()

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
        return SimpleServerSocket(None, host, port)
