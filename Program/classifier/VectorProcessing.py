import pandas as pd
import random
import numpy as np

from Program.classifier.variables import NATIONALITIES


class VectorProcessing:
    def __init__(self, wordCountColumn =1, xStartColumn =3, xEndColumn=-1, pathColumn=-1):
        self.wordCountColumn = wordCountColumn
        self.xStartColumn=xStartColumn
        self.xEndColumn = xEndColumn
        self.pathColumn = pathColumn

    # returns dataset witch is list of dictionaries
    # Term Frequencies
    def CreateDataSet(self, path="SelectedData.csv"):
        data = pd.read_csv(path)
        print(data)
        dataset =[]
        for index, row in data.iterrows():
            wordCount= row[self.wordCountColumn]
            X=row[self.xStartColumn:self.xEndColumn]
            print(X)
            XTF=self.CreateTermFrequencyVector(X,wordCount)
            if XTF is None:
                continue
            # not sure if Y shouldn't be reshaped as well
            dataset.append({"X": np.asarray(XTF).reshape(1, -1), "Y": self.ExtractLabel(row[self.pathColumn])})
        return dataset
 
    # returns nationality label
    def ExtractLabel(self, path):
        catalogs = path.split('/')
        return NATIONALITIES[catalogs[1]]

    # NOT IMPleMENTED!
    def CreateInversedTermFrequencyVector(self, vector):
        return


    def CreateTermFrequencyVector(self, vector, wordCount):
        record = vector
        if wordCount is 0:
            print("Wordcount is 0")
            return None
        if wordCount is None:
            print("WORDCOUNT IS NONE!!!")
            return None
        vectorTF = list(map(lambda x: x / wordCount, record))
        return vectorTF

    # gets the list of dictionary
    # shuffles it
    def ShuffleData(self, data):
        random.shuffle(data)

    # returns splited dataset from path, trainSetRate=trainSetLength/dataSetSize
    def GetData(self, path = "SelectedData.csv", trainSetRate = 0.6):
        dataSet = self.CreateDataSet(path)
        self.ShuffleData(dataSet)
        middlePoint = (int)(len(dataSet)*trainSetRate)
        trainData = dataSet[0:middlePoint]
        testData = dataSet[middlePoint:(len(dataSet)-1)]
        return trainData , testData
    
    def GetVector(self, path ="SelectedData.csv"):
        return self.CreateDataSet(path)
    
