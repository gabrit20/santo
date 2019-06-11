import codecs

def allvocabulariesInit():
    global vocGeneric
    vocGeneric = {}
    global vocSources
    vocSources = {}
    global vocTopics
    vocTopics = {}
    global vocPeople
    vocPeople = {}
    Nlanguages = 4
    entry = {}
    
    #print("Generic")
    file = codecs.open('allvocabulariesGeneric.csv', encoding='latin-1') #used to be utf-8
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
            vocGeneric[keywordID] = entry
            #print("ENTRY")
            #print(keywordID, vocGeneric[keywordID])
    file.close()

    #print("Sources")
    file = codecs.open('allvocabulariesSources.csv', encoding='latin-1')
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
            vocSources[keywordID] = entry
            #print("ENTRY")
            #print(keywordID, vocSources[keywordID])
    file.close()

    #print("Topics")
    file = codecs.open('allvocabulariesTopics.csv', encoding='latin-1')
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
            vocTopics[keywordID] = entry
            #print("ENTRY")
            #print(keywordID, vocTopics[keywordID])
    file.close()

    #print("People")
    file = codecs.open('allvocabulariesPeople.csv', encoding='latin-1')
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
            vocPeople[keywordID] = entry
            #print("ENTRY")
            #print(keywordID, vocPeople[keywordID])
    file.close()


#allvocabulariesInit()
#print(vocabularyPeople)
