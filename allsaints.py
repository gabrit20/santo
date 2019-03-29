#coding: latin-1
import codecs
from settings import *


saints = {}



def allsaintsInit():
    global saints

    
    
    
    file = codecs.open('allsaints.csv', encoding='latin-1')
    file.readline() #skips the first line
    for line in file:

        
        items = line.strip().split(';')
        month = str(items[0])
        day = str(items[1])
        info = str(items[2])
        text_IT = items[3].encode('utf-8')
        text_ES = items[4].encode('utf-8')
        text_EN = items[5].encode('utf-8')
        text_DE = items[6].encode('utf-8')


        if month not in saints:
            saints[month] = {}
        if day not in saints[month]:
            saints[month][day] = {}
        #saints[month][day][info] = [text_IT, text_ES, text_EN, text_DE]
        saints[month][day][info] = {'IT':text_IT, 'ES':text_ES, 'EN':text_EN, 'DE':text_DE}



        #print(month, day, info, saints[month][day][info])
        #print()



##allsaintsInit()
##for i in range(1, 13):
##    print("")
##    print (i)
##    for j in range(1, 30):
##        print (j, saints[str(i)][str(j)])
