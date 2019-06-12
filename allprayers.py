#coding: latin-1
import codecs
from settings import *


prayers = {}



def allprayersInit():
    global prayers

    
    
    
    file = codecs.open('allprayers.csv', encoding='latin-1')
    file.readline() #skips the first line
    for line in file:

        
        items = line.strip().split(';')
        prayerID = str(items[0])
        part = str(items[1])
        text_IT = items[2].encode('utf-8')
        text_ES = items[3].encode('utf-8')
        text_EN = items[4].encode('utf-8')
        text_DE = items[5].encode('utf-8')


        if prayerID not in prayers:
            prayers[prayerID] = {}
        if part not in prayers[prayerID]:
            prayers[prayerID][part] = {}

        prayers[prayerID][part] = {'IT':text_IT, 'ES':text_ES, 'EN':text_EN, 'DE':text_DE}

print("Initialising prayers...")
