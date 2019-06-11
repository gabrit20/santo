import picamera
import picamera.array
import cv2
import math
import serial

import numpy.linalg as np



import threading
import soundfiles
import random
import time
from settings import *




CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
color = (15,15,15)
prev_x = 160
prev_y = 120
memoriaC=0





def cameraRun(ser,cascade):
        global prev_x
        global prev_y
        global CAMERA_WIDTH
        global CAMERA_HEIGHT
        global memoriaC

        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
                while True:        
                        if (True ): #state=="enquiry"
                        #elif (state=="camera"):
                                        
                                # stream.arrayにBGRの順で映像データを格納
                                camera.capture(stream, 'bgr', use_video_port=True)
                                # 映像データをグレースケール画像grayに変換
                                gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
                                # grayから顔を探す
                                facerect = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2, minSize=(30,30), maxSize=(150,150))

                                if len(facerect) > 0:
                                    # 複数見つかった顔のうち、以前の顔の位置に最も近いものを探す
                                    mindist = 320+240
                                    minindx = 0
                                    indx = 0
                                    for rect in facerect:
                                        dist = math.fabs(rect[0]+rect[2]/2-prev_x) + math.fabs(rect[1]+rect[3]/2-prev_y)
                                        if dist < mindist:
                                                mindist = dist
                                                minindx = indx
                                        indx += 1

                                    # 現在の顔の位置
                                    face_x = facerect[minindx][0]+facerect[minindx][2]/2
                                    face_y = facerect[minindx][1]+facerect[minindx][3]/2

                                    # 元の画像(system.array)上の、顔がある位置に赤い四角を描画
                                    cv2.rectangle(stream.array, tuple(facerect[minindx][0:2]),tuple(facerect[minindx][0:2]+facerect[minindx][2:4]), (0,0,255), thickness=2)
                                    prev_x = face_x
                                    prev_y = face_y
                                    real_x = CAMERA_WIDTH - face_x
                                    real_y = CAMERA_HEIGHT - face_y
                                    print ("(%d,%d)" % (real_x,real_y))
                                    if (real_y < 80):
                                                if (real_x<110):
                                                        coordenada=1
                                                        if (memoriaC!=coordenada):
                                                                    print ("1")
                                                                    ser.write("1")
                ##                                        if (standby=="Y"):
                ##                                                    cambio="B"
                                                        #print ser.read()
                                                elif (real_x>210):
                                                        coordenada=3
                                                        if (memoriaC!=coordenada):
                                                                    print ("3")
                                                                    ser.write("3")
                ##                                      if (standby=="Y"):
                ##                                              cambio="B"
                                                        #print ser.read()
                                                else:
                                                        coordenada=2
                                                        if (memoriaC!=coordenada):
                                                                    print ("2")
                                                                    ser.write("2")
                ##                                      if (standby=="Y"):
                ##                                              cambio="B"
                                                        #print ser.read()
                                    elif (real_y>160):
                                                if (real_x<110):
                                                        coordenada=7
                                                        if (memoriaC!=coordenada):
                                                                    print ("7")
                                                                    ser.write("7")
                ##                                      if (standby=="Y"):
                ##                                              cambio="B"
                                                        #print ser.read()
                                                elif (real_x>210):
                                                        coordenada=9
                                                        if (memoriaC!=coordenada):
                                                                    print ("9")
                                                                    ser.write("9")
                ##                                      if (standby=="Y"):
                ##                                              cambio="B"
                                                        #print ser.read()
                                                else:
                                                        coordenada=8
                                                        if (memoriaC!=coordenada):
                                                                    print ("8")
                                                                    ser.write("8")
                ##                                      if (standby=="Y"):
                ##                                              cambio="B"
                                                        #print ser.read()
                                    else:
                                                if (real_x<110):
                                                        coordenada=4
                                                        if (memoriaC!=coordenada):
                                                                    print ("4")
                                                                    ser.write("4")
                ##                                        if (standby=="Y"):
                ##                                                    cambio="B"
                                                        #print ser.read()
                                                elif (real_x>210):
                                                        coordenada=6
                                                        if (memoriaC!=coordenada):
                                                                    print ("6")
                                                                    ser.write("6")
                ##                                      if (standby=="Y"):
                ##                                              cambio="B"
                                                        #print ser.read()
                                                else:
                                                        coordenada=5
                                                        if (memoriaC!=coordenada):
                                                                    print ("5")
                                                                    ser.write("5")
                ##                                      if (standby=="Y"):
                ##                                              cambio="B"
                                                        #print ser.read() 
                                    time.sleep(0.8) #0.2
                                    memoriaC=coordenada
                ##                      if (state=="standby"):
                ##                              print standby
                ##                              thand=5


                                    
        ##                            m = alsaaudio.Mixer('PCM')
        ##                            m.setvolume(0)   


                                
                        # shows the window system.array
                        #cv2.imshow('frame', stream.array)
                        
                        # pressing q stops the application
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                        # stream reset
                        stream.seek(0)
                        stream.truncate()

                cv2.destroyAllWindows()



        

def cameraInit(ser):
        cascade_path =  "/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_alt.xml"
        cascade = cv2.CascadeClassifier(cascade_path)
        cameraThread = threading.Thread(target=cameraRun,args=(ser,cascade,))
        cameraThread.start()










