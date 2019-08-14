#coding: latin-1
import codecs
from settings import *

Bible = {}
Biblebooks = {}


def allbibleInit():

    for iLanguage in language_list_out:

        with codecs.open("BibleBooks.csv", encoding='latin-1') as booksFile:
            booksFile.readline() #skips the first line
            for line in booksFile:
                items = line.strip().split(';')
                bookID = str(items[0])  #3 latters abbreviation
                bookName = items[1+language_list_out.index(iLanguage)].lower().encode('utf-8')

                if bookID not in Bible:
                    Bible[bookID] = {}
                #Bible[bookID] = {'bookNames': {'IT':bookName_IT, 'ES':bookName_ES, 'EN':bookName_EN, 'DE':bookName_DE}}

                if bookID not in Biblebooks:
                    Biblebooks[bookID] = {}
                Biblebooks[bookID][iLanguage] = bookName

    #print(Biblebooks)

    
    for iLanguage in language_list_out:
        if iLanguage != language_out:
            continue #cut loading times

        try:
            #iLanguage = 'EN'
            with codecs.open('Bible'+iLanguage+'.csv', encoding='latin-1') as singleBiblefile:
                print ("Processing Bible", iLanguage)
                
                for line in singleBiblefile:
                    #print(line)
                    items = line.strip().split(';')
                    bookName = items[0].lower().encode('utf-8') #may be "Gen" or "Génesis", will become "gen" or "gen\...nesis"
                    bookNum = str(items[1])
                    
                    verseNum = str(items[2])
                    verse = items[3].lower().encode('utf-8')

                    for iBook in Bible:
                        #print(bookName, iBook, iBook.lower().encode('utf-8'), Biblebooks[iBook][iLanguage]) #iBook is a 3 characters. Only for string comparison, must be made lower()
                        if (bookName == iBook.lower().encode('utf-8') or bookName == Biblebooks[iBook][iLanguage]):  #full name or abbreviation

                            if bookNum not in Bible[iBook]:
                                Bible[iBook][bookNum] = {}
                            if verseNum not in Bible[iBook][bookNum]:
                                Bible[iBook][bookNum][verseNum] = {}

                            Bible[iBook][bookNum][verseNum][iLanguage] = verse
                            #print("assigned", iBook,bookNum,verseNum,iLanguage,verse)
                            break
        except IOError:
            print("Bible file not found", iLanguage)


print("Initialising Bible...")
if __name__ == '__main__':
    allbibleInit()
    #for iBook in Bible:
    #    print(iBook)
    print(Biblebooks['Gen'])
    print(Bible['Rev']['3'])

