from simplesocket import SimpleClient
import sys


def client_handle(client):
    while True:
        try:
            cmd = input("command >>> ")
            client.send(cmd)
            if cmd in ("[Exit]", "[E]"):
                break
            msg = client.receive()
            print(msg)
        except:
            pass
    client.close()


def main():
    client = SimpleClient.client_from_string("" if len(sys.argv) < 2 else sys.argv[1])
    print("connecting to {}:{} ...".format(client.host, client.port))
    client.run(client_handle)


if __name__ == '__main__':
    main()
