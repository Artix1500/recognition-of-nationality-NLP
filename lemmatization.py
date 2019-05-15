import pandas as pd
from nltk.stem import WordNetLemmatizer

# Przyjmuje i zwraca pandas.DataFrame z kolumnami poetykietowanymi słowami

def dataLemmatization(data):
    newWords = []
    allWords = data.columns
    newQuantityDF = pd.DataFrame()
    lemmatizer = WordNetLemmatizer()
    for word in allWords:
        lemmatizedWord = lemmatizer.lemmatize(word)
        if lemmatizedWord in newWords:
            newQuantityDF[lemmatizedWord] += data[word]
        else:
            newWords.append(lemmatizedWord)
            newCol = data[word]
            newQuantityDF = pd.concat([newQuantityDF, pd.DataFrame({lemmatizedWord:newCol})], axis=1)

    return newQuantityDF
