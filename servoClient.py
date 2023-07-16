import socket
import keyboard
import random

PORT = 5050
SERVER = "172.20.10.2"
ADDR = (SERVER,PORT)


def start(speed:int):
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
            message = "-{}/x".format(speed)
        elif input == "left":
            message = "+{}/x".format(speed)
        elif input == "up":
            message = "+{}/y".format(speed)
        elif input == "down":
            message = "-{}/y".format(speed)
        else:
            message = ""

        if message != "":    
            print("Message:{} [SENT]\n".format(message))
            message = message.encode('utf-8')
            messageLength = str(len(message)).encode('utf-8')
            messageLength += b' ' * (64 - len(messageLength))
            client.send(messageLength)
            client.send(message)


start(speed=2.5) #speed should be in angle measures



