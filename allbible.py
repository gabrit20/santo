#coding: latin-1
import codecs
from settings import *

Bible = {}


def allbibleInit():


    booksFile = codecs.open("BibleBooks.csv", encoding='latin-1')
    booksFile.readline() #skips the first line
    for line in booksFile:
        items = line.strip().split(';')
        bookID = str(items[0])
        bookName_IT = items[1].encode('utf-8')
        bookName_ES = items[2].encode('utf-8')
        bookName_EN = items[3].encode('utf-8')
        bookName_DE = items[4].encode('utf-8')


        Bible[bookID] = {'bookNames': {'IT':bookName_IT, 'ES':bookName_ES, 'EN':bookName_EN, 'DE':bookName_DE}}

        
    

    singleBiblefile = codecs.open('Bible'+language_out+'.csv', encoding='latin-1')

    for line in singleBiblefile:

        items = line.strip().split(';')
        bookName = items[0].encode('utf-8')
        bookNum = str(items[1])
        verseNum = str(items[2])
        verse = items[3].encode('utf-8')

        for iBook in Bible:
            if (Bible[iBook]['bookNames'][language_out] == bookName):

                if bookNum not in Bible[iBook]:
                    Bible[iBook][bookNum] = {}
                if verseNum not in Bible[iBook][bookNum]:
                    Bible[iBook][bookNum][verseNum] = {}

                Bible[iBook][bookNum][verseNum][language_out] = verse
                break


#allbibleInit()
#print(Bible['Genesis']['bookNames'])
#print(Bible['Genesis']['3']['1'])
