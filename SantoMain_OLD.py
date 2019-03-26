import picamera
import picamera.array
import cv2
import math
import serial

#import sounddevice as sd
import numpy.linalg as np

##import alsaaudio
##import pygame
##from pygame.mixer import music

import threading
import soundfiles
import random
import time
from settings import *

#Text to speech
from alltext import *
from playVoice import playVoice
from playWave import playWave

from speech_recognizer_google_standalone import GSpeech
speech_rec = GSpeech("")


import allvocabularies

listening = False
played = False
global chosenReply
chosenReply = ""
global countInteractions
countInteractions = 0
countEmpty = 0


global ser
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
color = (15,15,15)
prev_x = 160
prev_y = 120
global memoriaC
memoriaC=0
global cascade





# doesnt work for all the calls from elaborateAnswer
def changeState(newState, bStopNextSpeech, bEnableListening, fromWhichFunction):
        global listening
        global played
        global state

        if bStopNextSpeech != -1:
                played = bStopNextSpeech
        if bEnableListening != -1:
                listening = bEnableListening
                
        countEmpty = 0
        print("CHANGING TO " + newState + " FROM " + fromWhichFunction + " " +state)
        state = newState



        


def playSound(cancion, stop):

        global ser
        global listening
        global speech_rec

        print("playSound: ", cancion)

        previousListening = listening
        speechStarted = speech_rec.isStarted()
        print("speechStarted", speechStarted)

        if (listening == True):
                print("turning off listening momentarily")
                listening = False

#if enabled, this breaks the direct playing of any playSound from elaborateAnswer or even reactivating it below, makes it delayed
##        if (speechStarted):
##                print("turning off speech rec momentarily")
##                speech_rec.stop() 
        

        playVoice(language_out, cancion)

        

        if (listening == True):
                print("reenabling listening")
                listening = previousListening

##        if (speechStarted):
##                print("reenabling speech rec")
##                speech_rec.start()
 



                
          #to interrupt with hand. doesnt work      
##        else: 
##              while (stop==1):
##                      if (pygame.mixer.music.get_busy()==True):
##                              recibo=ser.read()
##                              if (recibo=="L"):
##                                      stop="N"
##                                      #time.sleep(1)
##                              if (recibo=="R"):
##                                      stop="N"
##                                      #time.sleep(1)
##                              #continue
##                      else:
##                              stop="N"
##
##                      time.sleep(1)
##

        return True



        
def elaborateAnswer(keyword):  #enters here only if it recognises some word
        global v
        global state
        global gender
        global played
        global chosenReply
        global countInteractions
        
        changeState = False
        is_recognized = False
        keyword = keyword.lower()
        print("keyword>", keyword)



        if (state == "enquiry"):
                print("in elaborateAnswer enquiry")
                chosenReply = -1
                queryID = -1


                for iKey in allvocabularies.vocabulary:
                        #print("iKey",iKey)
                        for iWord in allvocabularies.vocabulary[iKey][language_in]: #compare the strings, one inside another
                                if iWord in keyword or keyword in iWord:
                                        #print("match", keyword, iWord)
                                        is_recognized = True
                                        print("setting is_recognized = True in elaborateAnswer query")
                                        queryID = iKey
                                        print("queryID", queryID)
                                        break
                                        break

                if (is_recognized == True):             

                        if queryID == "bye":
                                playSound("goInPeace",0)
                                time.sleep(0.4)
                                playSound("retireShort",0)
                                countEmpty = 0
                                played = True
                                state = "gotostandby"
                                print("go to standby from elaborateAnswer", played)
                                #changeState("gotostandby", False, -1, "elaborateAnswer")
                        elif queryID == "day":
                                countEmpty = 0
                                played = False
                                listening = False
                                state = "saint"
                                print("go to saint from elaborateAnswer", played)
                                #changeState("saint", False, False, "elaborateAnswer")
                        elif queryID == "prob":
                                playSound("problem",0)
                                time.sleep(1.5)
                                countEmpty = 0
                                played = False
                                listening = False
                                state = "pray"
                                print("go to pray from elaborateAnswer", played)
                                #changeState("saint", False, False, "elaborateAnswer")
                        else: #no state changes
                                for i in range(len(soundfiles.replies)):
                                        print("soundfiles.replies[i]", soundfiles.replies[i])
                                        if(soundfiles.replies[i][0] == queryID): 
                                               chosenReply = soundfiles.replies[i][random.randint(1, len(soundfiles.replies[i])-1)]
                                               break
                                print("replying to " + keyword +" with file " +chosenReply )
                                
                                countEmpty = 0
                                played = False
                                listening = False
                                state = "reply"
                                print("go to reply from elaborateAnswer")
                                #changeState("reply", False, False, "elaborateAnswer")


                

        elif (state == "greeting"):
                print("in elaborateAnswer greeting")
                if (keyword is not None):       #len(keyword) >= 3):
                        is_recognized = True
                        print("setting is_recognized = True  in elaborateAnswer greeting")
                if (is_recognized == True):
                        print(soundfiles.users)
                        gender = "m"
                        if keyword[len(keyword)-1] == "a":
                                gender = "f"
                        print(gender)
                        if keyword not in soundfiles.users:
                                print("new user", keyword)
                                soundfiles.users.append(keyword)
                                #playSound("meet",0)
                                if gender == "m":
                                        playSound("meetM",0)
                                else:
                                        playSound("meetF",0)

                        else:
                                print("exhisting user")
                                if gender == "m":
                                        playSound("welcomeBackM",0)
                                else:
                                        playSound("welcomeBackF",0)

                #even if regognized is false: skip name if not detected
                countEmpty = 0
                #countInteractions += 1
                played = False
                state = "enquiry"
                print("go to enquiry from elaborateAnswer", played)
                #changeState("enquiry", False, -1, "elaborateAnswer")
                        

        if (is_recognized == False):
                countEmpty = 0
                played = False
                listening = False
                print("disabling listening from inside elaborateAnswer")
                state = "wakaranai"
                print("go to wakaranai from elaborateAnswer")
                #changeState("wakaranai", False, False, "elaborateAnswer")
                                
                        




