import codecs

def allvocabulariesInit():
    global vocabulary
    vocabulary = {}
    Nlanguages = 4
    entry = {}
    
    #file = open("allvocabularies.csv")
    file = codecs.open('allvocabularies.csv', encoding='latin-1') #it's not utf-8!
    file.readline() #skips the first line
    for line in file:
        items = line.strip().split(';')
        keywordID = str(items[0])
        languageID = str(items[2])
        textArray = []
        for iText in range(3, len(items)):
            if items[iText] != '':
                #textArray.append(unicode(items[iText], 'utf8')) 
                #textArray.append(str(items[iText]))
                textArray.append(items[iText]) 
        if str(items[1]) == '0': #first language: beginning of an entry
            entry = {}
        entry[languageID] = textArray

        if str(items[1]) == str(Nlanguages-1): #last language: end of an entry
            vocabulary[keywordID] = entry
            #print("ENTRY")
            #print(keywordID, vocabulary[keywordID])
