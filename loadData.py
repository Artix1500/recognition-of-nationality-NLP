import glob
import sys
import os
import numpy as np
import codecs
from tika import parser
from sentences_processor import process_PDF_content

np.set_printoptions(threshold=sys.maxsize)

# logging variables
FileCount = 0
LineCount = 0


# read data from csv file and save it into python variables using lists and numpy.ndarray
def splitData(csvContent):
    filenamesInFile = []
    quantitiesList = []

    # we assume there is at least one line ending with \n
    index = csvContent.index("\n") if "\n" in csvContent else -1
    existingWords = [] if index == -1 else csvContent[:index].split(',')[1:]
    # read all lines of data.csv and extract values between commas
    for line in csvContent.split('\n')[1:]:
        row = line.strip().split(',')
        filenamesInFile.append(row[0])
        quantitiesList.append(np.array(row[1:], dtype='uint16'))
    wordQuantitiesMatrix = np.array(quantitiesList)

    return existingWords, filenamesInFile, wordQuantitiesMatrix


# search for indexes of rows to be deleted, keeping the right order
def getIndexesOfRowsToBeDeleted(filenamesInFile, rowsToBeDeleted):
    indexes = []
    for filename in rowsToBeDeleted:
        indexes.append(filenamesInFile.index(filename))
    indexes.sort()
    return indexes


# delete rows of files no longer found in data/ folder
def deleteRows(indexesOfRowsToBeDeleted, wordQuantitiesMatrix):
    for index in indexesOfRowsToBeDeleted[::-1]:
        wordQuantitiesMatrix = np.delete(wordQuantitiesMatrix, index, axis=0)
    return wordQuantitiesMatrix


# create dictionary (pdf_filename: processed words of this pdf)
def readPDFsFromNewFiles(rowsToBeAdded):
    # fileName: its content
    newFilesDicts = {}
    for newFile in rowsToBeAdded:
        global FileCount
        try:
            FileCount = FileCount + 1
            text = parser.from_file(newFile)
            print("PFD number: " + str(FileCount) + ') ' + str(newFile) + " is being processed")
            newFilesDicts[newFile] = process_PDF_content(text['content'])
        except KeyError:
            print("KEYERROR in " + newFile)
        except UnicodeEncodeError:
            print("UnicodeEncodeError in " + newFile)
        except:
            print("STH ELSE WENT WRONG!")

    return newFilesDicts


# enlarge matrix containing quantities of words, extend list of all words
def addNewRows(newFilesDicts, existingWords, wordQuantitiesMatrix):
    for filename, allwords in newFilesDicts.items():
        newWords = []
        newRowQuantities = []
        existingWordsQuantities = {}
        oldWordsLength = len(existingWords)
        # create dictionary/update quantity of word
        for word, quantity in allwords.items():
            if word not in existingWords:
                newWords.append(word)
                newRowQuantities.append(quantity)
            else:
                existingWordsQuantities[word] = quantity

        existingWords.extend(newWords)

        # make new bigger matrix with zeros, then put old matrix into the bigger one
        newMatrix = np.zeros((wordQuantitiesMatrix.shape[0] + 1, len(existingWords)), dtype="uint16")
        if newWords:
            print(filename + " added " + str(len(existingWords) - oldWordsLength) + " new words")
            newMatrix[:-1, :-len(newWords)] = wordQuantitiesMatrix
        else:
            print(filename + " DID NOT add any new words")
            newMatrix[:-1, :] = wordQuantitiesMatrix

        # add quantities of the words in new PDF row
        for k, v in existingWordsQuantities.items():
            newMatrix[-1, existingWords.index(k)] = v

        newMatrix[-1, oldWordsLength:] = newRowQuantities
        wordQuantitiesMatrix = newMatrix
    return existingWords, wordQuantitiesMatrix


# delete zero columns (after deleting some pdf from data/ folder)
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


