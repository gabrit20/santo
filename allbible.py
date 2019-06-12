#coding: latin-1
import codecs
from settings import *

Bible = {}


def allbibleInit():


    booksFile = codecs.open("BibleBooks.csv", encoding='latin-1')
    booksFile.readline() #skips the first line
    for line in booksFile:
        items = line.strip().split(';')
        bookID = str(items[0])  #3 latters abbreviation
        bookName_IT = items[1].encode('utf-8')
        bookName_ES = items[2].encode('utf-8')
        bookName_EN = items[3].encode('utf-8')
        bookName_DE = items[4].encode('utf-8')


        Bible[bookID] = {'bookNames': {'IT':bookName_IT, 'ES':bookName_ES, 'EN':bookName_EN, 'DE':bookName_DE}}



    
    
    for iLanguage in language_list:

        try: 
            with codecs.open('Bible'+iLanguage+'.csv', encoding='latin-1') as singleBiblefile:
                #print (iLanguage)
                for line in singleBiblefile:
                    #print(line)
                    items = line.strip().split(';')
                    bookName = items[0].encode('utf-8')
                    bookNameNotEncoded = items[0]
                    bookNum = str(items[1])
                    
                    verseNum = str(items[2])
                    verse = items[3].encode('utf-8')

                    for iBook in Bible:
                        if (bookName == Bible[iBook]['bookNames'][iLanguage] or bookNameNotEncoded == iBook):  #full name or abbreviation

                            if bookNum not in Bible[iBook]:
                                Bible[iBook][bookNum] = {}
                            if verseNum not in Bible[iBook][bookNum]:
                                Bible[iBook][bookNum][verseNum] = {}

                            Bible[iBook][bookNum][verseNum][iLanguage] = verse
                            #print(iBook,bookNum,verseNum,iLanguage,verse)
                            break
        except:
            pass

print("Initialising Bible...")
if __name__ == '__main__':
    allbibleInit()
    #for iBook in Bible:
    #    print(iBook)
    print(Bible['Gen']['bookNames'])
    print(Bible['Rev']['3']['1'])

