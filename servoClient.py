import socket
import keyboard

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)


def start():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)

    connected = True
    print("\nListening for input:")
    message="start"
    while connected:
        input = keyboard.read_key()
        if input=="k":
            message = "END"
            connected = False
        elif input == "right":
            message = "-45/x"
        elif input == "left":
            message = "+45/x"
        elif input == "up":
            message = "+45/y"
        elif input == "down":
            message = "-45/y"
        else:
            message = ""

        if message != "":    
            print("Message:{}\n".format(message))
            message = message.encode('utf-8')
            messageLength = str(len(message)).encode('utf-8')
            messageLength += b' ' * (64 - len(messageLength))
            client.send(messageLength)
            client.send(message)
            print("[MESSAGE SENT]")

start()


