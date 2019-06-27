#coding: latin-1
import codecs
from settings import *


entries = []



def allentriesInit():
    global entries

    
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


print("Initialising entries...")

if __name__ == '__main__':
    allentriesInit()
    for i in entries:
        print(i)
