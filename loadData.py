import glob
import PyPDF2
import numpy as np


def processText(text):
    dictionary = {}
    for word in text.split():
        if word not in dictionary:
            dictionary[word] = 1
        else:
            dictionary[word] += 1

    key = 'the'
    # print(max(dictionary, key=dictionary.get))
    if key in dictionary:
        print(dictionary[key])
    return dictionary


def load_pdfs():
    root_dir = 'data'
    files = []
    for filename in glob.iglob(root_dir + '**/**/*.pdf', recursive=True):

        # creating an object
        file = open(filename, 'rb')

        # creating a pdf reader object
        fileReader = PyPDF2.PdfFileReader(file)

        # print the number of pages in pdf file
        print(filename)
        # print(fileReader.numPages)
        num_pages = fileReader.numPages
        count = 0
        text = ""
        # The while loop will read each page
        while count < num_pages:
            pageObj = fileReader.getPage(count)
            count += 1
            text += pageObj.extractText()

        dict = processText(text)
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
    load_pdfs()
