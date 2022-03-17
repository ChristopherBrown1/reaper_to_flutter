import reapy
from reapy import reascript_api as RPR
import socket
import threading
import advertiserSocket


# TODO: Try catch to ensure that reaper is open. If not open then continue to try

HEADER = 64
PORT = 4545
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM is UDP, SOCK_STREAM is TCP. Try SOCK_STREAM to see if it works.
s.connect(("8.8.8.8", 80)) # Gets the ip address from the google DNS. Must have an internet connection for this to work. socket.getsockname() may also work.
SERVER = s.getsockname()[0] # Could possibly use "0.0.0.0" to bind to any ip address from this server if there are multiple addresses. Only would work for a LAN.
s.close()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
print(f'Python Server address = {SERVER}')
conn = ''
project = reapy.Project()
advertiser = advertiserSocket.AdvertiserSocket()


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    print(conn.recv(64).decode(FORMAT))


def sort_data(data):

    # TODO: If connection is not established an icon should be on the tablet showing no connection symbol.
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
    elif data == "rewind":
        action_id = reapy.get_command_id(
            "40084")  # converts the action id string to an int.
        reapy.perform_action(action_id)
    elif data == "mainOnCommand":
        action_id = reapy.get_command_id("_f518c91fefc442f296feb866ca286b6a") # converts the action id string to an int.
        reapy.perform_action(action_id)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {conn} Address = {addr} connected.")
    connected = True
    advertiserThread = threading.Thread(target=advertiser.stopAdvertisingApplication)
    advertiserThread.start()
    # TODO: When connection is made a message should be sent back to the tablet to go to the start page.
    # conn.send(bytes("connection established", "utf-8"))
    while connected:
        # now we are connected to the other flutter app.
        data = conn.recv(1024).decode()
        print(data)

        if data == "exit":
            # conn.send(bytes("connection closed", "utf-8"))
            break

        sort_data(data)

    conn.close()
    advertiserThread = threading.Thread(target=advertiser.advertiseApplication)
    advertiserThread.start()

def start():
    server.listen()
    advertiserThread = threading.Thread(target=advertiser.advertiseApplication)
    advertiserThread.start()
    print(f"[LISTENING] Server is listening on {SERVER}")
    print("HEY")
    while True:
        # Accept connections from the outside

        conn, addr = server.accept()
        print("Hello")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] server is starting...")
start()
