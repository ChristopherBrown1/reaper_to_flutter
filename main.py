import reapy
from reapy import reascript_api as RPR


import socket
import threading

HEADER = 64
PORT = 4545
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
SERVER = s.getsockname()[0]
s.close()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
print(f'Python Server address = {SERVER}')
conn = ''
project = reapy.Project()


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    print(conn.recv(64).decode(FORMAT))


def sort_data(data):

    if data == "data":
        d = data
        conn.send(bytes(d, "utf-8"))
    elif data == "reaper hello":
        reapy.print('Hello from flutter')
    elif data == "play":
        project.play()
    elif data == "pause":
        project.pause()
    elif data == "stop":
        project.stop()
    elif data == "mainOnCommand":
        action_id = reapy.get_command_id("_f518c91fefc442f296feb866ca286b6a") # converts the action id string to an int.
        reapy.perform_action(action_id)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {conn} Address = {addr} connected.")
    connected = True
    while connected:
        # now our endpoint knows about the OTHER endpoint.
        data = conn.recv(1024).decode()
        print(data)

        if data == "exit":
            break

        sort_data(data)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] server is starting...")
start()
