"""
    created by aa.smpro@gmail.com
"""
import socket
import datetime
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

server_socket.bind((host, int(port)))
server_socket.listen()
print("""
{}
server started on {}:{}
""".format(datetime.datetime.now(), host, port))

while True:
    client_socket, addr = server_socket.accept()
    try:
        cmd = (client_socket.recv(1024)).decode('ascii')
        if cmd:
            print("""client {}:{} >>> {}""".format(addr[0], addr[1], cmd))
            msg = "Error : unknown command."
            cmd = cmd.split()

            if cmd[0] == "time":
                msg = 'time is {}'.format(datetime.datetime.now().time())

            client_socket.send(msg.encode('ascii'))

    except:
        pass

    client_socket.close()
