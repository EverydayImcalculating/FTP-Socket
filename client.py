import socket
import threading

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
    "close", #
    "delete",
    "disconnect",  #
    "get",
    # "help", not required
    "ls",
    "open",  #
    "put",
    "pwd",
    "quit",  #
    "rename",
    "user",
]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send(msg):
    message = msg.encode(FORMAT) + b"\r\n"
    client.sendall(message)
    print(receive_response(), end="")


def receive_response():
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
        send("QUIT")
        isConnected = False


def disconnect():
    global isConnected
    if not isConnected:
        print("Not connected.")
        return
    else:
        send("QUIT")
        isConnected = False


def bye():
    if not isConnected:
        exit()
    else:
        send("QUIT")
        client.close()
        exit()


def quit():
    if not isConnected:
        exit()
    else:
        send("QUIT")
        client.close()
        exit()


def open(args):
    global isConnected
    if not args == "":
        try:
            ADDR = (args, PORT)
            client.connect(ADDR)
            print(f"Connected to {args}.")
            print(receive_response(), end="")
            ip = socket.gethostbyname(socket.gethostname())
            host = socket.gethostname()
            username = input(f"Name ({ip}:{host}): ")
            cuser = "USER " + username
            send(cuser)
            passwd = input("Password: ")
            cpasswd = "PASS " + passwd
            send(cpasswd)
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


def handle_command(cmd, args):

    if cmd == "quit":
        quit()
    elif cmd == "open":
        open(args)
    elif cmd == "bye":
        bye()
    elif cmd == "ascii":
        send("TYPE A")
    elif cmd == "binary":
        send("TYPE I")
    elif cmd == "disconnect":
        disconnect()
    elif cmd == "close":
        close()
    return


while True:
    command_input = input("ftp> ")  # Remove leading and trailing whitespaces
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
