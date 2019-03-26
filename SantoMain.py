import random
import threading
import sys


from settings import *

from alltext import *
from playVoice import playVoice
from playWave import playWave
from camera import cameraInit

from speech_recognizer_google_standalone import GSpeech
speech_rec = GSpeech("")

import soundfiles
import allvocabularies

alreadyPlayed = False
global chosenReply
chosenReply = ""
global countInteractions
countInteractions = 0
countEmpty = 0

import serial
global ser


import pygame
from pygame.mixer import music

def func_name():
        return sys._getframe(1).f_code.co_name


def changeState(newState, previousState, callingFunction, bStopNextSpeech):
        global alreadyPlayed
        global state

        if bStopNextSpeech != -1:
                alreadyPlayed = bStopNextSpeech
                
        if (newState != "noreply" and previousState != "noreply"):
                countEmpty = 0
        print("STATE CHANGING TO " + newState + " FROM " + previousState + " IN " + callingFunction)
        state = newState



        


def playSound(cancion, stop):

        global ser

        print("playSound: ", cancion)
        playVoice(language_out, cancion)

        while (pygame.mixer.music.get_busy()==True):
                time.sleep(1)
        

        return True






def listen():

        global state
        global speech_rec
        global is_recognized #
        global countInteractions
        global countEmpty
        global alreadyPlayed

        #while True:
        if (state == "enquiry" or state == "greeting" ):  #shouldn't happen in other states

                is_recognized = -1
                
                print("Speech recognition starting")
                speech_rec.start()
                
                time.sleep(recordingTime) # Make it equal to recording length inside Speech Recognition module.

                speech_rec.stop()
                print("Speech recognition stopped")


                print("is_recognized", is_recognized)


                if (is_recognized == -1):

                        countEmpty += 1

                        if (state=="greeting"):
                                #skip the name
                                countEmpty = 0 
                                alreadyPlayed = False
                                countInteractions = 0
                                state = "enquiry"
                                print("go to enquiry from timeout")   #skip the name                             
                                #changeState("enquiry", False, -1, "timeout")


                        elif (state=="enquiry"):
                                #pass
                                changeState("noreply", state, func_name(), False)
                                #it keeps running

                                

                                        
                        



def touch():
        global state
        global alreadyPlayed
        global countInteractions
        global speech_rec
        while True:

                recibo=ser.read()
                if ((recibo=="L")|(recibo=="R")):
                        print ("hand recibo", recibo)
                        if (state=="standby"):
                                countEmpty = 0
                                changeState("begin", state, func_name(), False)
                        if (state=="enquiry"):
                                countEmpty = 0
                                speech_rec.stop()
                                changeState("farewell", state, func_name(), False)
                        if (state =="reply"):
                                while (pygame.mixer.music.get_busy()==True):
                                        pygame.mixer.music.stop()
                                        changeState("enquiry", state, func_name(), False)
                        if (state =="saint"):
                                while (pygame.mixer.music.get_busy()==True):
                                        pygame.mixer.music.stop()
                                        changeState("enquiry", state, func_name(), False)
                        if (state =="pray"):
                                while (pygame.mixer.music.get_busy()==True):
                                        pygame.mixer.music.stop()
                                        changeState("enquiry", state, func_name(), False)
                                
                                

                        time.sleep(0.2) #to avoid multiple touch detected  with just one press



        
def elaborateAnswer(keyword):  #enters here only if it recognises some word
        global v
        global state
        global gender
        global alreadyPlayed
        global chosenReply
        global countInteractions
        

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
                                countInteractions == 0
                                playSound("retireShort",0)
                                changeState("farewell", state, func_name(), True)
                                
                        elif queryID == "day":
                                changeState("saint", state, func_name(), False)

                        elif queryID == "prob":
                                playSound("problem",0)
                                time.sleep(1.5)
                                changeState("pray", state, func_name(), False)

                        else: 
                                for i in range(len(soundfiles.replies)):
                                        print("soundfiles.replies[i]", soundfiles.replies[i])
                                        if(soundfiles.replies[i][0] == queryID): 
                                               chosenReply = soundfiles.replies[i][random.randint(1, len(soundfiles.replies[i])-1)]
                                               break
                                print("replying to " + keyword +" with file " +chosenReply )
                                
                                changeState("reply", state, func_name(), False)


                

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
                #countInteractions += 1
                changeState("enquiry", state, func_name(), False)
                        

        if (is_recognized == False):
                changeState("wakaranai", state, func_name(), False)
                                
                        

        

def logic():
        global state
        global alreadyPlayed
        global countInteractions
        global countEmpty
        global chosenReply
        while True:

                if (state != "standby"):
                        if (int(time.clock()*10)%25 == 0):
                                print("STATE:", state, "alreadyPlayed=",alreadyPlayed)

                
                if (state == "standby"):
                        if alreadyPlayed == False:
                                alreadyPlayed = playWave('chimes') 
                        


                elif (state == "begin"): 

                        playSound("inTheNameAmen",0)
                        if (countInteractions == 0):
                                changeState("greeting", state, func_name(), False)
                        else:
                                changeState("enquiry", state, func_name(), False)
                        


                elif (state == "greeting"): 

                        if alreadyPlayed == False:
                                playSound("greeting1",0)
                                time.sleep(0.5)
                                alreadyPlayed = playSound("yourName",0)
                                time.sleep(0.5)
                                listen()
                                


                elif (state == "saint"):
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
                        changeState("enquiry", state, func_name(), False)

                elif (state == "pray"):
                        playSound(random.choice(soundfiles.prayers),0)
                        print("replying with a prayer" )
                        time.sleep(0.8)

                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)

                                             
                elif (state=="farewell"):
                        if alreadyPlayed == False:
                                playSound("retire",0)
                        time.sleep(3)
                        changeState("standby", state, func_name(), True) #no chimes


                elif (state=="enquiry"): 

                        if alreadyPlayed == False:
                                if countInteractions <= 0:
                                        alreadyPlayed = playSound("tellMeLong",0)                                        
                                else:
                                        #alreadyPlayed = playSound("tellMe1",0)
                                        for i in range(len(soundfiles.variants)):
                                                if(soundfiles.variants[i][0] == "tellMe"): 
                                                        alreadyPlayed = playSound(soundfiles.variants[i][random.randint(1, len(soundfiles.variants[i])-1)],0)
                                                        break
                                time.sleep(0.5)
                        listen()

                        if(countEmpty >= maxWaitingCycles):
                                print("countEmpty", countEmpty)
                                changeState("farewell", state, func_name(), False)
                                

                elif (state=="noreply"):
                        print("no reply")
                        time.sleep(1)
                        countEmpty += 1
                        print("go to enquiry from main noreply")
                        changeState("enquiry", state, func_name(), True)


                elif (state=="reply"):
                        playSound(chosenReply,0)
                        time.sleep(1)
                        countInteractions += 1
                        print("go to enquiry from main reply")
                        changeState("enquiry", state, func_name(), False)


                elif (state=="wakaranai"):
                        playSound(random.choice(soundfiles.wakaranai),0)
                        time.sleep(1.2)
                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)


                



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


        cameraInit(ser)
        touchhand=threading.Thread(target=touch)
        touchhand.start()
        logicThread = threading.Thread(target=logic)
        logicThread.start()





init()
alltextInit()
allvocabularies.allvocabulariesInit()







