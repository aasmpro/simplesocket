from SimpleSocket import SimpleServerSocket
import datetime
from threading import Thread


def main_func(client, server):
    print("client {}:{} joined. # clients : {}".format(client.host, client.port, len(server.clients)))


def clients_handel(client, server):
    while True:
        try:
            cmd = client.receive()
            if cmd not in ("[Exit]", "[E]"):
                print("""client {}:{} >>> {}""".format(client.host, client.port, cmd))
                msg = "Error : unknown command."
                cmd = cmd.split()
                if cmd[0] == "time":
                    msg = 'time is {}'.format(datetime.datetime.now().time())
                    client.send(msg)
                elif cmd[0] == "[ALL]":
                    server.broadcast(" ".join(cmd[1:]))
                else:
                    client.send(msg)
            else:
                client.close()
                server.clients.remove(client)
                print("""client {}:{} left. # clients : {}""".format(client.host, client.port, len(server.clients)))
                break
        except:
            pass


def main():
    server = SimpleServerSocket.socket_from_sys()
    print("\n\t{}\n\tserver started on {}:{}\n".format(datetime.datetime.now(), server.host, server.port))
    server.listen()
    accept_thread = Thread(server.accept_thread(clients_handel, main_func))
    accept_thread.start()
    accept_thread.join()


if __name__ == '__main__':
    main()
