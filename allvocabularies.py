import codecs
from settings import *

if __name__ == '__main__':
    from allsaints import *
    allsaintsInit()
from allsaints import saints

if __name__ == '__main__':
    from allbible import *
    allbibleInit()
from allbible import Biblebooks


vocGeneric = {}
vocSources = {}
vocTopics = {}
vocPeople = {}
    
def allvocabulariesInit():
##    global vocGeneric
##    vocGeneric = {}
##    global vocSources
##    vocSources = {}
##    global vocTopics
##    vocTopics = {}
##    global vocPeople
##    vocPeople = {}
    Nlanguages = len(language_list)
    entry = {}

    loopCSV = ["Generic", "Sources", "Topics", "People"]
    loopVoc = [vocGeneric, vocSources, vocTopics, vocPeople]
    for CSV, voc in zip(loopCSV, loopVoc):
        #print(CSV, voc)
        filename = 'allvocabularies' + CSV + '.csv'
        file = codecs.open(filename, encoding='latin-1') #used to be utf-8
        file.readline() #skips the first line
        for line in file:
            items = line.strip().split(';')
            keywordID = str(items[0])
            languageID = str(items[2])
            textArray = []
            for iText in range(3, len(items)):
                if items[iText] != '':
                    textArray.append(items[iText].lower()) 
            if str(items[1]) == '0': #first language: beginning of an entry
                entry = {}
            entry[languageID] = textArray
            if str(items[1]) == str(Nlanguages-1): #last language: end of an entry
                voc[keywordID] = entry
                #print("ENTRY")
                #print(keywordID, voc[keywordID])
        file.close()


    #adding existing saints
    #print("SAINTS")
    for month in saints:
        for day in saints[month]:
            for info in saints[month][day]:
                if info == 'n': #name
                    for iLanguage in language_list:
                        #print(month, day, iLanguage, saints[month][day]['s'][iLanguage])
                        if saints[month][day]['n'][iLanguage] != b'' and saints[month][day]['s'][iLanguage] != b'': #should be at least one language not empty (both name and story)
                            newKey = str(month) + '-' + str(day) + 'n'
                            #print("ADDING", newKey)
                            if newKey not in vocPeople:
                                vocPeople[newKey] = {}
                            for j in range(len(language_list_in)):
                                listOfSynonims = []   #necessary as words to be recognised have to be contained in a list. Otherwise it operates on a string, letter by latter
                                if saints[month][day]['n'][language_list[j]] != b'':
                                    listOfSynonims.append(saints[month][day]['n'][language_list[j]].decode('utf-8'))
                                vocPeople[newKey][language_list_in[j]] = listOfSynonims 
                            break
# NO
##    for month in saints:
##        for day in saints[month]:
##            for info in saints[month][day]:
##                if info == 'n': #name
##                    for j in range(len(language_list)):
##                        if saints[month][day]['n'][language_list[j]] != b'' and saints[month][day]['s'][language_list[j]] != b'': #should be at least one language not empty (both name and story)
##                            newKey = str(month) + '-' + str(day) + 'n'
##                            #print("ADDING", newKey)
##                            if newKey not in vocPeople:
##                                vocPeople[newKey] = {}
##
##                            listOfSynonims = []
##                            if saints[month][day]['n'][language_list[j]] != b'':
##                                listOfSynonims.append(saints[month][day]['n'][language_list[j]].decode('utf-8'))
##                            vocPeople[newKey][language_list_in[j]] = listOfSynonims 
                      
            

    for bookID in Biblebooks:          
        if bookID not in vocSources:
            vocSources[bookID] = {}
            for j in range(len(language_list_in)):
                listOfSynonims = []
                #print(Biblebooks[bookID])
                if Biblebooks[bookID][language_list[j]] != b'':
                     listOfSynonims.append(Biblebooks[bookID][language_list[j]].decode('utf-8'))
                vocSources[bookID][language_list_in[j]] = listOfSynonims


        

print("Initialising vocabularies...")
if __name__ == '__main__':
    allvocabulariesInit()
    print(vocGeneric)
    print(vocPeople)
    print(vocSources)
    
