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
    for word in allWords:
        print("New Word "+word)
        lemmatizedWord = lemmatizer.lemmatize(word)
        print("lemmatized word " + word)
        if lemmatizedWord in newWords:
            print("is already in set")
            newQuantityDF[lemmatizedWord] += data[word]
        else:
            print("is not")
            newWords.append(lemmatizedWord)
            newCol = data[word]
            newQuantityDF = pd.concat([newQuantityDF, pd.DataFrame({lemmatizedWord:newCol})], axis=1)
    return newQuantityDF
