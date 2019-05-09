class VectorProcessing:
    # returns nationality
    def CreateLabels(self, vector):
        path = vector[0]
        catalogs = path.split('/')
        return catalogs[1]

    def CreateTermFrequencyVector(self, vector):
        record = vector[2:-1]
        wordCount = vector[1]
        vectorTF = list(map(lambda x: x / wordCount, record))
        return vectorTF

    # labels to digits


    #inverse frequency
    # topics