def timeout():

        global state
        global listening
        global speech_rec
        global is_recognized #
        global countInteractions
        global countEmpty
        global played

        while True:
                #print("listening inside timeout", listening)
                if (listening == True):
                        is_recognized = -1
                        
                        print("Speech recognition starting")
                        speech_rec.start()
                        
                        #time.sleep(speech_recognizer_google_standalone.seconds) # Make it equal to recording length inside Speech Recognition module.
                        time.sleep(recordingTime) # Make it equal to recording length inside Speech Recognition module.

                        speech_rec.stop()
                        print("Speech recognition stopped")

                        listening = False
                        print("disabling listening from inside timeout")


                        print("is_recognized", is_recognized)
                        print("nothing was recognized")


                        if (is_recognized == -1):

                                countEmpty += 1

                                if (state=="greeting"):
                                        #skip the name
                                        countEmpty = 0 
                                        played = False
                                        countInteractions = 0
                                        state = "enquiry"
                                        print("go to enquiry from timeout")   #skip the name                             
                                        #changeState("enquiry", False, -1, "timeout")


                                elif (state=="enquiry"):
                                        listening = True
                                        pass
                                        #it keeps running

                                

                                        
                        



def tacto():
        global state
        global played
        global countInteractions
        while True:

                recibo=ser.read()
                if ((recibo=="L")|(recibo=="R")):
                        print ("hand recibo", recibo)
                        if (state=="standby"):
                                countEmpty = 0
                                played = False
                                state="begin"
                                print("go to begin from tacto")
                                #changeState("begin", False, -1, "tacto")
##                      if (state=="saint"):
##                              countInteractions += 1
##                              countEmpty = 0
##                              played = False
##                              state="enquiry"
##                              print("go to enquiry from tacto")
                                #changeState("enquiry", False, -1, "tacto")
##                      if (state=="greeting"):
##                              countInteractions += 1
##                              countEmpty = 0
##                              played = False
##                              state="enquiry"
##                              print("go to enquiry from tacto") 
##                              #changeState("enquiry", False, -1, "tacto")
                        if (state=="enquiry"):
                                played = False
                                countEmpty = 0
                                state="gotostandby"
                                print("go to gotostandby from tacto")                        
                                #changeState("gotostandby", False, -1, "tacto")

                        time.sleep(0.2) #to avoid multiple touch detected  with just one press



def init():
        global ser
        global cascade
        b = 0
        speech_rec.register_callback(elaborateAnswer)
        while True:
                try:
                        ser = serial.Serial('/dev/ttyUSB'+ str(b),9600,timeout=0.3)
                        time.sleep(2)
                        print ("paso delay")
                        ser.write("0")
                        print ("envio")
                        b=0
                        break
                except:
                        print ("No se conecto")
                        b=b+1
                        if (b==100):
                                print ("Error de conexion")
                                break


        cuentatiempo=threading.Thread(target=timeout)
        cuentatiempo.start()
        touchhand=threading.Thread(target=tacto)
        touchhand.start()
        cascade_path =  "/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_alt.xml"
        cascade = cv2.CascadeClassifier(cascade_path)

