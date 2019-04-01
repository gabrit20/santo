import random
import sys
import time
import logging

import threading
alreadyPlayed = False
alreadyPlayed_ready = threading.Event()
#state_ready = threading.Event()
alreadyPlayed_ready.set()


from settings import *

from alltext import *
from allbible import *
from allsaints import *
from allprayers import *

from playVoice import *
from camera import cameraInit

from speech_recognizer_google_standalone import GSpeech
speech_rec = GSpeech("")

import soundfiles
import allvocabularies


global chosenReply
chosenReply = ""
global countInteractions
countInteractions = 0
countEmpty = 0

import serial
global ser
global cabezera
global tiempoSer
global aureola
global espalda

aureola=0
espalda=0
tiempoSer=0.30

cabezera="$OAX"

import pygame
from pygame.mixer import music


                        
def func_name():
        return sys._getframe(1).f_code.co_name


def changeState(newState, previousState, callingFunction, bStopNextSpeech):
        global alreadyPlayed
        global state
        timeInfo = time.localtime(time.time())

                
        if (newState != "noreply" and previousState != "noreply"):
                countEmpty = 0
        if bStopNextSpeech != -1:
                alreadyPlayed = bStopNextSpeech
        state = newState
        print("STATE CHANGING TO " + newState + " FROM " + previousState + " IN " + callingFunction)
        logging.info(str(timeInfo[3])+":"+str(timeInfo[4])+ ": " + "STATE CHANGING TO " + newState + " FROM " + previousState + " IN " + callingFunction)
        alreadyPlayed_ready.set()
        #state_ready.set()



        


def playSound(filename, archive=-1):

        global ser
        global cabezera
        global tiempoSer
        global aureola
        global espalda
        
        print("playSound: ", filename)
        logging.info("playSound: "+ filename)
        
        if (archive == -1):
                archive = text[filename] #id of filename coincides with the key of the dictionary
        
        print('ARCHIVE', archive)
        #if (row != -1 and column != -1):
        #        playList(language_out, filename, archive, row, column)
        if (espalda==0):
                time.sleep(tiempoSer)
                envia=cabezera+"B111"
                espalda=1
                ser.write(envia)
        if (aureola==1):
                time.sleep(tiempoSer)
                envia=cabezera+"A000"
                aureola=0
                ser.write(envia)

        playDict(language_out, filename, archive)

                

        while (pygame.mixer.music.get_busy()==True):
                time.sleep(1)

        if (espalda==1):
                time.sleep(tiempoSer)
                envia=cabezera+"B000"
                espalda=0
                ser.write(envia)
        return True






def listen():

        global state
        global speech_rec
        global is_recognized
        global countInteractions
        global countEmpty
        global alreadyPlayed
        global ser
        global cabezera
        global tiempoSer
        global aureola
        global espalda
        
        #while True:
        if (state == "enquiry" or state == "meeting" ):  #shouldn't happen in other states

                is_recognized = -1
                
                #print("Speech recognition starting")
                #aureola on
                if (aureola==0):
                        time.sleep(tiempoSer)
                        envia=cabezera+"A111"
                        aureola=1
                        ser.write(envia)
                        
                if (espalda==1):
                        time.sleep(tiempoSer)
                        envia=cabezera+"B000"
                        espalda=0
                        ser.write(envia)
                        
                speech_rec.start()
                
                time.sleep(recordingTime) # Make it equal to recording length inside Speech Recognition module.

                speech_rec.stop()
                #aureola off
                if (aureola==1):
                        time.sleep(tiempoSer)
                        envia=cabezera+"A000"
                        aureola=0
                        ser.write(envia)
                #print("Speech recognition stopped")
                is_recognized = speech_rec.is_recognized

                
                print("is_recognized", is_recognized)


                if (is_recognized == False):

                        countEmpty += 1

                        if (state=="meeting"):
                                #skip the name
                                if (countEmpty >= 3): 
                                        countInteractions = 0                           
                                        changeState("enquiry", state, func_name(), False)
                                else:
                                        changeState("noname", state, func_name(), False)


                        elif (state=="enquiry"):
                                changeState("noreply", state, func_name(), False)
                                #it keeps running

                                

                                        
                        


