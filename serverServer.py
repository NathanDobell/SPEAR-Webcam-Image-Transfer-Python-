import socket
import threading
from piservo import Servo

PORT = 5050
SERVER = "0.0.0.0"
ADDR = (SERVER,PORT)

servo_x = Servo(12)
servo_y = Servo(13)
servo_x_angle = 0
servo_y_angle = 0

def reset_servos():
    """
    Used to reset the servo angles to 0 for each
    """
    servo_x.write(servo_x_angle)
    servo_y.write(servo_y_angle)

def send_servo_signal(message:str):
    messageList = message.split("/") #splits on the "/" to give the angle change in [0] and in axis in [1]
    angle_change = int(messageList[0])
    match messageList[1]:
        case "x":
            servo_x_angle += angle_change
            servo_x.write(servo_x_angle)
        case "y":
            servo_y_angle += angle_change
            servo_y.write(servo_y_angle)
    print("Message recieved")
    return

def handle_client(connection:socket.socket,address):
    connected = True
    while connected:
        messageLength = connection.recv(64).decode("utf-8")
        if messageLength:
            message = connection.recv(int(messageLength)).decode("utf-8")            
            print("\nSending {} to send_servo_signal()".format(message))
            send_servo_signal(message)
            if message == "END":
                connected = False


    print("[ENDING CONNECTION]: {}".format(address))
    connection.close()
    return



def start_server():
    reset_servos()
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
