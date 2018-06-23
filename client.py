from SimpleSocket import SimpleClientSocket


def main():
    client = SimpleClientSocket.socket_from_sys()
    print("connecting to {}:{} ...".format(client.host, client.port))
    host, port = client.host, client.port
    while True:
        client = SimpleClientSocket(sock=None, host=host, port=port)
        client.connect()
        try:
            cmd = input("command >>> ")
            if cmd == "exit": break
            client.send(cmd)
            msg = client.receive()
            print(msg)

        except:
            pass

        client.close()


if __name__ == '__main__':
    main()
