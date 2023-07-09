import socket
import cv2
import pickle
import numpy as np
#import matplotlib

##-----------------------------------------------------------------------------------------#
## CONSTANT VALUES
PORT   = 7505
#SERVER = '10.0.0.145' ## ez adress switch
SERVER = socket.gethostbyname(socket.gethostname())
ADDR   = (SERVER , PORT) ## basic informaton for contacting server
HEADER = 16 ## How big the header is on the incoming info
BUFFER = 100000 ## How many chars can be recived in one go
FORMAT = 'utf-8' ## Format of the bytes used
DISMES = '!END' ## Message to disconnect from server

SD  = (480  , 640 )
HD  = (720  , 1280)
FHD = (1080 , 1920) ## STANDARD MONITOR
QHD = (1440 , 2560) ## NOT WORK
UHD = (2160 , 3840) ## NOT WORK

REZ = FHD

CAMID = 0 ## ID of camera, depends on how many devices you have

##-----------------------------------------------------------------------------------------#
## START
def start():
    print('[CLIENT] STARTING UP')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f'[CLIENT] CONNECTED TO {SERVER}, {PORT}')
    camera = cam_set(CAMID, REZ, client)
    video_send(camera , client)



##-----------------------------------------------------------------------------------------#
## CAM SET - Intakes Camera ID and Tuples rez (y,x), returns camera for cv2
def cam_set(camID, rez, client):
    print(f'[CLIENT] Linking Camera #{camID}')
    sendData(client, (f'Linking Camera #{camID}'))
    camera = cv2.VideoCapture(camID)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, rez[0])
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, rez[1])
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    print(f'[CLIENT] Camera #{camID} set at {rez[0]} x {rez[1]}')
    return camera

##-----------------------------------------------------------------------------------------#
## VIDEOSEND - Intakes a camera and a server connection
def video_send(camera , client):
    while camera.isOpened():
        img, frame = camera.read()
        if img == True:
            sendData(client, frame)            


##-----------------------------------------------------------------------------------------#
## SEND - Intakes data and sends to server
def sendData(client , msg):
    msg = pickle.dumps(msg)
    msg_len = str(len(msg)).encode(FORMAT)
    msg_len += b' ' * (HEADER - len(msg_len))
    client.send(msg_len)
    client.send(msg)

start()