from SimpleSocket import SimpleServerSocket
import datetime
from threading import Thread
import sys


def main_func(client, server):
    print("{} joined. # clients : {}".format(client, len(server.clients)))
    print(server.clients)


def clients_handel(client, server):
    while True:
        try:
            cmd = client.receive()
            if cmd not in ("[Exit]", "[E]"):
                print("""{} >>> {}""".format(client, cmd))
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
                print("""{} left. #Clients : {}""".format(client, len(server.clients)))
                break
        except:
            pass


def main():
    server = SimpleServerSocket.server_from_string("" if len(sys.argv) < 2 else sys.argv[1])
    print("\n\t{}\n\tStarted {}\n".format(datetime.datetime.now(), server))
    server.listen()
    accept_thread = Thread(server.accept_thread(clients_handel, main_func))
    accept_thread.start()
    accept_thread.join()


if __name__ == '__main__':
    main()
