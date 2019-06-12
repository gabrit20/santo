#coding: latin-1
import codecs
from settings import *


pope = {}



def allpopeInit():
    global pope

    
    
    
    file = codecs.open('allpope.csv', encoding='latin-1')
    file.readline() #skips the first line
    for line in file:

        
        items = line.strip().split(';')
        popeID = str(items[0])
        part = str(items[1])
        text_IT = items[2].encode('utf-8')
        text_ES = items[3].encode('utf-8')
        text_EN = items[4].encode('utf-8')
        text_DE = items[5].encode('utf-8')


        if popeID not in pope:
            pope[popeID] = {}
        if part not in pope[popeID]:
            pope[popeID][part] = {}

        pope[popeID][part] = {'IT':text_IT, 'ES':text_ES, 'EN':text_EN, 'DE':text_DE}


print("Initialising pope...")
