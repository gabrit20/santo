#coding: latin-1
import codecs
from settings import *


entries = []
entriesSkip = []


def allentriesInit():
    global entries
    global entriesSkip

    
    file = codecs.open('allentries.csv', encoding='latin-1')
    file.readline() #skips the first line
    for line in file:

        #convert to -1
        items = line.strip().split(';')
        for i in range(4): #up to people
            if items[i] == "-1":
                items[i] = int(items[i])
                
        
        command = items[0]
        source = items[1]
        topic = items[2]
        people = items[3]
        answerID = items[4]
        priority = int(items[5])

        entries.append([command, source, topic, people, answerID, priority])



    fileSkip = codecs.open('allentriesSkip.csv', encoding='latin-1')
    fileSkip.readline() #skips the first line
    for line in fileSkip:

        #convert to -1
        items = line.strip().split(';')
        for i in range(4): #up to people
            if items[i] == "-1":
                items[i] = int(items[i])
                
        
        command = items[0]
        source = items[1]
        topic = items[2]
        people = items[3]
        answerID = items[4]


        entriesSkip.append([command, source, topic, people, answerID])




print("Initialising entries...")

if __name__ == '__main__':
    allentriesInit()
    for i in entries:
        print(i)
    print('\n')

    for i in entriesSkip:
        print(i)
