import socket
import threading

BUFFER = 1024
FORMAT = "utf-8"
PORT = 21
SERVER = ""
ADDR = ("", PORT)

isConnected = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b" " * (BUFFER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(2048).decode(FORMAT))w


def quit(status):
    client.send(b"quit")
    # Wait for server go-ahead
    resp = client.recv(BUFFER)
    client.close()
    print("Server connection ended")


def open(cmd, args):
    if not args == "":
        print("Sending server request...")
        try:
            ADDR = (args, PORT)
            client.connect(ADDR)
            print("Connection sucessful")
        except:
            print("Connection unsucessful. Make sure the server is online.")
    else:
        addr = input("To ")
        print(addr)

    pass


def handle_command(cmd, args = None, status = None):

    if cmd == "quit":
        quit()
    elif cmd == "open":
        open(cmd, args)
    pass


while True:
    command_list = [
        "ascii",
        "binary",
        "bye",
        "cd",
        "close",
        "delete",
        "disconnect",
        "get",
        "help",
        "ls",
        "open",
        "put",
        "pwd",
        "quit",
        "rename",
        "user",
    ]
    command_input = input("ftp> ").split(" ")  # Remove leading and trailing whitespaces

    print(command_input)

    # Case 4: Empty input
    if not command_input:
        continue

    cmd, args = command_input[0], ""

    if len(command_input) > 1:
        args = command_input[1]

    matched_commands = []
    # Check for full matches, partial matches, and ambiguous matches
    for command in command_list:
        if cmd == command:
            # Case 1: Full match
            print("Command executed:", command)
            handle_command(command, args)
            break
        elif command.startswith(cmd):
            matched_commands.append(command)
    else:
        # Case 2: Ambiguous command
        if len(matched_commands) > 1:
            print("Ambiguous command. Possible matches:")
            for command in matched_commands:
                print(command)
        # Case 3: Abbreviated match
        elif len(matched_commands) == 1:
            print("Command executed:", matched_commands[0])
        else:
            # Case 3 (continued): No match found
            print("Invalid command.")
