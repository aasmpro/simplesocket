from SimpleSocket import SimpleClientSocket
from threading import Thread
import atexit


def client_handle(client):
    while True:
        try:
            cmd = input("command >>> ")
            if cmd in ("[Exit]", "[E]"):
                break
            client.send(cmd)
            msg = client.receive()
            print(msg)

        except:
            pass

        client.send("[E]")
        client.close()


def main():
    client = SimpleClientSocket.socket_from_sys()
    print("connecting to {}:{} ...".format(client.host, client.port))
    client.connect()
    receiver_thread = Thread(target=client_handle, args=(client,))
    receiver_thread.start()
    atexit.register(at_exit, client=client)


def at_exit(client):
    client.send("[E]")
    client.close()


if __name__ == '__main__':
    main()
