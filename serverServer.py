import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)

def handle_client(connection:socket.socket,address):
    connected = True
    while connected:
        messageLength = connection.recv(64).decode("utf-8")
        if messageLength:
            message = connection.recv(int(messageLength)).decode("utf-8")            
            print("\n{}".format(message))

            if message == "END":
                connected = False


    print("[ENDING CONNECTION]: {}".format(address))
    return



def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENTING] on port {}\n".format(PORT))

    while True:
        connection, address = server.accept()
        print("[UPDATE] New Connection: {}".format(address))
        thread = threading.Thread(target=handle_client,args=[connection,address])
        thread.start()

start_server()