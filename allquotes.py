#coding: latin-1
import codecs
from settings import *


quotes = {}



def allquotesInit():
    global quotes

    
    
    with codecs.open('allquotes.csv', encoding='latin-1') as file:

        file.readline() #skips the first line
        for line in file:

            items = line.strip().split(';')
            quoteID = str(items[0])
            randomOK = str(items[1])
            part = str(items[2])
            
            for iLanguage in language_list_out:

                text = items[3+language_list_out.index(iLanguage)].lower().encode('utf-8')


                if quoteID not in quotes:
                    quotes[quoteID] = {}
                if 'parts' not in quotes[quoteID]:
                    quotes[quoteID]['parts'] = {}
                if part not in quotes[quoteID]['parts']:
                    quotes[quoteID]['parts'][part] = {}

                quotes[quoteID]['parts'][part][iLanguage] = text
            quotes[quoteID]['randomOK'] = randomOK


        
print("Initialising quotes...")

if __name__ == '__main__':
    allquotesInit()
    print(quotes)
