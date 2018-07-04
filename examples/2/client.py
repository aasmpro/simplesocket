from simplesocket import SimpleClient
import time
import sys


def client_handle(client):
    retries = 0
    while True:
        try:
            msg = client.receive()
            print(msg)
            if msg == "closing connection.":
                break
            if msg == "input sum of the numbers : ":
                sum_of_numbers = input()
                client.send(sum_of_numbers)

        except Exception as ex:
            if str(ex).__contains__("A request to send or receive data was disallowed") \
                    or str(ex).__contains__("An existing connection was forcibly closed by the remote host"):
                print("Server is not online, closing connection.")
                break
            print("something went wrong...\n\tError : {}".format(ex))
            retries += 1
            time.sleep(1)
            if retries == 10:
                print("closing connection.")
                break
            pass

    client.close()


def main():
    client = SimpleClient.client_from_string("" if len(sys.argv) < 2 else sys.argv[1])
    print("connecting to {}:{} ...".format(client.host, client.port))
    client.run(client_handle)


if __name__ == '__main__':
    main()
