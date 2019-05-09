from keras.models import Sequential
from keras.layers import Dense
import numpy as np


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

    # changes the vector to the need of network
    def processVector(self, vector):
        return vector

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
    def train(self, x, y, nepochs=150, nbatch=self.batchSize):
        self.model.fit(x, y, epochs=nepochs, batch_size=nbatch)

    # evaluates the model, checks how well it predicts
    def evaluate(self, x, y):
        scores = self.model.evaluate(x, y)
        print("\n%s: %.2f%%" % ("text predicted:", scores[1] * 100))

    def predict(self, x):
        predictions = self.model.predict(x)
        # round predictions
        rounded = [round(x[0]) for x in predictions]