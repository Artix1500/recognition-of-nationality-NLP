import glob
import sys
import string

import os
import numpy as np
import codecs
import csv

import pandas as pd
from nltk import WordNetLemmatizer

import textprocessing as tp
import ner
from tika import parser
from Program.classifier.classifier import Classifier
from Program.classifier.VectorProcessing import VectorProcessing
from Program.preprocessing.ClearData import ClearData
from Program.classifier.variables import NATIONALITIES
from Program.classifier.Run  import getVector
from Program.classifier.WordsExtracting import TakeMatchingWords

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




def updateCSV(existingWords, wordQuantitiesMatrix, paths, pathToCSV):
    rows = []
    # if ',' + bla it needs to be added in numbers to
    # firstRow = ',' + ','.join(existingWords)
    firstRow = "path_from_file," +','.join(existingWords)
    rows.append(firstRow)
    global LineCount
    for i in range(wordQuantitiesMatrix.shape[0]):
        LineCount = LineCount + 1
        quantities = paths[i] +',' + ','.join(map(str, wordQuantitiesMatrix.astype(int)[i, :].tolist()))
        rows.append(quantities)
    finalCSVContent = '\n'.join(rows)
    with codecs.open(pathToCSV, 'w', 'utf-8') as csvFile:

        csvFile.write(finalCSVContent)



def updateData(file, pathToCSV="data.csv"):

    rowsToBeAdded = [file]
    existingWords = []
    wordQuantitiesMatrix= []

    if rowsToBeAdded:
        newFilesDicts = readPDFsFromNewFiles(rowsToBeAdded)
        existingWords, wordQuantitiesMatrix = addNewRows(newFilesDicts, existingWords, wordQuantitiesMatrix)


    updateCSV(existingWords, wordQuantitiesMatrix, paths=rowsToBeAdded,  pathToCSV=pathToCSV)


if __name__ == "__main__":
    lem = True
    wordsLen = 999
    file = input('I need the name of your file: ')
    #file="data/British/somepdf.pdf"
    print(file)
    # I think it reads from the pdf
    updateData(file)
    # data.csv -> ProcessedData.csv
    ClearData(withLemmatization=lem)
    # ProcessedData.csv -> SelectedData.csv
    #WordsExtracting()
    TakeMatchingWords()
    # create classifier
    clf = Classifier(inputSize=wordsLen, outputSize=len(NATIONALITIES))
    # load trained model
    if lem:
        modelpath="modelLem.h5"
    else:
        modelpath="model.h5"
    clf.load_model(modelpath)

    # SelectedData.csv -> vect
    vp = VectorProcessing(wordCountColumn=-2, xStartColumn=0,xEndColumn=-2,pathColumn=-1 )
    vect = vp.GetVector()
    print(vect)
    vectX = vect[0]['X']

    
    score = clf.predict(vectX)
    print(score)
    for key, value in NATIONALITIES.items():
        if value==np.argmax(score):
            print("predicted nationality: ", key)