#coding: latin-1
import codecs

def alltextInit():
    global text
    text = {}
    
    #file = open("alltext.csv")
    file = codecs.open('alltext.csv', encoding='latin-1')
    #file = codecs.open('alltext.csv', encoding='utf-8')
    file.readline() #skips the first line
    for line in file:
        #line.decode('latin-1').encode('utf-8')
        items = line.strip().split(';')
        textID = str(items[0])
##        text_IT = str(items[1])
##        text_ES = str(items[2])
##        text_EN = str(items[3])
##        text_DE = str(items[4])
        text_IT = items[1].encode('utf-8')
        text_ES = items[2].encode('utf-8')
        text_EN = items[3].encode('utf-8')
        text_DE = items[4].encode('utf-8')


        text[textID] = [text_IT, text_ES, text_EN, text_DE]


