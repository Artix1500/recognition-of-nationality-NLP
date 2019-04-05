import glob
import string

import PyPDF2
import os
import numpy as np
from functools import reduce


def processText(text):
    dictionary = {}
    for word in text.split():
        if word not in dictionary:
            dictionary[word] = 1
        else:
            dictionary[word] += 1

    return dictionary


def splitData(csvContent):
    filenamesInFile = []
    quantitiesList = []
    fileLines = []

    # assuming there is at least one line ended in \n
    existingWords = csvContent[:csvContent.index("\n")].split(',')[1:]

    for line in csvContent.split('\n')[1:]:
        row = line.strip().split(',')
        fileLines.append(row)
        filenamesInFile.append(row[0])
        quantitiesList.append(np.array(row[1:]))
    wordQuantitiesMatrix = np.array(quantitiesList)

    return existingWords, filenamesInFile, fileLines, wordQuantitiesMatrix


def getIndexesOfRowsToBeDeleted(filenamesInFile, rowsToBeDeleted):
    indexes = []
    for filename in rowsToBeDeleted:
        indexes.append(filenamesInFile.index(filename))
    indexes.sort()
    return indexes


def deleteRows(indexesOfRowsToBeDeleted, fileLines, wordQuantitiesMatrix):
    for index in indexesOfRowsToBeDeleted[::-1]:
        del fileLines[index]
        wordQuantitiesMatrix = np.delete(wordQuantitiesMatrix, index, axis=0)
    return fileLines


def readPDFsFromNewFiles(rowsToBeAdded):
    # fileName: its content
    newFilesDicts = {}
    for newFile in rowsToBeAdded:

        # creating an object
        file = open(newFile, 'rb')

        # creating a pdf reader object
        fileReader = PyPDF2.PdfFileReader(file)

        # get number of pages
        num_pages = fileReader.numPages
        count = 0
        text = ""
        # The while loop will read each page
        while count < num_pages:
            pageObj = fileReader.getPage(count)
            count += 1
            text += pageObj.extractText()

        newFilesDicts[newFile] = processText(text)
    return newFilesDicts


def addNewRows(fileLines, newFilesDicts, existingWords, wordQuantitiesMatrix):
    for filename, allwords in newFilesDicts.items():
        # concatenation of strings in python makes new object, thus we have array for now
        newWords = []
        newRowQuantities = []
        for word, quantity in allwords.items():
            if word not in existingWords:
                newWords.append(word)
                newRowQuantities.append(str(quantity))
        existingWords.extend(newWords)

        # this is bad
        rowOfQuantities = str(reduce(lambda x, y: x + "," + y, newRowQuantities))
        fileLines.append(filename + ',' + rowOfQuantities)
        # print("\n\n\n")
        # print(existingWords)

        # add zeros to numpy array


def removeZeroColumns():
    pass


def updateCSV():
    pass


def updateData():
    root_dir = 'data'
    pathToCsv = os.path.join(root_dir, 'data.csv')
    csvFile = open(pathToCsv, 'r+')
    csvContent = csvFile.read().strip()
    csvFile.close()

    existingWords, filenamesInFile, fileLines, wordQuantitiesMatrix = splitData(csvContent)
    filenamesSearched = list(glob.iglob(root_dir + '**/**/*.pdf', recursive=True))
    rowsToBeDeleted = list(set(filenamesInFile) - set(filenamesSearched))
    rowsToBeAdded = list(set(filenamesSearched) - set(filenamesInFile))
    indexesOfRowsToBeDeleted = getIndexesOfRowsToBeDeleted(filenamesInFile, rowsToBeDeleted)

    print(existingWords, filenamesInFile, fileLines, wordQuantitiesMatrix)
    deleteRows(indexesOfRowsToBeDeleted, fileLines, wordQuantitiesMatrix)

    # for only new files:
    newFilesDicts = readPDFsFromNewFiles(rowsToBeAdded)

    addNewRows(fileLines, newFilesDicts, existingWords, wordQuantitiesMatrix)
    removeZeroColumns()
    updateCSV()

    # print(dict)

    # new string (line for data.csv)
    # read lines from dictionary.txt
    # for each word
    #   append to string number and comma
    #   remove this key from dict
    # if dict is not empty after removing known words start updating CSV file
    # For each key in dict
    #   add column to CSV file and put 0 in each line
    #   append number to string and comma
    # after updating CSV append our string to the end of data.CSV
    # print(dict)


#

if __name__ == "__main__":
    updateData()
