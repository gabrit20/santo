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
from alldates import *
from allprayers import *
from allpope import *
from allvocabularies import *
from allquotes import *
from allentries import *

from playVoice import *
from camera import cameraInit

from speech_recognizer_google_standalone import GSpeech
speech_rec = GSpeech("")

import soundfiles


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

                while(True):
                        if (speech_rec.is_in_recognition() == False): break
                        #if (int(time.clock()*10)%1000 == 0):
                        #        print("speech_lock main while", speech_lock)
                        #time.sleep(1)
                        #print("speech_lock main while", speech_lock)
                        pass
                #time.sleep(recordingTime) # Make it equal to recording length inside Speech Recognition module.

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
                                
                                

                        time.sleep(3) #to avoid multiple touch detected  with just one press




def retrieveTextFromKey(source, key, wholeBook=False): #TODO: key not found exception
        """retrieves a single dictionary (with all the languages) or more than one,
        into a list containing each filename and dictionary/string
        to be processed by playSound(filename, archive=-1)"""
        textPartsToPlay = []
        if (source == 'text'):
                dictionaryEntry = text[key]    
                if dictionaryEntry[language_out] != "":
                        textPartsToPlay.append([key, dictionaryEntry])
        elif (source == 'pray'):
                counter = 0
                for counter in range(0, maxNumPartsText):
                        if str(counter) in prayers[key]['parts']: #if entry exists
                                dictionaryEntry = prayers[key]['parts'][str(counter)] 
                                if dictionaryEntry[language_out] != "":
                                        textPartsToPlay.append([key, dictionaryEntry])           
        elif (source == 'pope'):
                counter = 0
                for counter in range(0, maxNumPartsText):
                        if str(counter) in pope[key]['parts']: #if entry exists
                                dictionaryEntry = pope[key]['parts'][str(counter)] 
                                if dictionaryEntry[language_out] != "":
                                        textPartsToPlay.append([key, dictionaryEntry])      
        elif (source == 'quotes'):
                counter = 0
                for counter in range(0, maxNumPartsText):
                        if str(counter) in quotes[key]['parts']: #if entry exists
                                dictionaryEntry = quotes[key]['parts'][str(counter)] 
                                if dictionaryEntry[language_out] != "":
                                        textPartsToPlay.append([key, dictionaryEntry])    
        elif (source == 'saints'):
                [month, day, info] = IDtoDate(key)
                dictionaryEntry = saints[month][day][info] 
                if dictionaryEntry[language_out] != "":
                        textPartsToPlay.append([key, dictionaryEntry])    
        elif ((source == 'bible' or source in Biblebooks) and wholeBook == False):
                [book,bookNum,verseNum] = BibleIDtoData(key)
                print("coordinates:",book,bookNum,verseNum)
                dictionaryEntry = Bible[book][bookNum][verseNum]
                if dictionaryEntry[language_out] != "":
                        textPartsToPlay.append([key, dictionaryEntry])
                #previous and next also included
                previousVerseNum = str(int(verseNum)-1)
                if previousVerseNum in Bible[book][bookNum]:
                        previousKey = BibleDataToID(book, bookNum, previousVerseNum)
                        textPartsToPlay.insert(0, [previousKey, Bible[book][bookNum][previousVerseNum] ] )
                nextVerseNum = str(int(verseNum)+1)
                if nextVerseNum in Bible[book][bookNum]:
                        nextKey = BibleDataToID(book, bookNum, nextVerseNum)
                        textPartsToPlay.append( [nextKey, Bible[book][bookNum][nextVerseNum] ] )
                #also bookName and book number
                textPartsToPlay.insert(0, [book, Biblebooks[book] ])
                textPartsToPlay.insert(1, [bookNum, bookNum] )
        elif ((source == 'bible' or source in Biblebooks) and wholeBook == True):
                [book,bookNum,verseNum] = BibleIDtoData(key)
                #book="Dan"
                #bookNum="1"
                #also bookName and book number
                textPartsToPlay.insert(0, [book, Biblebooks[book] ])
                textPartsToPlay.insert(1, [bookNum, bookNum] )
                
                for iVerse in Bible[book][bookNum]:
                        key = BibleDataToID(book,bookNum,iVerse)
                        print("coordinates:",book,bookNum,iVerse)
                        dictionaryEntry = Bible[book][bookNum][iVerse]
                        print("dictionaryEntry", dictionaryEntry)
                        if dictionaryEntry[language_out] != "":
                                textPartsToPlay.append([key, dictionaryEntry])         
                
        #print("textPartsToPlay", textPartsToPlay)
        return textPartsToPlay


