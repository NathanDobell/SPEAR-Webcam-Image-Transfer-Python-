import socket
import threading
import cv2.aruco as aruco
import cv2
import pickle
import numpy as np
import matplotlib

##-----------------------------------------------------------------------------------------#
## CONSTANT VALUES
PORT   = 7505
SERVER = socket.gethostbyname(socket.gethostname()) 
ADDR   = (SERVER , PORT) ## basic informaton for contacting server
HEADER = 16 ## How big the header is on the incoming info
BUFFER = 100000 ## How many chars can be recived in one go
FORMAT = 'utf-8' ## Format of the bytes used
DISMES = '!END' ## Message to disconnect from server

##-----------------------------------------------------------------------------------------#
## START
def start():
    print('[SERVER] STARTING UP')
    host = socket.socket(socket.AF_INET , socket.SOCK_STREAM) ## Creates stream type server
    host.bind(ADDR) ## Binds Server to adress
    host.listen(5) ## Server listening for connections with buffer 5
    print('[SERVER] STARTUP COMPLETE')
    print(f'[SERVER] LISTENING ON {SERVER}, {PORT}')
    main_run(host)

##-----------------------------------------------------------------------------------------#
## MAIN RUN - Intakes Host Socket
def main_run(host):
    while True:
        conn , addr = host.accept() # Accepts and stores incoming conneciton
        thread = threading.Thread(target = handle_client, args= (conn, addr)) 
        thread.start() # Puts each client on own thread
        print(f'[SERVER] NEW CONNECTION : {threading.active_count()-1} ACTIVE')

##-----------------------------------------------------------------------------------------#
## HANDEL CLIENT - Intakes connection and its adrress
def handle_client(conn , addr):
    print(f'[SERVER] NEW CONNECTION AT {addr}')
    connected = True ## False to end conn

    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT) ## Checks Header for message length
        if msg_len: ## Check for no data
            msg_len = int(msg_len) 
            msg = b'' ## msg is the actual data being transfered
            while len(msg) < msg_len: ## Collects all data to msg
                msg_temp = conn.recv(msg_len-len(msg)) ## ensures all data collected
                msg += msg_temp
               
            msg = pickle.loads(msg) ## Collected Message Unloaded
            msg_type = type(msg)

            if msg_type ==  str : ## if string show in console, or Disconnecting
                if msg == DISMES:
                    print(f'[CLIENT {addr}] DISCONNECTING')
                    connected = False
                else: 
                    print(f'[CLIENT {addr}] {msg}')
            elif msg_type == np.ndarray: ## if list turn into and show image
                #print(np.shape(msg))

                aruco_dict = aruco.PredefinedDictionaryType(aruco.DICT_4X4_100)
                parameters = aruco.DetectorParameters_create()
                corners, ids, rejectedImgPoints = aruco.detectMarkers(msg,aruco_dict,parameters=parameters)
                if len(ids) == 0:
                    cv2.imshow("RECIVEDVIDEO", msg)
                else:
                    editedFrame = aruco.drawDetectedMarkers(image=msg.copy(),corners=corners,ids=ids)
                    cv2.imshow("RECIEVEDVIDEO",editedFrame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'): ## if q is pressed disconnect
                    connected = False
    conn.close()
            
start()

            