def touch():
        global state
        global alreadyPlayed
        global countEmpty
        global countInteractions
        global speech_rec
        recibo = -1
        while True:
                if (ser.inWaiting()>0):
                        recibo=ser.read()
                        print (recibo)
                        
                if ((recibo=="L")|(recibo=="R")):
                        print ("hand recibo", recibo)
                        logging.info("hand recibo" + recibo)
                        if (state=="standby"):
                                countEmpty = 0
                                #print("recibo1", recibo, state)
                                #recibo = -1
                                #print("recibo2", recibo, state)
                                
                                changeState("greeting", state, func_name(), False)
                                continue
                        if (state=="enquiry"):
                                countEmpty = 0
                                #recibo = -1
                                speech_rec.force_stop()
                                changeState("farewell", state, func_name(), False)
                                continue
                        if (state=="greeting" or state=="meeting"):
                                #print("recibo1", recibo, state)
                                countEmpty = 0
                                #recibo = -1
                                speech_rec.force_stop()
                                while (pygame.mixer.music.get_busy()==True):
                                        pygame.mixer.music.stop()
                                #print("recibo2", recibo, state)
                                changeState("enquiry", state, func_name(), False)
                                continue
                        if (state =="reply"):
                                while (pygame.mixer.music.get_busy()==True):
                                        recibo = -1
                                        pygame.mixer.music.stop()
                                        changeState("enquiry", state, func_name(), False)
                                continue
                        if (state =="saint"):
                                while (pygame.mixer.music.get_busy()==True):
                                        recibo = -1
                                        pygame.mixer.music.stop()
                                        changeState("enquiry", state, func_name(), False)
                                continue
                        if (state =="pray"):
                                while (pygame.mixer.music.get_busy()==True):
                                        recibo = -1
                                        pygame.mixer.music.stop()
                                        changeState("enquiry", state, func_name(), False)
                                continue
                        if (state =="bible"):
                                while (pygame.mixer.music.get_busy()==True):
                                        recibo = -1
                                        pygame.mixer.music.stop()
                                        changeState("enquiry", state, func_name(), False)
                                continue
                                
                                

                        time.sleep(3) #to avoid multiple touch detected  with just one press



        
def elaborateAnswer(keyword):  #enters here only if it recognises some word
        global v
        global state
        global gender
        global alreadyPlayed
        global chosenReply
        global countInteractions
        

        is_matched = False
        keyword = keyword.lower()
        print("keyword>", keyword)
        logging.info("keyword> "+ keyword)



        if (state == "enquiry"):
                print("in elaborateAnswer enquiry")
                chosenReply = -1
                queryID = -1


                for iKey in allvocabularies.vocabulary:
                        #print("iKey",iKey)
                        for iWord in allvocabularies.vocabulary[iKey][language_in]: #compare the strings, one inside another
                                if iWord in keyword or keyword in iWord:
                                        #print("match", keyword, iWord)
                                        is_matched = True
                                        print("setting is_matched = True in elaborateAnswer query")
                                        queryID = iKey
                                        print("queryID", queryID)
                                        break
                                        break

                if (is_matched == True):             

                        if queryID == "bye":
                                playSound("goInPeace")
                                time.sleep(0.4)
                                countInteractions == 0
                                playSound("retireShort")
                                changeState("farewell", state, func_name(), True)
                                
                        elif queryID == "day":
                                changeState("saint", state, func_name(), False)

                        elif queryID == "bible":
                                changeState("bible", state, func_name(), False)

                        elif queryID == "pray":
                                changeState("pray", state, func_name(), False)

                        elif queryID == "problem":
                                playSound("problem")
                                time.sleep(1.5)
                                changeState("pray", state, func_name(), True)

                        else: 
                                for i in range(len(soundfiles.replies)):
                                        print("soundfiles.replies[i]", soundfiles.replies[i])
                                        if(soundfiles.replies[i][0] == queryID): 
                                               chosenReply = soundfiles.replies[i][random.randint(1, len(soundfiles.replies[i])-1)]
                                               break
                                print("replying to " + keyword +" with file " +chosenReply )
                                
                                changeState("reply", state, func_name(), False)


                

        elif (state == "meeting"):
                print("in elaborateAnswer greeting")
                if (keyword is not None):       #len(keyword) >= 3):
                        is_matched = True
                        print("setting is_matched = True  in elaborateAnswer greeting")
                if (is_matched == True):
                        print(soundfiles.users)
                        logging.info("NAME: "+ keyword)
                        gender = "m"
                        if keyword[len(keyword)-1] == "a":
                                gender = "f"
                        print(gender)
                        if keyword not in soundfiles.users:
                                print("new user", keyword)
                                soundfiles.users.append(keyword)
                                #playSound("meet")
                                if gender == "m":
                                        playSound("meetM")
                                else:
                                        playSound("meetF")

                        else:
                                print("exhisting user")
                                if gender == "m":
                                        playSound("welcomeBackM")
                                else:
                                        playSound("welcomeBackF")

                #even if regognized is false: skip name if not detected
                #countInteractions += 1
                time.sleep(0.5)
                playSound("intro")
                time.sleep(0.5)
                playSound("aureola")
                changeState("enquiry", state, func_name(), False)
                time.sleep(0.8)
                        

        if (is_matched == False):
                changeState("wakaranai", state, func_name(), False)
                                
                        

        

