#coding: latin-1
import codecs
from settings import *

Bible = []


def allbibleInit():
    global Bible
    
    
    #file = open("alltext.csv")
    file = codecs.open('Bible'+language_out+'.csv', encoding='latin-1')
    #file = codecs.open('alltext.csv', encoding='utf-8')
    #file.readline() #skips the first line
    for line in file:
        #line.decode('latin-1').encode('utf-8')
        items = line.strip().split(';')
        bookName = items[0].encode('utf-8')
        bookNum = int(items[1])
        bookVerse = int(items[2])
        verse = items[3].encode('utf-8')


        Bible.append([bookName, bookNum, bookVerse, verse])