##        m = alsaaudio.Mixer('PCM')
##        m.setvolume(95)




init()
alltextInit()
allvocabularies.allvocabulariesInit()


with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        
        while True:
                if (state=="standby"):
                        if played == False:
                                played = playWave('chimes') 
                        


                elif (state=="begin"): 

                        playSound("inTheNameAmen",0)

                        countEmpty = 0
                        played = False
                        state = "greeting"
                        print("go to greeting from main begin")
                        #changeState("greeting", False, -1, "main")
                        


                elif (state=="greeting"): 

                        if played == False:
                                playSound("greeting1",0)
                                time.sleep(0.5)
                                played = playSound("yourName",0)
                                listening = True


                elif (state=="saint"):
                        dayInfoFound = 0
                        for iSaint in range(len(soundfiles.saintsDB)):
                                print("days", soundfiles.saintsDB[iSaint][0], month, soundfiles.saintsDB[iSaint][1], day)
                                if soundfiles.saintsDB[iSaint][0] == month and soundfiles.saintsDB[iSaint][1] == day:
                                        dayInfoFound = iSaint
                                        break
                                
                        print("playing the saint of the day")
                        #playSound(soundfiles.saintsDB[iSaint][2],0)
                        #playSound(soundfiles.saintsDB[iSaint][3],0) #it
                        #playSound(soundfiles.saintsDB[iSaint][4],0) #it
                        for iData in range(2, len(soundfiles.saintsDB[dayInfoFound])):
                                playSound(soundfiles.saintsDB[dayInfoFound][iData],0)
                        
                        time.sleep(0.8)
                                
                        countInteractions += 1
                        countEmpty = 0
                        played = False
                        listening = True
                        state = "enquiry"
                        print("go to enquiry from main saint")
                        #changeState("enquiry", False, True, "main")

                elif (state=="pray"):
                        playSound(random.choice(soundfiles.prayers),0)
                        print("replying with a prayer" )
                        time.sleep(0.8)

                        countInteractions += 1
                        countEmpty = 0
                        played = False
                        listening = True
                        state = "enquiry"
                        print("go to enquiry from main pray")
                        #changeState("enquiry", False, True, "main")

                                             

                elif (state=="enquiry"):
                        
                        if (int(time.clock()*10)%25 == 0):
                                print("enquiry status", played, listening)
                        if played == False:
                                if countInteractions <= 0:
                                        played = playSound("tellMeLong",0)                                        
                                else:
                                        #played = playSound("tellMe1",0)
                                        for i in range(len(soundfiles.variants)):
                                                if(soundfiles.variants[i][0] == "tellMe"): 
                                                        played = playSound(soundfiles.variants[i][random.randint(1, len(soundfiles.variants[i])-1)],0)
                                                        break
                                time.sleep(0.5)
                                listening = True
                                print("enabling listening from inside enquiry")


                                                
##                        time.sleep(0.5)
##                        listening = True
##                        print("enabling listening from inside enquiry")

                        if(countEmpty >= maxWaitingCycles):
                                print("countEmpty", countEmpty)
                                played = False
                                listening = False
                                state = "gotostandby"
                                print("go to gotostandby from main enquiry")  
                                #changeState("gotostandby", False, False, "main")
                                


                elif (state=="reply"):
                        playSound(chosenReply,0)
                        time.sleep(1)
                        countInteractions += 1
                        countEmpty = 0
                        played = False
                        listening = False#True
                        print("disabling listening from inside reply")
                        state = "enquiry"
                        print("go to enquiry from main reply")
                        #changeState("enquiry", False, False, "main")


                elif (state=="wakaranai"):
                        listening = False#True
                        playSound("wakaranai",0)
                        time.sleep(0.8)
                        countInteractions += 1
                        played = False
                        state = "enquiry"
                        print("go to enquiry from main wakaranai")                
                        #changeState("enquiry", False, False, "main")


                elif (state=="gotostandby"):
                        if played == False:
                                playSound("retire",0)
                        countEmpty = 0
                        time.sleep(3)
                        played = True
                        listening = False
                        state = "standby"
                        print("go to standby from main gotostandby")    
                        #changeState("standby", True, False, "main")


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




