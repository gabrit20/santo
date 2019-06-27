#coding: latin-1
import codecs
from settings import *


prayers = {}


def allprayersInit():
    global prayers

    

    with codecs.open('allprayers.csv', encoding='latin-1') as file:

        file.readline() #skips the first line
        for line in file:

            items = line.strip().split(';')
            prayerID = str(items[0])
            randomOK = str(items[1])
            part = str(items[2]) 

            for iLanguage in language_list:    
                
                text = items[3+language_list.index(iLanguage)].lower().encode('utf-8')

                if prayerID not in prayers:
                    prayers[prayerID] = {}
                if 'parts' not in prayers[prayerID]:
                    prayers[prayerID]['parts'] = {}
                if part not in prayers[prayerID]['parts']:
                    prayers[prayerID]['parts'][part] = {}

                prayers[prayerID]['parts'][part][iLanguage] = text
            prayers[prayerID]['randomOK'] = randomOK
                
    
print("Initialising prayers...")


if __name__ == '__main__':
    allprayersInit()
    print(prayers)
