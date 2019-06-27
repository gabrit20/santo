#coding: latin-1
import codecs
from settings import *


pope = {}



def allpopeInit():
    global pope

    
    
    with codecs.open('allpope.csv', encoding='latin-1') as file:
        file.readline() #skips the first line
        for line in file:

            items = line.strip().split(';')
            popeID = str(items[0])
            randomOK = str(items[1])
            part = str(items[2]) 
            

            for iLanguage in language_list:

                text = items[3+language_list.index(iLanguage)].lower().encode('utf-8')


                if popeID not in pope:
                    pope[popeID] = {}
                if 'parts' not in pope[popeID]:
                    pope[popeID]['parts'] = {}
                if part not in pope[popeID]['parts']:
                    pope[popeID]['parts'][part] = {}

                pope[popeID]['parts'][part][iLanguage] = text
            pope[popeID]['randomOK'] = randomOK
                

print("Initialising pope...")


if __name__ == '__main__':
    allpopeInit()
    print(pope)
