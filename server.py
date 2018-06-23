from SimpleSocket import SimpleServerSocket
import datetime


def main():
    server = SimpleServerSocket.socket_from_sys()
    print("""
    {}
    server started on {}:{}
    """.format(datetime.datetime.now(), server.host, server.port))
    server.listen()

    while True:
        client = server.accept()
        try:
            cmd = client.receive()
            if cmd:
                print("""client {}:{} >>> {}""".format(client.host, client.port, cmd))
                msg = "Error : unknown command."
                cmd = cmd.split()

                if cmd[0] == "time":
                    msg = 'time is {}'.format(datetime.datetime.now().time())

                client.send(msg)

        except:
            pass

        client.close()


if __name__ == '__main__':
    main()
