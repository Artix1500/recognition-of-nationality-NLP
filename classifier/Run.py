from classifier import Classifier
import numpy as np
from VectorProcessing import VectorProcessing as vp


def Run():
    clf = Classifier(2,999,5)
    clf.compileModel()
    trainData , testData = getData()

    # print(len(trainData))
    # print(trainData[55]['X'])
    # print(len(testData))

    # X, Y = CreateSomeData(xSize=10, howMany=5)

    trainX = np.array(list(map(lambda x: x['X'][0], trainData)))
    trainY = np.array(list(map(lambda x: x['Y'], trainData)))
    testX = np.array(list(map(lambda x: x['X'][0], testData)))
    testY = np.array(list(map(lambda x: x['Y'], testData)))

    clf.train(trainX, trainY)
    clf.evaluate(testX, testY)


def getData(path="SelectedData.csv"):
    vectorProcesser= vp()
    return vectorProcesser.GetData(path)

Run()
