#coding: latin-1
import codecs
from settings import *


saints = {}



def allsaintsInit():
    print("Initialising saints...")
    
    global saints

    
    
    with codecs.open('allsaints.csv', encoding='latin-1') as file:
        file.readline() #skips the first line
        for line in file:

            for iLanguage in language_list:
                items = line.strip().split(';')
                month = str(items[0])
                day = str(items[1])
                info = str(items[2])  #d/n/s (day/name/story)
                text = items[3+language_list.index(iLanguage)].lower().encode('utf-8')
                


                if month not in saints:
                    saints[month] = {}
                if day not in saints[month]:
                    saints[month][day] = {}
                if info not in saints[month][day]:
                    saints[month][day][info] = {}
                saints[month][day][info][iLanguage] = text

                #print(month, day, info, saints[month][day][info])
                #print()



if __name__ == '__main__':
    allsaintsInit()
    for i in range(1, 13):
        print("")
        print (i)
        for j in range(1, 30):
            print (j, saints[str(i)][str(j)])
    print(saints)

