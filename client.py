import os
import socket
import threading
from getpass import getpass

BUFFER = 1024
FORMAT = "utf-8"
PORT = 21
SERVER = ""
ADDR = ("", PORT)
isConnected = False

command_list = [
    "ascii",  #
    "binary",  #
    "bye",  #
    "cd",  #
    "close",  #
    "delete",
    "disconnect",  #
    "get",
    # "help", not required
    "ls",  #
    "open",  #
    "put",  #
    "pwd",  #
    "quit",  #
    "rename",  #
    "user",  ##
]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send(msg):
    message = msg.encode(FORMAT) + b"\r\n"
    client.sendall(message)


def voidsend(msg):
    message = msg.encode(FORMAT) + b"\r\n"
    client.sendall(message)
    print(get_resp(client), end="")


def get_resp(rsocket):
    response = b""
    while True:
        part = rsocket.recv(BUFFER)
        response += part
        if b"\r\n" in part:
            break
    return response.decode(FORMAT)


def get_mul_resp(rsocket):
    response = b""
    while True:
        part = rsocket.recv(BUFFER)
        if not part:
            break
        response += part
    return response.decode(FORMAT)


def close():
    global isConnected
    if not isConnected:
        print("Not connected.")
        return
    else:
        cmd = "QUIT"
        voidsend(cmd)
        isConnected = False


def disconnect():
    global isConnected
    if not isConnected:
        print("Not connected.")
        return
    else:
        cmd = "QUIT"
        voidsend(cmd)
        isConnected = False


def quit():
    if not isConnected:
        exit()
    else:
        cmd = "QUIT"
        voidsend(cmd)
        client.close()
        exit()


def make_socket():
    data_sock = socket.create_server((client.getsockname()[0], 0))
    host = data_sock.getsockname()[0]
    port = data_sock.getsockname()[1]
    send_port(host, port)
    return data_sock


def send_port(host, port):
    hbytes = host.split(".")
    pbytes = [repr(port // 256), repr(port % 256)]
    bytes = hbytes + pbytes
    cmd = "PORT " + ",".join(bytes)
    voidsend(cmd)
    return


def open_conn(args):
    global isConnected
    if not args == "":
        try:
            ADDR = (args, PORT)
            client.connect(ADDR)
            print(f"Connected to {args}.")
            print(get_resp(client), end="")
            ip = socket.gethostbyname(socket.gethostname())
            host = socket.gethostname()
            username = input(f"Name ({ip}:{host}): ")
            cuser = "USER " + username
            voidsend(cuser)
            passwd = getpass("Password: ")
            cpasswd = "PASS " + passwd
            voidsend(cpasswd)
            isConnected = True
        except:
            print("Connection unsucessful. Make sure the server is online.")
    else:
        addr = input("To ")
        try:
            ADDR = (addr, PORT)
            client.connect(ADDR)
            print("Connection sucessful")
            isConnected = True
        except:
            print("Connection unsucessful. Make sure the server is online.")
    return


def dir():
    cmd = "LIST"
    data_sock = make_socket()
    voidsend(cmd)
    data_conn, size = data_sock.accept()
    print(get_mul_resp(data_conn), end="")
    print(get_resp(client), end="")
    data_conn.close()
    return


def path():
    cmd = "PWD"
    voidsend(cmd)
    return


def changedir(args):
    if args == "":
        dir = input("(remote-directory) ").strip()
        cmd = "CWD " + dir
    else:
        cmd = "CWD " + args

    voidsend(cmd)


def rename(args):
    if len(args) > 1:
        from_name = args[0]
        to_name = args[1]
    elif len(args) > 0:
        from_name = args
        to_name = input("(to-name) ").strip()
    elif len(args) == 0:
        from_name = input("(from-name) ").strip()
        to_name = input("(to-name) ").strip()
    fromcmd = "RNFR " + from_name
    tocmd = "RNTO " + to_name
    send(fromcmd)
    resp = get_resp(client)
    print(resp)
    if not resp.startswith("5"):
        voidsend(tocmd)
    return


def ascii():
    cmd = "TYPE A"
    voidsend(cmd)
    return


def binary():
    cmd = "TYPE I"
    voidsend(cmd)
    return


def user(args):
    if args == "":
        username = input("(username) ").strip()
        cmd = "USER " + username
    else:
        cmd = "USER " + args

    send(cmd)
    resp = get_resp(client)
    print(resp, end="")
    if resp.startswith("5"):
        print("Login failed.")
    else:
        print("Login successful.")

        return


def put():
    localfilename = input("(local-file) ")
    remotefilename = input("(remote-file) ")
    if localfilename:
        try:
            data_sock = make_socket()
            cmd = "STOR " + remotefilename
            voidsend(cmd)

            localfile = os.path.join(os.getcwd(), localfilename)

            data_conn, size = data_sock.accept()

            with open(localfile, "rb") as file:
                data_conn.sendfile(file)
            data_conn.close()
            print(get_resp(client), end="")
        except FileNotFoundError:
            print("ftp: local: g: No such file or directory")
        except Exception:
            print("An error occurred")
    return

def get():
    remotefilename = input("(remote-file) ")
    localfilename = input("(local-file) ")
    
    if remotefilename:
        try:
            data_sock = make_socket()
            cmd = "RETR " + remotefilename
            voidsend(cmd)

            data_conn, size = data_sock.accept()
            print(get_mul_resp,end='')

            data_conn.close()
        except Exception as ex:
            print(ex)

    pass


def handle_command(cmd, args):

    if cmd == "quit":
        quit()
    elif cmd == "open":
        open_conn(args)
    elif cmd == "bye":
        quit()
    elif cmd == "ascii":
        ascii()
    elif cmd == "binary":
        binary()
    elif cmd == "disconnect":
        disconnect()
    elif cmd == "close":
        close()
    elif cmd == "ls":
        dir()
    elif cmd == "pwd":
        path()
    elif cmd == "cd":
        changedir(args)
    elif cmd == "rename":
        rename(args)
    elif cmd == "user":
        user(args)
    elif cmd == "put":
        put()
    elif cmd == "get":
        get()
    return


while True:
    command_input = input("ftp> ").strip()  # Remove leading and trailing whitespaces
    # Case 4: Empty input
    if not command_input:
        continue

    command_parts = command_input.split(" ")
    cmd = command_parts[0]
    args = " ".join(command_parts[1:]) if len(command_parts) > 1 else ""

    matched_commands = []

    for command in command_list:
        if cmd == command:
            # Case 1: Full match
            handle_command(command, args)
            break
        elif command.startswith(cmd):
            matched_commands.append(command)
    else:
        # Case 2: Ambiguous command
        if len(matched_commands) > 1:
            print("Ambiguous command.")
        # Case 3: Abbreviated match
        elif len(matched_commands) == 1:
            handle_command(command, args)
        else:
            # Case 3 (continued): No match found
            print("Invalid command.")
