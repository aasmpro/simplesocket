from simplesocket import SimpleServer
import datetime
from random import randint
import time
import sys

random_list = list()
sent_data, received_data = dict(), dict()


def set_random_list():
    global random_list, sent_data, received_data
    received_data.clear()
    sent_data.clear()
    random_list = [randint(0, 100) for i in range(100)]


def clients_handel(client, server):
    global received_data, sent_data
    print("client {}:{} joined. # clients : {}".format(client.host, client.port, len(server.clients)))
    server.broadcast("{} clients are joined.".format(len(server.clients)))
    if len(server.clients) == 5:
        print("5 clients are connected, sending data to clients :\n")
    end = False
    getting_input = False
    sending_data = True
    print_received = False
    while True:
        try:
            if end is True:
                client.send("closing connection.")
                client.close()
                server.clients.remove(client)
                print("""client {}:{} left. # clients : {}""".format(client.host, client.port, len(server.clients)))
                break

            elif len(received_data) == 5 and print_received:
                print_received = False
                msg = "received answers are : {} = {}".format(" + ".join(str(i) for i in received_data.values()),
                                                              sum(received_data.values()))
                print("5 answers received\n{}".format(msg))
                print("closing clients connections.")
                client.send(msg)
                end = True

            elif len(server.clients) == 5 and sending_data:
                i = server.clients.index(client) * 20
                client.send("numbers to sum =>")
                client.send("\n{}\n".format(random_list[i:i + 20]))
                sent_data.update({client: random_list[i:i + 20]})
                print("to {} :\n{}".format(str(client), random_list[i:i + 20]))
                getting_input = True
                sending_data = False

            elif len(server.clients) == 5 and getting_input:
                msg = "input sum of the numbers : "
                client.send(msg)
                cmd = client.receive()
                try:
                    cmd = int(cmd)
                except:
                    cmd = 0

                received_data.update({client: cmd})
                total_sum = 0
                for i in sent_data[client]:
                    total_sum += i
                msg = "great! answer is correct.\nwaiting for others to answer..."
                if total_sum != cmd:
                    msg = "right answer is {}.\nwaiting for others to answer...".format(total_sum)
                client.send(msg)
                getting_input = False
                print("{} answered {}, {}.".format(str(client),
                                                   cmd,
                                                   "answer is right." if cmd == total_sum
                                                   else "the right answer is " + str(total_sum)))
                print_received = True

        except Exception as ex:
            if str(ex).__contains__("An existing connection was forcibly closed by the remote host"):
                client.close()
                server.clients.remove(client)
                print("""client {}:{} left. # clients : {}""".format(client.host, client.port, len(server.clients)))
                break

            print("{} >>> something went wrong...\n\tError : {}".format(client, ex))
            print("{} data >>>\n{}\n{} ".format(client, received_data,
                                                "End:{}, G_Input:{}, S_Data:{}, P_Received:{}".format(end,
                                                                                                      getting_input,
                                                                                                      sending_data,
                                                                                                      print_received)))
            time.sleep(2)
            pass


def main():
    set_random_list()
    server = SimpleServer.server_from_string("" if len(sys.argv) < 2 else sys.argv[1])
    print("\n\t{}\n\t{}\n".format(datetime.datetime.now(), str(server)))
    server.run(clients_handel, 10)


if __name__ == '__main__':
    main()