def logic():
        global state
        global alreadyPlayed
        global countInteractions
        global countEmpty
        global chosenReply
        global aureola
        global espalda
        while True:

                if (state != "standby"):
                        if (int(time.clock()*10)%25 == 0):
                                print("STATE:", state, "alreadyPlayed=",alreadyPlayed)

                
                if (state == "standby"):
                        #print("STANDBY inside")
                        #print(alreadyPlayed_ready.is_set())
                        alreadyPlayed_ready.wait()
                        if (alreadyPlayed == False and state == "standby"):
                                #print("PLAY CHIMES")
                                alreadyPlayed = playWave('chimes')
                                alreadyPlayed_ready.clear()
                        


                elif (state == "greeting"):
                        #print("BEGIN inside")

                        if (espalda==1):
                                time.sleep(tiempoSer)
                                envia=cabezera+"B000"
                                espalda=0
                                ser.write(envia)

                        if (aureola==1):
                                time.sleep(tiempoSer)
                                envia=cabezera+"A000"
                                aureola=0
                                ser.write(envia)

                        

                        playSound("inTheNameAmen")
                        time.sleep(0.8)
                        playSound("greeting1")
                        time.sleep(0.5)      
                        playSound("myNameShort")
                        time.sleep(0.5)      
                        if (countInteractions == 0 and state == "greeting"):
                                changeState("meeting", state, func_name(), False)
                        else:
                                changeState("enquiry", state, func_name(), False)
                        


                elif (state=="noname"):
                        print("no name")
                        print("countEmpty", countEmpty)
                        changeState("meeting", state, func_name(), True)


                elif (state == "meeting"):
                        #print("GREETING inside")

                        if alreadyPlayed == False:
                                alreadyPlayed = playSound("yourName")
                                time.sleep(1)
                        listen()
                                


                elif (state == "saint"):
                        global saints
                        dayInfoFound = 0
                                                        
                        print("playing the saint of the day")

                        dayFilename = smonth + '-' + sday + 'd'
                        nameFilename = smonth + '-' + sday + 'n'
                        storyFilename = smonth + '-' + sday + 's'



                        if (saints[smonth][sday]['d'][language_out] != ""):
                                playSound(dayFilename, saints[smonth][sday]['d'])
                                if (saints[smonth][sday]['n'][language_out] != ""):
                                        playSound("dayMemory")
                                        playSound(nameFilename, saints[smonth][sday]['n'])
                                        time.sleep(0.5)
                                        playSound(storyFilename, saints[smonth][sday]['s'])
                                else:
                                        playSound("noSaint")
                                        playSound("sorry")
                        else:
                                playSound("noDay")
                                playSound("sorry")
                        
                        
                        time.sleep(1.5)
                                
                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)

                elif (state == "bible"):
                        global Bible
                        randomBookID = random.choice(Bible.keys())
                        randomBooknum = random.choice(Bible[randomBookID].keys())
                        while (randomBooknum.isdigit() == False): #as it contains also the key "bookNames"
                                randomBooknum = random.choice(Bible[randomBookID].keys())


                        
                        randomVerseBookname = randomBookID
                        randomVerseBooknum = randomBooknum
                                

                        playSound("verse")
                        time.sleep(0.3)
                        playSound("touchHand")
                        playSound(randomBookID, Bible[randomBookID]['bookNames'])
                        playSound(randomBooknum, randomBooknum)  #play only the number
                        
                        time.sleep(0.8)
                        iVerse = 1
                        iVerseFilename = randomBookID + '-'  + randomBooknum + '-' + str(iVerse)
                        print("Bible", randomBookID, randomBooknum, str(iVerse))
                        playSound(iVerseFilename, Bible[randomBookID][randomBooknum][str(iVerse)])
                        
                        while (state=="bible"): #necessary condition as touching hand will shift the state

                                iVerse += 1
                                if (str(iVerse) in Bible[randomBookID][randomBooknum]):
                                        iVerseFilename = randomBookID + '-'  + randomBooknum + '-' + str(iVerse)
                                        playSound(iVerseFilename, Bible[randomBookID][randomBooknum][str(iVerse)])
                                else:
                                        break

                        time.sleep(1.5)

                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)

                                             
                elif (state == "pray"):
                        if alreadyPlayed == False:
                                playSound("prayStart")
                        time.sleep(1)
                        randomPrayer = random.choice(prayers.keys())
                        part = 1
                        
                        while (prayers[randomPrayer][str(part)][language_out] == ""):
                                print("empty prayer entry; skipping")
                                randomPrayer = random.choice(prayers.keys())
                        
                        while (state=="pray"):
                                playSound(randomPrayer + str(part), prayers[randomPrayer][str(part)])
                                part += 1
                                if (str(part) not in prayers[randomPrayer]):
                                        break
                        time.sleep(1.5)

                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)

                                             
                elif (state=="farewell"):
                        if alreadyPlayed == False:
                                playSound("retire")
                        time.sleep(3)
                        changeState("standby", state, func_name(), True) #no chimes


                elif (state=="enquiry"):
                        print("ENQUIRY inside")

                        if alreadyPlayed == False:
                                if countInteractions <= 0:
                                        alreadyPlayed = playSound("tellMeLong")   
                                else:
                                        
                                        alreadyPlayed = playSound(random.choice(soundfiles.variants["tellMe"]))
                                time.sleep(0.5)
                        listen()

                        if(countEmpty >= maxWaitingCycles):
                                print("countEmpty", countEmpty)
                                changeState("farewell", state, func_name(), False)
                                

                elif (state=="noreply"):
                        print("no reply")
                        time.sleep(0.2)
                        print("countEmpty", countEmpty)
                        changeState("enquiry", state, func_name(), True)


                elif (state=="reply"):
                        playSound(chosenReply)
                        time.sleep(1)
                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)


                elif (state=="wakaranai"):
                        playSound(random.choice(soundfiles.variants["wakaranai"]))
                        time.sleep(1.2)
                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)


                