def BibleIDtoData(key):
        book = key[0:3] #012
        bookNum = key[3]
        if key[4] != ":":
                bookNum += key[4]
        verseNum = key[key.index(":")+1 : len(key)]
        return [book, bookNum, verseNum]


def BibleDataToID(book, bookNum, verseNum):
        return str(book) + str(bookNum) + ":" + str(verseNum)


def IDtoDate(key):
        month = key[0]
        if key[1].isdigit():
                month += key[1]
        day = key[key.index("-")+1 : len(key)-1]
        info = key[len(key)-1]
        return [month, day, info]


def dateToID(month, day, info):
        return str(month) + '-' + str(day) + info


def wordInSentence(currentSource, listWords, wordsGroup, sentence, foundKey, foundResults): #foundResults is passed by reference
        """wordsGroup can be 'topic' or 'people'"""
        for i in range(len(listWords)):
                if listWords[i] in sentence:
                        #foundKey = str(book) + str(bookNum) + ":" + str(verseNum)
                        #foundKey = prayer
                        if foundKey not in foundResults:
                                foundResults[foundKey] = {}
                                foundResults[foundKey]['source'] = currentSource
                                foundResults[foundKey]['topic'] = 0
                                foundResults[foundKey]['people'] = 0
                        foundResults[foundKey][wordsGroup] += 1  #example: 'topic'
                        #print("FOUND", listWords[i], foundKey)


def randomSearchText(source):
        if (source == 'bible'):
                randomBookID = random.choice(list(Bible.keys()))
                randomBookNum = random.choice(list(Bible[randomBookID].keys()))
                verseNum = 1
                randomChoice = BibleDataToID(randomBookID, randomBookNum, verseNum)


        if (source in list(Biblebooks.keys())):
                randomBookNum = random.choice(list(Bible[source].keys()))
                verseNum = 1
                randomChoice = BibleDataToID(source, randomBookNum, verseNum)



        if (source == 'pray'):
                #OLD: this one would not work if all prayers are missing in one language
##                randomChoice = random.choice(list(prayers.keys()))
##                while (prayers[randomPrayer]['parts']['1'][language_out] == "" or
##                       prayers[randomPrayer]['randomOK'] == "0"):
##                        print("empty prayer entry; skipping")
##                        randomChoice = random.choice(prayers.keys())
##
                allkeys = list(prayers.keys())
                i = 0
                while i < len(allkeys):
                        print(allkeys[i])
                        if prayers[allkeys[i]]['parts']['1'][language_out] == "" or \
                           prayers[allkeys[i]]['randomOK'] == "0":
                                allkeys.remove(allkeys[i])
                                i -= 1
                        i += 1
                randomChoice = random.choice(allkeys)
                        
                        
        if (source == 'pope'):
                allkeys = list(pope.keys())
                i = 0
                while i < len(allkeys):
                        print(allkeys[i])
                        if pope[allkeys[i]]['parts']['1'][language_out] == "" or \
                           pope[allkeys[i]]['randomOK'] == "0":
                                allkeys.remove(allkeys[i])
                                i -= 1
                        i += 1
                randomChoice = random.choice(allkeys)

        return [source, randomChoice]

        