# creates rows to save to file in such manner: path,item1_quantity,item2_quantity...
def updateCSV(existingWords, filenamesSearched, wordQuantitiesMatrix, pathToCsv):
    rows = []
    # create first row
    firstRow = ',' + ','.join(existingWords)
    rows.append(firstRow)
    global LineCount
    # create rows from collected data for each file
    for i in range(wordQuantitiesMatrix.shape[0]):
        print("Append line nr " + str(LineCount))
        LineCount = LineCount + 1
        quantities = ','.join(map(str, wordQuantitiesMatrix.astype(int)[i, :].tolist()))
        rows.append(filenamesSearched[i] + ',' + quantities)
    finalCSVContent = '\n'.join(rows)

    print("SAVE the rows to file")
    with codecs.open(pathToCsv, 'w', 'utf-8') as csvFile:
        csvFile.write(finalCSVContent)
    print("\nCSV updated. Now containing " + str(len(existingWords)) + " words and " + str(
        wordQuantitiesMatrix.shape[0]) + " files")


# loads csv file, searches for new files and updates data.csv file with dictionary and word quantities
def updateData():
    root_dir = 'data'
    pathToCsv = os.path.join(root_dir, 'data.csv')
    with codecs.open(pathToCsv, 'r+', 'utf-8') as csvFile:
        csvContent = csvFile.read().strip()

    # read data from csv file and save it into python variables
    existingWords, filenamesInFile, wordQuantitiesMatrix = splitData(csvContent)
    # search for pdf files to add
    filenamesSearched = list(glob.iglob(root_dir + '**/**/*.pdf', recursive=True))
    # sort filenames to keep the order of files ant to not modify them in csv file
    filenamesSearched.sort()
    rowsToBeDeleted = list(set(filenamesInFile) - set(filenamesSearched))
    rowsToBeDeleted.sort()
    rowsToBeAdded = list(set(filenamesSearched) - set(filenamesInFile))
    rowsToBeAdded.sort()

    print("\nFiles found in filesystem: " + str(len(filenamesSearched)))
    print("Files to be added to CSV: " + str(len(rowsToBeAdded)))
    print("Files to be deleted from CSV: " + str(len(rowsToBeDeleted)))

    # return early if no changes to PDFs in file system detected
    if not rowsToBeAdded and not rowsToBeDeleted:
        print("\nNothing to be changed")
        print(
            "Now CSV contains " + str(len(existingWords)) + " words and " + str(
                wordQuantitiesMatrix.shape[0]) + " files")
        return

    # delete old rows (files that no longer exist in data/ folder)
    indexesOfRowsToBeDeleted = getIndexesOfRowsToBeDeleted(filenamesInFile, rowsToBeDeleted)
    wordQuantitiesMatrix = deleteRows(indexesOfRowsToBeDeleted, wordQuantitiesMatrix)
    # add new rows, enlarge word dictionary
    if rowsToBeAdded:
        print("Reading PDFs...")
        newFilesDicts = readPDFsFromNewFiles(rowsToBeAdded)
        existingWords, wordQuantitiesMatrix = addNewRows(newFilesDicts, existingWords, wordQuantitiesMatrix)

    # delete potential zero columns (after deleting some pdf from data/ folder)
    if wordQuantitiesMatrix.size != 0 and rowsToBeDeleted.__len__() > 0:
        existingWords, wordQuantitiesMatrix = removeZeroColumns(existingWords, wordQuantitiesMatrix)

    # get the proper order of rows in CSV
    filenames = [x for x in filenamesInFile if x not in rowsToBeDeleted]
    filenames.extend(rowsToBeAdded)

    # clear dictionary if there are no PDFs in data/
    if wordQuantitiesMatrix.size == 0:
        existingWords.clear()

    # save/update data to data.csv file
    updateCSV(existingWords, filenames, wordQuantitiesMatrix, pathToCsv)


if __name__ == "__main__":
    updateData()
    print('The end')
