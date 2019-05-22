from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import os
from VectorProcessing import VectorProcessing as vp

# from loadData import processText


class Classifier:
    # batchSize - how many samples at once
    # inputSize - how long input vector
    # outputSize - how big output - how many nationalities
    def __init__(self, batchSize, inputSize, outputSize):
        self.batchSize = batchSize
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.model = self.buildModel()

    # builds a model, the hidden layers' size can be customized
    def buildModel(self, layer1Size=10, layer2Size=10):
        model = Sequential()
        model.add(Dense(layer1Size, activation="relu", input_dim=self.inputSize))
        model.add(Dense(layer2Size, activation="relu"))
        model.add(Dense(self.outputSize, activation="sigmoid"))
        return model

    def compileModel(self):
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # trains the model
    # x - data
    # y - labels
    # nepochs - how many iterations
    # nbatch - the number of instances that are evaluated before
    # a weight update in the network is performed
    def train(self, x, y, nepochs=300, nbatch=2):
        self.model.fit(x, y, epochs=nepochs, batch_size=nbatch, verbose=0)

    # evaluates the model, checks how well it predicts
    def evaluate(self, x, y):
        scores = self.model.evaluate(x, y)
        print("\n%s: %.2f%%" % ("text predicted:", scores[1] * 100))
        
    def testAccuracy(self, x, y):
        predictions = []
        good= 0
        all_pieces= len(x)
        
        for one_x in x:
            predictions.append(self.model.predict(np.asarray(one_x).reshape(1, -1)))
        for i in range(all_pieces):
           # print("label: ", y[i])
           # print("predicted: ", predictions[i])
            if np.argmax(predictions[i]) == np.argmax(y[i]):
            #    print("goooood")
                good+=1
        acc = good/all_pieces
        print("accuracy: ", acc)    
        return acc
        


    def predict(self, x):
        predictions = self.model.predict(x)
        # round predictions
        rounded = [round(x[0]) for x in predictions]
        return predictions

    # Gets weights for model from file
    # Returns true if success
    def load_model(self, filename):
        exists = os.path.isfile(filename)
        if exists:
            print("loading model")
            self.model.load_weights(filename)

    # Saves weights of trained model to file->path is path to that file
    # Returns true if success
    def save_model(self, filename='model.h5'):
        print("saving model")
        self.model.save_weights(filename)
