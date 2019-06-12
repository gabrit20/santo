#coding: latin-1
import codecs
from settings import *


dates = {}
dateformat = {'IT':"DDMM", 'ES':"DDMM", 'EN':"DDMM", 'DE':"DDMM"}
days = []
months = []
words = []

def alldatesInit():
    global dates

    
    
    
    file = codecs.open('alldates.csv', encoding='latin-1')
    file.readline() #skips the first line
    for line in file:

        
        items = line.strip().split(';')
        datatype = str(items[0])
        number = str(items[1])
        text_IT = items[2]#.encode('utf-8')
        text_ES = items[3]#.encode('utf-8')
        text_EN = items[4]#.encode('utf-8')
        text_DE = items[5]#.encode('utf-8')

    
        if (datatype == "words"):
            words.append({'IT':text_IT, 'ES':text_ES, 'EN':text_EN, 'DE':text_DE})
        elif (datatype == "month"):
            months.append({'IT':text_IT, 'ES':text_ES, 'EN':text_EN, 'DE':text_DE})
        elif (datatype == "day"):
            days.append({'IT':text_IT, 'ES':text_ES, 'EN':text_EN, 'DE':text_DE})

    file.close()
    #print(words)
    #print(months)
    #print(days)

    
    for m in range(len(months)):
        month = str(m+1)
        for d in range(len(days)):
            day = str(d+1)
            sentences = {}
            for lan in language_list:
                sentence = ""
                dateformat_language = dateformat[lan]

                if dateformat_language == "DDMM":
                    sentence += words[0][lan].strip()  #today
                    sentence += " "
                    sentence += words[1][lan].strip()  #it's 
                    sentence += " "
                    sentence += days[d][lan].strip()  
                    sentence += " "
                    sentence += words[2][lan].strip()  #of 
                    sentence += " "
                    sentence += months[m][lan].strip()
                    sentence += " "
                    sentence += words[3][lan].strip()  #desu
                elif dateformat_language == "MMDD":
                    sentence += words[0][lan].strip()  #today
                    sentence += " "
                    sentence += words[1][lan].strip()  #it's 
                    sentence += " "
                    sentence += months[m][lan].strip()  
                    sentence += " "
                    sentence += words[2][lan].strip()  #of 
                    sentence += " "
                    sentence += days[d][lan].strip()
                    sentence += " "
                    sentence += words[3][lan].strip()  #desu

                sentences[lan] = sentence.encode('utf-8')
            

            if month not in dates:
                dates[month] = {}
            if day not in dates[month]:
                dates[month][day] = {}
            dates[month][day] = sentences
            #print(month, day, sentences)




print("Initialising dates...")
if __name__ == '__main__':
    alldatesInit()
    for i in range(1, 13):
        print("")
        print (i)
        for j in range(1, 30):
            print (j, saints[str(i)][str(j)])