def init():
        global ser
        global cascade
        global cabezera
        global tiempoSer
        global aureola
        global espalda
        
        b = 0
        speech_rec.register_callback(elaborateAnswer)
        
        while True:
                try:
                        ser = serial.Serial('/dev/ttyUSB'+ str(b),9600,timeout=0.3)
                        time.sleep(tiempoSer)
                        ser.flushInput()
                        print ("paso delay")
                        envia=cabezera+"M000"
                        ser.write(envia)
                        print ("envio")
                        b=0
                        break
                except:
                        print ("No se conecto")
                        b=b+1
                        if (b==100):
                                print ("Error de conexion")
                                break
        
        #ser = serial.Serial('/dev/ttyUSB1',9600,timeout=0.3)
        #time.sleep(tiempoSer)
        #ser.flushInput()
        print ("paso delay")
        envia=cabezera+"M000"
        ser.write(envia)
        print ("envio")
        time.sleep(tiempoSer)

        #print ("apago espalda")
        print ("espalda on")
        #envia=cabezera+"B000"
        envia=cabezera+"B111"
        #espalda=0
        espalda=1
        ser.write(envia)
        time.sleep(tiempoSer)
        #print ("apago aureola")
        print ("aureola on")
        #envia=cabezera+"A000"
        envia=cabezera+"A111"
        #aureola=0
        aureola=1
        ser.write(envia)

        
        cameraInit(ser)
        touchhand=threading.Thread(target=touch)
        touchhand.start()
        logicThread = threading.Thread(target=logic)
        logicThread.start()

        logging.basicConfig(filename="logs/log"+str(year)+"-"+smonth+"-"+sday+"-"+shour+"-"+sminute+".txt", level=logging.INFO)
        logging.basicConfig(format='%(message)s')

        




#texts must be initialised before init()
alltextInit()
allvocabularies.allvocabulariesInit()
allbibleInit()
allsaintsInit()
allprayersInit()

init()








