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
    "cd",
    "close",  #
    "delete",
    "disconnect",  #
    "get",
    # "help", not required
    "ls",
    "open",  #
    "put",
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
    print(get_resp(), end="")


def get_resp():
    response = b""
    while True:
        part = client.recv(BUFFER)
        response += part
        if b"\r\n" in part:
            break
    return response.decode(FORMAT)


def close():
    global isConnected
    if not isConnected:
        print("Not connected.")
        return
    else:
        voidsend("QUIT")
        isConnected = False


def disconnect():
    global isConnected
    if not isConnected:
        print("Not connected.")
        return
    else:
        voidsend("QUIT")
        isConnected = False


def quit():
    if not isConnected:
        exit()
    else:
        voidsend("QUIT")
        client.close()
        exit()


def open(args):
    global isConnected
    if not args == "":
        try:
            ADDR = (args, PORT)
            client.connect(ADDR)
            print(f"Connected to {args}.")
            print(get_resp(), end="")
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
    sock = socket.create_server(("127.0.0.1", 0))
    port = sock.getsockname()[1]  # Get proper port
    host = sock.getsockname()[0]  # Get proper host
    hbytes = host.split(".")
    pbytes = [repr(port // 256), repr(port % 256)]
    bytes = hbytes + pbytes
    port = "PORT " + ",".join(bytes)
    send(port)
    send(cmd)
    return


def path():
    voidsend("PWD")
    return


def changedir(args):
    if args == "":
        dir = input("(remote-directory) ").strip()
        cmd = "CWD " + dir
    else:
        cmd = "CWD " + args

    voidsend(cmd)


def rename(args):
    from_name = input("(from-name) ").strip()
    to_name = input("(to-name) ").strip()
    fromcmd = "RNFR " + from_name
    tocmd = "RNTO " + to_name
    voidsend(fromcmd)
    voidsend(tocmd)
    return


def ascii():
    voidsend("TYPE A")
    return


def binary():
    voidsend("TYPE I")
    return


def user(args):
    if args == "":
        username = input("(username) ").strip()
        cmd = "USER " + username
    else:
        cmd = "USER " + args

    send(cmd)
    resp = get_resp()
    print(resp, end="")
    if resp.startswith("5"):
        print("Login failed.")
    else:
        print("Login successful.")

        return


def handle_command(cmd, args):

    if cmd == "quit":
        quit()
    elif cmd == "open":
        open(args)
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
        rename()
    elif cmd == "user":
        user()
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
