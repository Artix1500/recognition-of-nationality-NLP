import pandas as pd
from lemmatization import dataLemmatization

def ClearData(pathFrom="data.csv", pathTo="ProcessedData.csv", withLemmatization=False):
    df = pd.DataFrame()

    print("Reading data")
    data = df
    for chunk in pd.read_csv(pathFrom,  chunksize=100):
        data = pd.concat([data, chunk])
    print(data)


    if withLemmatization:
        print("Lemmatization")
        data = dataLemmatization(data)

    print("dropping first column")
    data = data.drop("Unnamed: 0", axis=1)

    print("summing columns")
    summed_colums = data.sum(axis=0, skipna=True)

    print("dropping columns")
    minCount = 10
    data = data[data.columns[data.sum() > minCount]]

    print("saving to file")
    data.to_csv(pathTo)

if __name__ == '__main__':
    ClearData(withLemmatization=True)
