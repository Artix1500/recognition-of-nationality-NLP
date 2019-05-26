from Program.classifier.classifier import Classifier
import numpy as np
from Program.classifier.VectorProcessing import VectorProcessing as vp
from Program.classifier.variables import NATIONALITIES

def Run():
    clf = Classifier(999,len(NATIONALITIES))
    clf.compileModel()
    trainData , testData = getData()

    trainX = np.array(list(map(lambda x: x['X'][0], trainData)))
    trainY = []
    temp = np.array(list(map(lambda x: x['Y'], trainData)))
    for num in temp:
        tempVector = [0, 0, 0, 0, 0]
        tempVector[num] = 1
        trainY.append(tempVector)
    trainY = np.array(trainY)



    testX = np.array(list(map(lambda x: x['X'][0], testData)))
    print(testX)
    testY = []
    temp = np.array(list(map(lambda x: x['Y'], testData)))
    for num in temp:
        tempVector = [0, 0, 0, 0, 0]
        tempVector[num] = 1
        testY.append(tempVector)
    testY = np.array(testY)
   # print(trainX)
   # print(trainY)

   # print(testX)
   # print(testY)
    print("before accuracy for testing sets---------------------------------------------------------")
    acc_before_test= clf.testAccuracy(testX, testY)

    print("before accuracy for traing sets----------------------------------------------------------")
    acc_before_train=clf.testAccuracy(trainX, trainY)

    clf.train(trainX, trainY, nepochs=30)

    
    print("after accuracy for testing sets----------------------------------------------------------")
    acc_after_test=clf.testAccuracy(testX, testY)

    print("after accuracy for traing sets-----------------------------------------------------------")
    acc_after_train=clf.testAccuracy(trainX, trainY)

    print("abtest, abtrain, aatest, aatrain",acc_before_test, acc_before_train, acc_after_test, acc_after_train)

    clf.save_model()
    

   # clf.evaluate(testX, testY)
   
   # print(clf.predict(np.array(testX[0:1])))
   # print(testY[0])

def getData(path="SelectedData.csv"):
    vectorProcesser= vp(wordCountColumn=1, xStartColumn=3,xEndColumn=-1,pathColumn=-1)
    return vectorProcesser.GetData(path)

def getVector(path="SelectedData.csv"):
    vectorProcesser = vp()
    return vectorProcesser.GetData(path)


if __name__ == '__main__':
    Run()
