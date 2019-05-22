import glob
import sys
import string

import os
import numpy as np
import codecs

import pandas as pd
from nltk import WordNetLemmatizer

import textprocessing as tp
import ner
from tika import parser
from classifier import Classifier

np.set_printoptions(threshold=sys.maxsize)

FileCount = 0
LineCount = 0


def processText(text):
    return tp.create_dictionary(tp.split_to_words(text))


def splitData(csvContent):
    filenamesInFile = []
    quantitiesList = []

    # assuming there is at least one line ended in \n

    index = csvContent.index("\n") if "\n" in csvContent else -1
    existingWords = [] if index == -1 else csvContent[:index].split(',')[1:]
    # print('ex:' + str(len(existingWords)))
    for line in csvContent.split('\n')[1:]:
        row = line.strip().split(',')
        filenamesInFile.append(row[0])
        quantitiesList.append(np.array(row[1:], dtype='uint16'))
    wordQuantitiesMatrix = np.array(quantitiesList)

    return existingWords, filenamesInFile, wordQuantitiesMatrix


def getIndexesOfRowsToBeDeleted(filenamesInFile, rowsToBeDeleted):
    indexes = []
    for filename in rowsToBeDeleted:
        indexes.append(filenamesInFile.index(filename))
    indexes.sort()
    return indexes


# probably unnecessary to delete fileLines
def deleteRows(indexesOfRowsToBeDeleted, wordQuantitiesMatrix):
    for index in indexesOfRowsToBeDeleted[::-1]:
        wordQuantitiesMatrix = np.delete(wordQuantitiesMatrix, index, axis=0)
    return wordQuantitiesMatrix


def readPDFsFromNewFiles(rowsToBeAdded):
    # fileName: its content
    newFilesDicts = {}
    for newFile in rowsToBeAdded:
        global FileCount
        try:
            FileCount = FileCount + 1
            text = parser.from_file(newFile)
            newFilesDicts[newFile] = processText(text['content'])
        except KeyError:
            print("KEYERROR in " + newFile)
        except UnicodeEncodeError:
            print("UnicodeEncodeError in " + newFile)
        except:
            print("STH ELSE WENT WRONG!")

    return newFilesDicts


def addNewRows(newFilesDicts, existingWords, wordQuantitiesMatrix):
    wordQuantitiesMatrix = np.array([])
    for filename, allwords in newFilesDicts.items():
        # concatenation of strings in python makes new object, thus we have array for now
        newWords = []
        newRowQuantities = []
        existingWordsQuantities = {}
        oldWordsLength = len(existingWords)
        for word, quantity in allwords.items():
            if word not in existingWords:
                newWords.append(word)
                newRowQuantities.append(quantity)
            else:
                existingWordsQuantities[word] = quantity

        existingWords.extend(newWords)

        newMatrix = np.zeros((wordQuantitiesMatrix.shape[0] + 1, len(existingWords)), dtype="uint16")
        if newWords:
            newMatrix[:-1, :-len(newWords)] = wordQuantitiesMatrix
        else:
            newMatrix[:-1, :] = wordQuantitiesMatrix

        for k, v in existingWordsQuantities.items():
            newMatrix[-1, existingWords.index(k)] = v

        newMatrix[-1, oldWordsLength:] = newRowQuantities
        wordQuantitiesMatrix = newMatrix
    return existingWords, wordQuantitiesMatrix




def updateCSV(existingWords, wordQuantitiesMatrix, pathToCsv):
    rows = []
    firstRow = ',' + ','.join(existingWords)
    rows.append(firstRow)
    global LineCount
    for i in range(wordQuantitiesMatrix.shape[0]):
        LineCount = LineCount + 1
        quantities = ','.join(map(str, wordQuantitiesMatrix.astype(int)[i, :].tolist()))
        rows.append(quantities)
    finalCSVContent = '\n'.join(rows)

    with codecs.open(pathToCsv, 'w', 'utf-8') as csvFile:
        csvFile.write(finalCSVContent)



def updateData(file):

    rowsToBeAdded = [file]
    existingWords = []
    wordQuantitiesMatrix= []

    if rowsToBeAdded:
        newFilesDicts = readPDFsFromNewFiles(rowsToBeAdded)
        existingWords, wordQuantitiesMatrix = addNewRows(newFilesDicts, existingWords, wordQuantitiesMatrix)

    updateCSV(existingWords, wordQuantitiesMatrix, "data.csv")


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
        lemmatizedWord = lemmatizer.lemmatize(word)
        if lemmatizedWord in newWords:
            newQuantityDF[lemmatizedWord] += data[word]
        else:
            newWords.append(lemmatizedWord)
            newQuantityDF[lemmatizedWord] = data[word]

    return newQuantityDF


def ClearData(pathFrom="data.csv", pathTo="ProcessedData.csv", withLemmatization=False):
    df = pd.DataFrame()

    data = df
    for chunk in pd.read_csv(pathFrom,  chunksize=100):
        data = pd.concat([data, chunk])

    data = dataLemmatization(data)

    return data


if __name__ == "__main__":
    print('Hello ! ')
    file = input('I need the name of your file: ')
    print(file)
    updateData(file)
    dataFromPdf = ClearData()

    clf = Classifier(2, 999, 5)
    clf.compileModel()
    clf.load_model("model.h5")

    df = pd.DataFrame()

    dataForAlgorithm = df
    for chunk in pd.read_csv("dataForAlgorithm.csv",  chunksize=100 , nrows=1):
        dataForAlgorithm = pd.concat([dataForAlgorithm, chunk])



    dataForAlgorithm = dataForAlgorithm.drop("Unnamed: 0", axis=1)

    dataForAlgorithm = dataForAlgorithm.drop("Unnamed: 0.1", axis=1)

    dataForAlgorithm = dataForAlgorithm.drop("path_from_file", axis=1)

    vect = []

    for key in dataForAlgorithm.keys():
        if key in dataFromPdf.keys():
            vect.append(dataFromPdf[key][0])
        else:
            vect.append(0)


    vect = vect[1:1000]

    vect = [[vect]]

    score = clf.predict(vect)

    NATIONALITIES = ["0: British", "1: Chinese", "2: French", "3: Polish", "4: Russian"]

    print(NATIONALITIES)
    print(score)
