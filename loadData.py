import glob
import sys
import string

import os
import numpy as np
import codecs
import textprocessing as tp
import ner
from tika import parser

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
            print(str(FileCount) + '\t')
        except KeyError:
            print("KEYERROR in " + newFile)
        except UnicodeEncodeError:
            print("UnicodeEncodeError in " + newFile)
        except:
            print("STH ELSE WENT WRONG!")

    return newFilesDicts


def addNewRows(newFilesDicts, existingWords, wordQuantitiesMatrix):
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
            print(filename + " is being processed")
            newMatrix[:-1, :-len(newWords)] = wordQuantitiesMatrix
        else:
            print("! " + filename + " DID NOT add any new words")
            newMatrix[:-1, :] = wordQuantitiesMatrix

        for k, v in existingWordsQuantities.items():
            newMatrix[-1, existingWords.index(k)] = v

        newMatrix[-1, oldWordsLength:] = newRowQuantities
        wordQuantitiesMatrix = newMatrix
    return existingWords, wordQuantitiesMatrix


def removeZeroColumns(existingWords, wordQuantitiesMatrix):
    print("Removing columns...")
    indexesToDelete = list(np.argwhere(np.all(wordQuantitiesMatrix[..., :] == 0, axis=0)).flat)
    indexesToDelete.sort()
    indexesToDelete.reverse()

    oldCount = wordQuantitiesMatrix.shape[1]
    wordQuantitiesMatrix = np.delete(wordQuantitiesMatrix, indexesToDelete, 1)
    newCount = wordQuantitiesMatrix.shape[1]

    if oldCount != newCount:
        print("Dictionary shortened from " + str(oldCount) + " to " + str(newCount))

    for index in indexesToDelete:
        del existingWords[index]

    return existingWords, wordQuantitiesMatrix


def updateCSV(existingWords, filenamesSearched, wordQuantitiesMatrix, pathToCsv):
    rows = []
    firstRow = ',' + ','.join(existingWords)
    rows.append(firstRow)
    global LineCount
    for i in range(wordQuantitiesMatrix.shape[0]):
        print("SAVE the: " + str(LineCount) + " line to rows var")
        LineCount = LineCount + 1
        quantities = ','.join(map(str, wordQuantitiesMatrix.astype(int)[i, :].tolist()))
        rows.append(filenamesSearched[i] + ',' + quantities)
    finalCSVContent = '\n'.join(rows)

    print("SAVE the rows to file")
    with codecs.open(pathToCsv, 'w', 'utf-8') as csvFile:
        csvFile.write(finalCSVContent)
    print("\nCSV updated. Now containing " + str(len(existingWords)) + " words and " + str(
        wordQuantitiesMatrix.shape[0]) + " files")


def updateData():
    root_dir = 'data'
    pathToCsv = os.path.join(root_dir, 'data.csv')
    with codecs.open(pathToCsv, 'r+', 'utf-8') as csvFile:
        csvContent = csvFile.read().strip()

    existingWords, filenamesInFile, wordQuantitiesMatrix = splitData(csvContent)
    filenamesSearched = list(glob.iglob(root_dir + '**/**/*.pdf', recursive=True))
    filenamesSearched.sort()
    rowsToBeDeleted = list(set(filenamesInFile) - set(filenamesSearched))
    rowsToBeDeleted.sort()
    rowsToBeAdded = list(set(filenamesSearched) - set(filenamesInFile))
    rowsToBeAdded.sort()

    print("\nFiles found in filesystem: " + str(filenamesSearched))
    print("Files to be added to CSV: " + str(rowsToBeAdded))
    print("Files to be deleted from CSV: " + str(rowsToBeDeleted))

    if not rowsToBeAdded and not rowsToBeDeleted:
        print("\nNothing to be changed")
        print(
            "Now CSV contains " + str(len(existingWords)) + " words and " + str(
                wordQuantitiesMatrix.shape[0]) + " files")
        return

    indexesOfRowsToBeDeleted = getIndexesOfRowsToBeDeleted(filenamesInFile, rowsToBeDeleted)
    wordQuantitiesMatrix = deleteRows(indexesOfRowsToBeDeleted, wordQuantitiesMatrix)
    if rowsToBeAdded:
        print("Reading PDFs...")
        newFilesDicts = readPDFsFromNewFiles(rowsToBeAdded)
        existingWords, wordQuantitiesMatrix = addNewRows(newFilesDicts, existingWords, wordQuantitiesMatrix)

    if wordQuantitiesMatrix.size != 0 and rowsToBeDeleted.__len__() > 0:
        existingWords, wordQuantitiesMatrix = removeZeroColumns(existingWords, wordQuantitiesMatrix)

    # to get the proper order of rows in CSV
    filenames = [x for x in filenamesInFile if x not in rowsToBeDeleted]
    filenames.extend(rowsToBeAdded)

    if wordQuantitiesMatrix.size == 0:
        existingWords.clear()

    updateCSV(existingWords, filenames, wordQuantitiesMatrix, pathToCsv)


if __name__ == "__main__":
    updateData()
    print('The end')
