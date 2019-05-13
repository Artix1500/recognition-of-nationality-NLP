import glob
import sys
import string

import os
import numpy as np
import codecs
import textprocessing as tp
from tika import parser

np.set_printoptions(threshold=sys.maxsize)


def processText(text):
    return tp.create_dictionary(tp.split_to_words(text))


def splitData(csvContent):
    print("Splitting data...")
    filenamesInFile = []
    quantitiesList = []

    # assuming there is at least one line ended in \n

    index = csvContent.index("\n") if "\n" in csvContent else -1
    # print('ex:' + str(len(existingWords)))
    for line in csvContent.split('\n')[1:]:
        row = line.strip().split(',')
        filenamesInFile.append(row[0])
        quantitiesList.append(np.array(row[1:], dtype='uint16'))
    wordQuantitiesMatrix = np.array(quantitiesList)

    return filenamesInFile, wordQuantitiesMatrix


def updateCSV(wordSums, filenamesSearched, wordQuantitiesMatrix, pathToSave):
    print("Concatenating rows...")
    rows = []
    firstRow = 'PATH,WORDCOUNT'
    rows.append(firstRow)
    for i in range(wordQuantitiesMatrix.shape[0]):
        rows.append(filenamesSearched[i] + ',' + wordSums[i])
    finalCSVContent = '\n'.join(rows)

    print("Saving rows to the file...")
    with codecs.open(pathToSave, 'w', 'utf-8') as csvFile:
        csvFile.write(finalCSVContent)
    print("\nWords counted, CSV updated. The file " + pathToSave + " contains " + str(len(wordSums)) + " rows.")


def sumWords(wordQuantitiesMatrix):
    print("Summing rows...")
    temp = wordQuantitiesMatrix.sum(axis=1).tolist()
    return [str(i) for i in temp]


def updateData():
    root_dir = 'data'
    pathToCsv = os.path.join(root_dir, 'data.csv')
    print("Reading data.csv...")
    with codecs.open(pathToCsv, 'r+', 'utf-8') as csvFile:
        csvContent = csvFile.read().strip()

    filenamesInFile, wordQuantitiesMatrix = splitData(csvContent)
    wordSums = sumWords(wordQuantitiesMatrix)

    pathToSave = os.path.join(root_dir, 'wordCount.csv')
    updateCSV(wordSums, filenamesInFile, wordQuantitiesMatrix, pathToSave)


if __name__ == "__main__":
    updateData()
    print('The end')
