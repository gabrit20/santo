import random
import threading
import sys


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



        


def playSound(filename, archive=-1):

        global ser

        print("playSound: ", filename)
        
        if (archive == -1):
                archive = text[filename] #id of filename coincides with the key of the dictionary
        
        print('ARCHIVE', archive)
        #if (row != -1 and column != -1):
        #        playList(language_out, filename, archive, row, column)

        playDict(language_out, filename, archive)

                

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
                #aureola on
                speech_rec.start()
                
                time.sleep(recordingTime) # Make it equal to recording length inside Speech Recognition module.

                speech_rec.stop()
                #aureola off
                print("Speech recognition stopped")
                is_recognized = speech_rec.is_recognized

                
                print("is_recognized", is_recognized)


                if (is_recognized == -1):

                        countEmpty += 1

                        if (state=="greeting"):
                                #skip the name
                                countEmpty = 0 
                                countInteractions = 0                           
                                changeState("enquiry", state, func_name(), False)


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
                                speech_rec.force_stop()
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
                                
                        if (state =="bible"):
                                print("CALLATE")
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
                playSound("intro")
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

                        playSound("inTheNameAmen")
                        if (countInteractions == 0):
                                changeState("greeting", state, func_name(), False)
                        else:
                                changeState("enquiry", state, func_name(), False)
                        


                elif (state == "greeting"): 

                        if alreadyPlayed == False:
                                playSound("greeting1")
                                time.sleep(0.5)
                                alreadyPlayed = playSound("yourName")
                                time.sleep(0.5)
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
                        
                        
                        time.sleep(0.8)
                                
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
                        time.sleep(0.8)

                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)

                                             
                elif (state=="farewell"):
                        if alreadyPlayed == False:
                                playSound("retire")
                        time.sleep(3)
                        changeState("standby", state, func_name(), True) #no chimes


                elif (state=="enquiry"): 

                        if alreadyPlayed == False:
                                if countInteractions <= 0:
                                        alreadyPlayed = playSound("tellMeLong")
                                        
                                else:
                                        #alreadyPlayed = playSound("tellMe1")
                                        for i in range(len(soundfiles.variants)):
                                                if(soundfiles.variants[i][0] == "tellMe"): 
                                                        alreadyPlayed = playSound(soundfiles.variants[i][random.randint(1, len(soundfiles.variants[i])-1)])
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
                        playSound(chosenReply)
                        time.sleep(1)
                        countInteractions += 1
                        print("go to enquiry from main reply")
                        changeState("enquiry", state, func_name(), False)


                elif (state=="wakaranai"):
                        playSound(random.choice(soundfiles.wakaranai))
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




#texts must be initialised before init()
alltextInit()
allvocabularies.allvocabulariesInit()
allbibleInit()
allsaintsInit()
allprayersInit()

init()








