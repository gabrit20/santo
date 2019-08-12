import random
import sys
import time
import logging

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



import soundfiles


global chosenReply
chosenReply = ""


                        
def func_name():
        return sys._getframe(1).f_code.co_name


def changeState(newState, previousState, callingFunction, bStopNextSpeech):
        pass

        
def playSound(filename, archive=-1):
        pass
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

                maxNumVerses = 5
                numAddedVerses = 0
                for iVerse in Bible[book][bookNum]:
                        key = BibleDataToID(book,bookNum,iVerse)
                        print("coordinates (wholebook):",book,bookNum,iVerse)
                        dictionaryEntry = Bible[book][bookNum][iVerse]
                        print("dictionaryEntry (wholebook)", dictionaryEntry)
                        if dictionaryEntry[language_out] != "":
                                textPartsToPlay.append([key, dictionaryEntry])
                                numAddedVerses += 1
                                if numAddedVerses >= maxNumVerses:
                                        break
                
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
        print("listWordsTopic", listWordsTopic)
        print("listWordsPeople", listWordsPeople)
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
                                #print(prayers[prayer]['parts'][part])
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

        #print("foundResults before saints:", foundResults)
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
        #filter case of AND (as so far it collected OR)
        if (topic != -1 and people != -1):
                for result in list(foundResults): #converted to a list to force a copy of the keys to avoid runtime error
                        if foundResults[result]['topic']==0 or foundResults[result]['people'] ==0:
                                del foundResults[result]
                                #print("deleted", result)

        #print("entriesSkip", entriesSkip)
        for result in list(foundResults):
                #print([-1, foundResults[result]['source'], topic, people, result])
                if ([-1, foundResults[result]['source'], topic, people, result] in entriesSkip):
                        del foundResults[result]
                        #print("skipping", result)

        print("filtered foundResults:", foundResults)

        """
        foundResults contains for each key:
        the source where it has been found, and the flags topic and people, which are 0/1
        the variable foundSource will be overwritten and is not usable
        topic and people are the variables containing the original query parameters
        """
        
        if len(foundResults) > 0:        
                chosenResult = random.choice(list(foundResults))   #chosenResult is a key of dictionary
                if ([-1, source, topic, people, chosenResult, '0'] not in entries):
                        print("adding to the entries")
                        entries.append([-1, source, topic, people, chosenResult, '0'])
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

                        elif query == ["thanks", -1, -1, -1] or query == ["ijou", -1, -1, -1]:        
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
                                #playSound("touchHand")
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
                                print("availableEntries", availableEntries)
                                #CASE 4A: available entry
                                numAvailableEntries = len(availableEntries)
                                if numAvailableEntries>0 and random.randint(0, numAvailableEntries+1)<numAvailableEntries: #50% if one entry, 33% if two entries
                                        
                                        chosenEntry = entries[random.choice(availableEntries)]           
                                        chosenReply = retrieveTextFromKey(chosenEntry[iSource], chosenEntry[answerColumn] )
                                        print("retrieveTextFromKey", chosenEntry[iSource], chosenEntry[answerColumn])
                                #CASE 4B: search if no entries or with probability 1/(1+numAvailableEntries)
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
                                        changeState("wakaranai", state, func_name(), True) #for now wakaranai
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

#print(vocSources)
#elaborateAnswer("preocupado  quiero rezar")
#elaborateAnswer("hola")
#elaborateAnswer("estoy preocupado")
#elaborateAnswer("pecador")
#elaborateAnswer("soy un pecador quiero rezar")
#elaborateAnswer("quiero solo rezar")
#elaborateAnswer("que dice de Dios el papa?")
#elaborateAnswer("Dios sabe que soy un pecador? Quiero rezar")
#elaborateAnswer("que dice Jesús sobre la misericordia en la biblia?")
#elaborateAnswer("hablame de san francisco")
#elaborateAnswer("hablame de santa balbina")
#elaborateAnswer("no estoy feliz")
#retrieveTextFromKey('bible','1Ma5:54')
#elaborateAnswer("dime algo de la biblia")
#elaborateAnswer("dime algo de la Génesis")
#elaborateAnswer("estoy pierdendo mi fe")
#elaborateAnswer("que dice de Jesús en la Génesis?")
#elaborateAnswer("I am feeling sick from the bible")
#elaborateAnswer("tell me something by the pope")
#elaborateAnswer("tell me about saint patrick")
#elaborateAnswer("blessed margaret pole")
#elaborateAnswer("from the bible")
#elaborateAnswer("sono preoccupato")

while(True):
        print("speak:")
        elaborateAnswer(input())






