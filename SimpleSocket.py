import socket
import sys
from threading import Thread


class SimpleSocket:
    def __init__(self, sock=None, host=None, port=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        if host is None:
            self.host = socket.gethostname()
        else:
            self.host = host

        if port is None:
            self.port = 9999
        else:
            self.port = port

    def set_host_port(self, host=None, port=None):
        if host is None:
            self.host = socket.gethostname()
        else:
            self.host = host

        if port is None:
            self.port = 9999
        else:
            self.port = port

    def send(self, msg, enc="UTF-8"):
        self.sock.send(msg.encode(enc))

    def receive(self, msg_len=2048, enc="UTF-8"):
        return (self.sock.recv(msg_len)).decode(enc)

    def __str__(self):
        return "socket on {}:{}".format(self.host, self.port)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.sock == other.sock and self.host == other.host and self.port == other.port
        return False

    @staticmethod
    def socket_from_sys():
        try:
            if ':' in sys.argv[1]:
                host, port = (sys.argv[1]).split(':')[0], (sys.argv[1]).split(':')[1]
            elif (sys.argv[1]).isdigit():
                host, port = None, sys.argv[1]
            else:
                host, port = sys.argv[1], None
        except:
            host, port = None, None

        return SimpleSocket(sock=None, host=host, port=port)


class SimpleClientSocket(SimpleSocket):
    def connect(self, host=None, port=None):
        host = self.host if host is None else host
        port = self.port if port is None else port
        try:
            self.sock.connect((host, port))
        except:
            return "can not connect to: {}:{}".format(host, port)

    def close(self):
        self.sock.close()

    @staticmethod
    def socket_from_sys():
        try:
            if ':' in sys.argv[1]:
                host, port = (sys.argv[1]).split(':')[0], (sys.argv[1]).split(':')[1]
            elif (sys.argv[1]).isdigit():
                host, port = None, sys.argv[1]
            else:
                host, port = sys.argv[1], None
        except:
            host, port = None, None

        return SimpleClientSocket(sock=None, host=host, port=port)


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
        except:
            return "can not listen to: {}:{}".format(host, port)

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

    @staticmethod
    def socket_from_sys():
        try:
            if ':' in sys.argv[1]:
                host, port = (sys.argv[1]).split(':')[0], (sys.argv[1]).split(':')[1]
            elif (sys.argv[1]).isdigit():
                host, port = None, sys.argv[1]
            else:
                host, port = sys.argv[1], None
        except:
            host, port = None, None

        return SimpleServerSocket(sock=None, host=host, port=port)