def searchText(source, topic, people):
        """searchs for topic OR people in sources and adds to foundResults.
        In foundResults filters out in case of topic AND people those with only one of the two
        then picks a random entry
        returns the foundSource and the key"""
        listWordsTopic = []
        if topic != -1:
                listWordsTopic = vocTopics[topic][language_in]
                for i in range(len(listWordsTopic)):
                        listWordsTopic[i] = listWordsTopic[i].encode('utf-8')
        listWordsPeople = []
        if people != -1:
                listWordsPeople = vocPeople[people][language_in]
                for i in range(len(listWordsPeople)):
                        listWordsPeople[i] = listWordsPeople[i].encode('utf-8')
        print(listWordsTopic)
        print("listWordsTopic", listWordsTopic)
        foundSource = None
        print("Searching....")
        foundResults = {}   #key, topic, people
        if (source == 'bible' or source == -1):
                foundSource = 'bible'
                for book in Bible:
                        #print("book", book)
                        for bookNum in Bible[book]:
                                #print("bookNum", bookNum)
                                for verseNum in Bible[book][bookNum]:
                                        #print("verseNum", verseNum)
                                        #print(Bible[book][bookNum][verseNum])
                                        #print(Bible[book][bookNum][verseNum][language_out])
                                        if (language_out in Bible[book][bookNum][verseNum]): #check that language exists
                                                foundKey = BibleDataToID(book, bookNum, verseNum)
                                                wordInSentence(foundSource, listWordsTopic, 'topic', Bible[book][bookNum][verseNum][language_out], foundKey, foundResults)
                                                wordInSentence(foundSource, listWordsPeople, 'people', Bible[book][bookNum][verseNum][language_out], foundKey, foundResults)

        if (source == 'pray' or source == -1):
                foundSource = 'pray'
                for prayer in prayers:
                        for part in prayers[prayer]['parts']:
                                print(prayers[prayer]['parts'][part])
                                if (language_out in prayers[prayer]['parts'][part]): #check that language exists
                                        foundKey = prayer
                                        wordInSentence(foundSource, listWordsTopic, 'topic', prayers[prayer]['parts'][part][language_out], foundKey, foundResults)
                                        wordInSentence(foundSource, listWordsPeople, 'people', prayers[prayer]['parts'][part][language_out], foundKey, foundResults)


        if (source == 'pope' or source == -1): #exactly the same as prayers
                foundSource = 'pope'
                for popeword in pope:
                        for part in pope[popeword]['parts']:
                                if (language_out in pope[popeword]['parts'][part]): #check that language exists
                                        foundKey = popeword
                                        wordInSentence(foundSource, listWordsTopic, 'topic', pope[popeword]['parts'][part][language_out], foundKey, foundResults)
                                        wordInSentence(foundSource, listWordsPeople, 'people', pope[popeword]['parts'][part][language_out], foundKey, foundResults)


        if (source == 'quotes' or source == -1): #exactly the same as prayers
                foundSource = 'quotes'
                for quote in quotes:
                        for part in quotes[quote]['parts']:
                                if (language_out in quotes[quote]['parts'][part]): #check that language exists
                                        foundKey = quote
                                        wordInSentence(foundSource, listWordsTopic, 'topic', quotes[quote]['parts'][part][language_out], foundKey, foundResults)
                                        wordInSentence(foundSource, listWordsPeople, 'people', quotes[quote]['parts'][part][language_out], foundKey, foundResults)

        if (people != -1):
                if people[0].isdigit(): #if it's a date, the query is a saint
                        foundSource = 'saints'
                        foundKey = people[0:len(people)-1] + 's'
                        if foundKey not in foundResults:
                                foundResults[foundKey] = {}
                                foundResults[foundKey]['source'] = foundSource
                                foundResults[foundKey]['topic'] = 0
                                foundResults[foundKey]['people'] = 1


        #print("foundResults:", foundResults)
        #filter case of AND
        if (topic != -1 and people != -1):
                for result in list(foundResults): #converted to a list to force a copy of the keys to avoid runtime error
                        if foundResults[result]['topic']==0 or foundResults[result]['people'] ==0:
                                del foundResults[result]
                                #print("deleted", result)

        print("filtered foundResults:", foundResults)
        
        if len(foundResults) > 0:        
                chosenResult = random.choice(list(foundResults))   #chosenResult is a key of dictionary
                if (['-1', source, topic, people, chosenResult, '0'] not in entries):
                        print("adding to the entries")
                        entries.append(['-1', source, topic, people, chosenResult, '0'])
                print("chosenResult:",chosenResult)
                print(entries)

                return [foundResults[chosenResult]['source'], chosenResult]
        else:
                return [None, None]
                

        
