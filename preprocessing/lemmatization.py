import pandas as pd
from nltk.stem import WordNetLemmatizer

# Przyjmuje i zwraca pandas.DataFrame z kolumnami poetykietowanymi słowami
# WAZNE: urzywa (pierwsza kolumna)Unnamed: 0  jako slowa, trzeba to zmienic
# i pewnie tez word count :<<<<<<<<<<<

def dataLemmatization(data):
    newWords = []
    allWords = data.columns
    newQuantityDF = pd.DataFrame()
    lemmatizer = WordNetLemmatizer()
    i = 0

    if "Unnamed: 0" in allWords:
        newQuantityDF["Unnamed: 0"] = data["Unnamed: 0"]
        i += 1
    if "Word_Count" in allWords:
        newQuantityDF["Word_Count"] = data["Word_Count"]
        i += 1

    for word in allWords[i:]:
        print("New Word "+word)
        lemmatizedWord = lemmatizer.lemmatize(word)
        print("lemmatized word " + word)
        if lemmatizedWord in newWords:
            print("is already in set")
            newQuantityDF[lemmatizedWord] += data[word]
        else:
            print("is not")
            newWords.append(lemmatizedWord)
            newQuantityDF[lemmatizedWord] = data[word]

    return newQuantityDF
