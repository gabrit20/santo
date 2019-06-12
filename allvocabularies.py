import codecs


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
    Nlanguages = 4
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

if __name__ == '__main__':
    allvocabulariesInit()
    print(vocGeneric)
    print(vocPeople)
    