def elaborateAnswer(keyword):  #enters here only if it recognises some word
        global v
        global state
        global gender
        global alreadyPlayed
        global chosenReply

        

        is_matched = False
        answer_found = False
        keyword = keyword.lower()
        print("keyword>", keyword)
        logging.info("keyword> "+ keyword)

        query = [-1, -1, -1, -1] #Generic, Sources, Topics, People

        if (state == "enquiry" and len(keyword)>=2):
                #print("in elaborateAnswer enquiry")
                chosenReply = -1
                queryID = -1

                loopQueryIndex = [0, 1, 2, 3]
                loopVoc = [vocGeneric, vocSources, vocTopics, vocPeople]

                for iQueryIndex, voc in zip(loopQueryIndex, loopVoc):
                        for iKey in voc:
                                #print("iKey",iKey)
                                for iWord in voc[iKey][language_in]: #compare the strings, one inside another
                                        #print("iWord", iWord)
                                        #print("iWord in keyword", iWord in keyword)
                                        #print("keyword in iWord", keyword in iWord)
                                        if iWord in keyword or keyword in iWord:
                                                print("match: [", keyword, "] with [", iWord, "]")
                                                is_matched = True
                                                query[iQueryIndex] = iKey
                                                break
                                                break


                print("QUERY", query)
                
                iCommand = 0
                iSource = 1
                iTopic = 2
                iPeople = 3
                #command = query[iCommand]
                #source = query[iSource]
                #topic = query[iTopic]
                #people = query[iPeople]
                answerColumn = iPeople+1 #column after
                                
                if (is_matched == True):


                        #CASE 1: direct command
                        
                        if query == ["bye", -1, -1, -1]:
                        #if queryID == "bye":
                                playSound("goInPeace")
                                time.sleep(0.4)
                                countInteractions == 0
                                playSound("retireShort")
                                answer_found = True
                                changeState("farewell", state, func_name(), True)

                        elif query == ["thanks", -1, -1, -1]:        
                        #elif queryID == "thanks":
