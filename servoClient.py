import socket
import keyboard
import random

PORT = 5050
SERVER = "172.20.10.2"
ADDR = (SERVER,PORT)


def start():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)

    connected = True
    print("\nListening for input:")
    message="start"
    #using to detect duplicate messages
    while connected:
        input = keyboard.read_key()
        if input=="k":
            message = "END"
            connected = False
        elif input == "right":
            message = "-5/x"
        elif input == "left":
            message = "+5/x"
        elif input == "up":
            message = "+5/y"
        elif input == "down":
            message = "-5/y"
        else:
            message = ""

        if message != "":    
            print("Message:{} [SENT]\n".format(message))
            message = message.encode('utf-8')
            messageLength = str(len(message)).encode('utf-8')
            messageLength += b' ' * (64 - len(messageLength))
            client.send(messageLength)
            client.send(message)


start()



