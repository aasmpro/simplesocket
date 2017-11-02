"""
    created by aa.smpro@gmail.com
"""
import socket
import sys

host = socket.gethostname()
port = 9999

try:
    if ':' in sys.argv[1]:
        host = (sys.argv[1]).split(':')[0]
        port = (sys.argv[1]).split(':')[1]
    elif (sys.argv[1]).isdigit():
        port = sys.argv[1]
    else:
        host = sys.argv[1]
except:
    try:
        if sys.argv[1]:
            print("Wrong host/port format.")
    except:
        pass

print("connecting to {}:{} ...".format(host, port))


def set_server(host, port):
    print("""server on {}:{} is offline. set new server address. blank will keep current data.""".format(host, port))
    hostt = input("host >>> ")
    portt = input("port >>> ")
    if hostt: host = hostt
    if portt: port = portt
    return host, port


while True:
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, int(port)))

        try:
            cmd = input("command >>> ")
            if cmd == "exit": break
            server_socket.send(str(cmd).encode('ascii'))
            msg = server_socket.recv(1024)
            print(msg.decode('ascii'))

        except:
            pass

        server_socket.close()
    except:
        host, port = set_server(host, port)
        print("connecting to {}:{} ...".format(host, port))
