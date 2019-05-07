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
        return np.ones(shape=self.inputSize)

    def buildModel(self, layer1Size=10, layer2Size=10):
        model = Sequential()
        model.add(Dense(layer1Size, activation="relu", input_dim=self.inputSize))
        model.add(Dense(layer2Size, activation="relu"))
        model.add(Dense(self.outputSize, activation="relu"))
        return model
