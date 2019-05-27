from Program.classifier.classifier import Classifier
import numpy as np
from Program.classifier.VectorProcessing import VectorProcessing as vp
from Program.classifier.variables import NATIONALITIES

def Run():
    #create classifier
    clf = Classifier(999,len(NATIONALITIES))

    #get data
    trainData , testData = getData()

    #get train data
    trainX = np.array(list(map(lambda x: x['X'][0], trainData)))
    trainY = []
    temp = np.array(list(map(lambda x: x['Y'], trainData)))
    for num in temp:
        tempVector = [0, 0, 0, 0, 0]
        tempVector[num] = 1
        trainY.append(tempVector)
    trainY = np.array(trainY)

    #getting test data
    testX = np.array(list(map(lambda x: x['X'][0], testData)))
    testY = []
    temp = np.array(list(map(lambda x: x['Y'], testData)))
    for num in temp:
        tempVector = [0, 0, 0, 0, 0]
        tempVector[num] = 1
        testY.append(tempVector)
    testY = np.array(testY)
   
    print("before accuracy for testing sets---------------------------------------------------------")
    acc_before_test= clf.testAccuracy(testX, testY)

    print("before accuracy for traing sets----------------------------------------------------------")
    acc_before_train=clf.testAccuracy(trainX, trainY)

    #training on the train data
    clf.train(trainX, trainY, nepochs=30)

    
    print("after accuracy for testing sets----------------------------------------------------------")
    acc_after_test=clf.testAccuracy(testX, testY)

    print("after accuracy for traing sets-----------------------------------------------------------")
    acc_after_train=clf.testAccuracy(trainX, trainY)

    print("results of the training:")
    print("accuracy before trainning of the test data: ", acc_before_test)
    print("accuracy before trainning of the train data: ", acc_before_train)
    print("accuracy after trainning of the test data: ", acc_after_test)
    print("accuracy after trainning of the train data: ", acc_after_train)
    
    #save weights
    clf.save_model()
    

def getData(path="SelectedData.csv"):
    vectorProcesser= vp(wordCountColumn=1, xStartColumn=2,xEndColumn=-1,pathColumn=-1)
    return vectorProcesser.GetData(path)

def getVector(path="SelectedData.csv"):
    vectorProcesser = vp()
    return vectorProcesser.GetData(path)


if __name__ == '__main__':
    Run()
