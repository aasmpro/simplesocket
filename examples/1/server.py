from simplesocket import SimpleServer
from datetime import datetime
import sys


def clients_handel(client, server):
    print("{} joined. # clients : {}".format(client, len(server.clients)))
    while True:
        try:
            cmd = client.receive()
            if cmd not in ("[Exit]", "[E]"):
                print("""{} >>> {}""".format(client, cmd))
                msg = "Error : unknown command."
                cmd = cmd.split()
                if cmd[0] == "time":
                    msg = 'time is {}'.format(datetime.now().time())
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
    server = SimpleServer.server_from_string("" if len(sys.argv) < 2 else sys.argv[1])
    print("\n\t{}\n\tStarted {}\n".format(datetime.now(), server))
    server.run(clients_handel)


if __name__ == '__main__':
    main()