##                                playSound("yourewelcome1")
##                                time.sleep(0.4)
##                                countInteractions == 0
##                                playSound("goInPeace")
                                answer_found = True
                                print("changeState", "farewell")
                                changeState("farewell", state, func_name(), True)
                                
                                
                        elif query == ["day", -1, -1, -1]:
                        #elif queryID == "day":
                                answer_found = True
                                print("changeState", "saint")
                                changeState("saint", state, func_name(), False)
                                

                        #CASE 2: direct command to random mode
                                
                        elif query == [-1, "bible", -1, -1]:
                        #elif queryID == "bible":
                                playSound("verse")
                                time.sleep(0.3)
                                playSound("touchHand")
                                time.sleep(0.8)
                                [searchResultSource, searchResultReply] = randomSearchText(query[iSource])
                                if (searchResultReply != None):
                                        chosenReply = retrieveTextFromKey(searchResultSource, searchResultReply, True )
                                        answer_found = True
        
                                        print("random Bible part: ", chosenReply )
                                print("changeState", "reply")
                                changeState("reply", state, func_name(), False)


                        elif query[iSource] in list(Biblebooks.keys()) and query[0] == -1 and query[2:4] == [-1, -1]:
                                [searchResultSource, searchResultReply] = randomSearchText(query[iSource])
                                if (searchResultReply != None):
                                        chosenReply = retrieveTextFromKey(searchResultSource, searchResultReply, True )
                                        answer_found = True
        
                                        print("random Bible part: ", chosenReply )
                                print("changeState", "reply")
                                changeState("reply", state, func_name(), False)

                                

                        elif query == [-1, "pray", -1, -1]:
                        #elif queryID == "pray":
                                answer_found = True
                                playSound("prayStart")
                                time.sleep(1)
                                [searchResultSource, searchResultReply] = randomSearchText(query[iSource])
                                if (searchResultReply != None):
                                        chosenReply = retrieveTextFromKey(searchResultSource, searchResultReply )
                                        print("random pray: ", chosenReply )
                                print("changeState", "reply")
                                changeState("reply", state, func_name(), False)
                                

                        elif query == [-1, "pope", -1, -1]:
                        #elif queryID == "pope":
                                answer_found = True
                                playSound("popeStart")
                                time.sleep(1)
                                print("changeState", "reply")
                                changeState("reply", state, func_name(), False)
                                

                        #CASE 3: direct keyword to answer
                                
                        elif query[1:4] == [-1, -1, -1] and query[iCommand] != -1:
                                for iEntry in range(1, len(entries)): #skip first line
                                        if (query[iCommand] == entries[iEntry][iCommand]):         
                                                chosenEntry = entries[iEntry]
                                                chosenReply = retrieveTextFromKey('text', chosenEntry[answerColumn])
                                                break
                                if chosenReply != -1:
                                        answer_found = True
                                        print("replying to ", keyword, " with: ", chosenReply )
                                        changeState("reply", state, func_name(), False)
                                                                           
                                        

                        #CASE 4/5: entries and query
                        else:
                                availableEntries = []
                                for iEntry in range(1, len(entries)): #skip first line

                                        
                                        if ((query[iSource] == entries[iEntry][iSource] or query[iSource] == -1) and
                                            query[iTopic] == entries[iEntry][iTopic] and
                                            query[iPeople] == entries[iEntry][iPeople]):
                                                availableEntries.append(iEntry)
                                #CASE 4A: available entry
                                if len(availableEntries)>0:
                                        print(availableEntries)
                                        chosenEntry = entries[random.choice(availableEntries)]           
                                        chosenReply = retrieveTextFromKey(chosenEntry[iSource], chosenEntry[answerColumn] )
                                        print("retrieveTextFromKey", chosenEntry[iSource], chosenEntry[answerColumn])
                                #CASE 4B: search
                                else:
                                        playSound("search")
                                        time.sleep(0.2)
                                        [searchResultSource, searchResultReply] = searchText(query[iSource], query[iTopic], query[iPeople])
                                        if (searchResultReply != None):
                                                chosenReply = retrieveTextFromKey(searchResultSource, searchResultReply )
                                if chosenReply != -1:
                                        answer_found = True
                                        print("replying to ", keyword, " with: ", chosenReply )
                                        changeState("reply", state, func_name(), False)
                                        print("answer found")
                                else:
                                        playSound("noresults")
                                        changeState("wakaranai", state, func_name(), False) #for now wakaranai
                                        print("answer not found")
                                        


        elif (state == "meeting"):
                #print("in elaborateAnswer greeting")
                if (keyword is not None):       #len(keyword) >= 3):
                        is_matched = True
                        answer_found = True
                        print("setting is_matched = True  in elaborateAnswer greeting")
                if (is_matched == True):
                        print(soundfiles.users)
                        logging.info("NAME: "+ keyword)
                        gender = "m"
                        if keyword[len(keyword)-1] == "a":
                                gender = "f"
                        print(gender)


