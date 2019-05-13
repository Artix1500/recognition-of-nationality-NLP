from classifier import Classifier
import numpy as np


def Run():
    clf = Classifier()
    clf.compileModel()
    X, Y = CreateSomeData(xSize=10, howMany=5)
    clf.train(X, Y)
    clf.evaluate(X, Y)


def CreateSomeData(xSize, howMany):
    xList = []
    yList = []
    for i in range(howMany):
        xList.append(np.ones(shape=xSize))
        yList = np.array([1])
    return list(xList, yList)


Run()
