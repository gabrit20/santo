import random
import threading
import soundfiles
from settings import *

#Text to speech
from alltext import *
from playVoice import playVoice
from playWave import playWave
from camera import cameraInit

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

import serial
global ser






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
                                #playSound(chosenReply,0)


                

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

        #while True:
        if (state == "enquiry" or state == "greeting" ):
                #print("listening inside timeout", listening)
                #if (listening == True):
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
                                #pass
                                state = "noreply"
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



        

def saintLogic():
        global state
        global listening
        global played
        global countInteractions
        global countEmpty
        while True:

                #if (int(time.clock()*10)%25 == 0):
                print("STATE:", state, "played=",played, "listening=",listening)

                
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


                elif (state=="enquiry"): 

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
                        timeout()
                        listening = True
                        print("enabling listening from inside enquiry")

                        if(countEmpty >= maxWaitingCycles):
                                print("countEmpty", countEmpty)
                                played = False
                                listening = False
                                state = "gotostandby"
                                print("go to gotostandby from main enquiry")  
                                #changeState("gotostandby", False, False, "main")
                                

                elif (state=="noreply"):
                        print("no reply")
                        time.sleep(1)
                        countEmpty += 1
                        print("go to enquiry from main noreply")
                        played = True
                        state = "enquiry"
                        #changeState("enquiry", False, False, "main")


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
                        playSound(random.choice(soundfiles.wakaranai),0)
                        #playSound("wakaranai",0)
                        time.sleep(1.2)
                        countInteractions += 1
                        played = False
                        state = "enquiry"
                        print("go to enquiry from main wakaranai")                
                        #changeState("enquiry", False, False, "main")


                



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


        #cuentatiempo=threading.Thread(target=timeout)
        #cuentatiempo.start()
        cameraInit(ser)
        
        touchhand=threading.Thread(target=tacto)
        touchhand.start()
        logicThread = threading.Thread(target=saintLogic)
        logicThread.start()

##        m = alsaaudio.Mixer('PCM')
##        m.setvolume(95)




init()

alltextInit()
allvocabularies.allvocabulariesInit()