##                        playSound("cuellar1")
##                        envia=cabezera+"C100"
##                        ser.write(envia)
##                        time.sleep(tiempoSer)
##                        envia=cabezera+"B100"
##                        ser.write(envia)
##                        time.sleep(tiempoSer)
##                        envia=cabezera+"A100"
##                        ser.write(envia)
##                        time.sleep(tiempoSer)
##                        playSound("cuellar2")
##                        time.sleep(1)
##                        changeState("pray", state, func_name(), False)
##                        return
##                        


                        
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
                        
        #CASE 5: did not understand
        if (is_matched == False or answer_found == False):
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

                        hour = timeInfo[3]
                        print("hour", hour)
                        if (hour < 12):
                                playSound("greetingMorning")
                        elif (hour < 17):
                                playSound("greetingAfternoon")
                        elif (hour < 19):
                                playSound("greetingEvening")
                        elif (hour >= 19):
                                playSound("greetingNight")
                                   
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
                        global dates
                        dayInfoFound = 0
                                                        
                        print("playing the saint of the day")
                        #smonth = str(random.randint(1,12)) #test random month
                        #sday = str(random.randint(1,31)) #test random day

                        dayFilename = smonth + '-' + sday + 'd'
                        nameFilename = smonth + '-' + sday + 'n'
                        storyFilename = smonth + '-' + sday + 's'



                        if (dates[smonth][sday][language_out] != ""):
                                #playSound("today")
                                playSound(dayFilename, dates[smonth][sday])
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

                                             
                elif (state=="farewell"):
                        if alreadyPlayed == False:
                                playSound("retire")
                        time.sleep(3)
                        changeState("standby", state, func_name(), True) #no chimes


                elif (state=="enquiry"):
                        print("ENQUIRY inside")
                        

                        if alreadyPlayed == False:
                                if countInteractions <= 0:
                                        alreadyPlayed = playSound("tellMeLong2")   
                                elif countInteractions % 3 == 0:
                                        print("countInteractions", countInteractions)
                                        alreadyPlayed = playSound(random.choice(soundfiles.variants["tellMeElse"]))
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
                        while (state=="reply"): #necessary condition as touching hand will shift the state
                                for replyPart in chosenReply:
                                        print("REPLY with ", replyPart[0], replyPart[1])
                                        playSound(replyPart[0], replyPart[1])
                                        time.sleep(0.1)
                                break
                        time.sleep(2)
                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)


                elif (state=="wakaranai"):
                        playSound(random.choice(soundfiles.variants["wakaranai"]))
                        time.sleep(1.2)
                        countInteractions += 1
                        changeState("enquiry", state, func_name(), False)


def keepLightsOn():
        while (state == "standby"):
                if (int(time.clock()*10)%50 == 0):
                        
                        print ("keep lights on")
                        envia=cabezera+"B111"
                        espalda=1
                        ser.write(envia)
                        time.sleep(tiempoSer)
                        envia=cabezera+"A111"
                        aureola=1
                        ser.write(envia)
                        time.sleep(tiempoSer)
                        candela=1
                        envia=cabezera+"C111"
                        ser.write(envia)

def detectCandle():
        global ser
        global cabezera

        envia=cabezera+"V000"
        ser.write(envia)
        for i in range(0,6):
                state=ser.read()
                print (state)
        return state

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
                        #envia=cabezera+"M000"
                        #ser.write(envia)
                        #print ("envio")
                        b=0
                        break
                except:
                        print ("No se conecto")
                        b=b+1
                        if (b==100):
                                print ("Error de conexion")
                                break
        
        banderita=0
        while (banderita==0):
                """
                envia=cabezera+"V000"
                ser.write(envia)
                
                for i in range(0, 6):
                        x=ser.read()
                """
                candleOn=detectCandle()
                time.sleep(0.1)
                if (candleOn=='0'):
                        banderita=1
                        envia=cabezera+"M000"
                        ser.write(envia)
                        print ("envio")     
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

                        #envia=cabezera+"C111"
                        #ser.write(envia)

                        
        cameraInit(ser)
        touchhand=threading.Thread(target=touch)
        touchhand.start()
        logicThread = threading.Thread(target=logic)
        logicThread.start()

        logging.basicConfig(filename="logs/log"+str(year)+"-"+smonth+"-"+sday+"-"+shour+"-"+sminute+".txt", level=logging.INFO)
        logging.basicConfig(format='%(message)s')       




#texts must be initialised before init()
alltextInit()
allbibleInit()
allsaintsInit()
alldatesInit()
allprayersInit()
allpopeInit()
allquotesInit()
allentriesInit()
#vocabularies must be done after saints and Bible
allvocabulariesInit()


init()








