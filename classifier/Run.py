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
    trainY = []
    temp = np.array(list(map(lambda x: x['Y'], trainData)))
    for num in temp:
        tempVector = [0, 0, 0, 0, 0]
        tempVector[num] = 1
        trainY.append(tempVector)
    trainY = np.array(trainY)

    testX = np.array(list(map(lambda x: x['X'][0], testData)))
    testY = []
    temp = np.array(list(map(lambda x: x['Y'], testData)))
    for num in temp:
        tempVector = [0, 0, 0, 0, 0]
        tempVector[num] = 1
        testY.append(tempVector)
    testY = np.array(testY)

    clf.train(trainX, trainY)
    clf.evaluate(testX, testY)

    print(clf.predict(np.array(testX[0:1])))
    print(testY[0])

def getData(path="SelectedData.csv"):
    vectorProcesser= vp()
    return vectorProcesser.GetData(path)

Run()
