from classifier import Classifier
import numpy as np
from VectorProcessing import VectorProcessing as vp


def Run():
    clf = Classifier(2,999,5)
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
    
    #clf.train(trainX, trainY, nepochs=50)
    #print("after accuracy for testing sets 2----------------------------------------------------------")
    #acc_after_test=clf.testAccuracy(testX, testY)

    #print("after accuracy for traing sets 2-----------------------------------------------------------")
    #acc_after_train=clf.testAccuracy(trainX, trainY)

   # print("abtest, abtrain, aatest, aatrain 2",acc_after_test, acc_after_train)
    
   # clf.train(trainX, trainY, nepochs=50)
   # print("after accuracy for testing sets 3----------------------------------------------------------")
   # acc_after_test=clf.testAccuracy(testX, testY)

  #  print("after accuracy for traing sets 3-----------------------------------------------------------")
 #   acc_after_train=clf.testAccuracy(trainX, trainY)

  #  print("abtest, abtrain, aatest, aatrain 3",acc_after_test, acc_after_train)
    
  #  clf.train(trainX, trainY, nepochs=50)
  #  print("after accuracy for testing sets 4----------------------------------------------------------")
  #  acc_after_test=clf.testAccuracy(testX, testY)

   # print("after accuracy for traing sets 4-----------------------------------------------------------")
   # acc_after_train=clf.testAccuracy(trainX, trainY)

  #  print("abtest, abtrain, aatest, aatrain 4",acc_after_test, acc_after_train)






   # clf.evaluate(testX, testY)
   
   # print(clf.predict(np.array(testX[0:1])))
   # print(testY[0])

def getData(path="SelectedData.csv"):
    vectorProcesser= vp()
    return vectorProcesser.GetData(path)

Run()
