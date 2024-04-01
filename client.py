import socket
import threading

BUFFER = 1024
FORMAT = "utf-8"
PORT = 5050
SERVER = "127.0.0.2"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)


# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b" " * (BUFFER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(2048).decode(FORMAT))

# send("HEllo")
# send(DISCONNECT_MESSAGE)

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
    quit_command = ["bye", "quit"]

    command_input = input("ftp> ").lower()

    if not command_input:
        continue

    if command_input in quit_command:
        print()
        break
        
    matched_commands = []
    # Check for full matches, partial matches, and ambiguous matches
    for command in command_list:
        if command_input == command:
            print("Command executed:", command)  # Case 1: Full match
            break
        elif command.startswith(command_input):
            matched_commands.append(command)
    else:
        # Case 2: Ambiguous command
        if len(matched_commands) > 1:
            print("Ambiguous command.")
        # Case 3: Abbreviated match
        elif len(matched_commands) == 1:
            print("Command executed:", matched_commands[0])
        else:
            # Case 3 (continued): No match found
            print("Invalid command.")
