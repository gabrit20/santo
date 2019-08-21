#coding: latin-1
import codecs
from settings import *


interactive = {}


def allinteractiveInit():
    global prayers

    

    with codecs.open('allinteractive.csv', encoding='latin-1') as file:

        file.readline() #skips the first line
        for line in file:

            items = line.strip().split(';')
            interactiveID = str(items[0])
            randomOK = str(items[1])
            part = str(items[2]) 

            for iLanguage in language_list_out:    
                
                text = items[3+language_list_out.index(iLanguage)].lower().encode('utf-8')

                if interactiveID not in interactive:
                    interactive[interactiveID] = {}
                if 'parts' not in interactive[interactiveID]:
                    interactive[interactiveID]['parts'] = {}
                if part not in interactive[interactiveID]['parts']:
                    interactive[interactiveID]['parts'][part] = {}

                interactive[interactiveID]['parts'][part][iLanguage] = text
            interactive[interactiveID]['randomOK'] = randomOK
                
    
print("Initialising interactive...")


if __name__ == '__main__':
    allinteractiveInit()
    print(interactive)
