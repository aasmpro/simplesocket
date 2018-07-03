from SimpleSocket import SimpleClientSocket
from threading import Thread
import atexit
import sys


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
    client = SimpleClientSocket.client_from_string("" if len(sys.argv) < 2 else sys.argv[1])
    print("connecting to {}:{} ...".format(client.host, client.port))
    client.connect()
    receiver_thread = Thread(target=client_handle, args=(client,))
    receiver_thread.start()
    atexit.register(at_exit, client=client)


def at_exit(client):
    try:
        client.send("[E]")
        client.close()
    except:
        pass


if __name__ == '__main__':
    main()
