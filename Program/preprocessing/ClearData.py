import pandas as pd
from Program.preprocessing.lemmatization import dataLemmatization

# ClearData clears data from pathFrom csv and saves processed csv to pathTo
# withDropping - drops columns with less than minCount summed words 
# withLemmatization - words lemmatization on
# does return anything
def ClearData(pathFrom="data.csv", pathTo="ProcessedData.csv", withLemmatization=False,  withDropping = False, minCount =10):
    data = pd.DataFrame()

    print("Reading data")
    for chunk in pd.read_csv(pathFrom,  chunksize=100):
        data = pd.concat([data, chunk])

    df=data

   # print("dropping first column")
   # data = data.drop("Unnamed: 0", axis=1)

    if withLemmatization:
        print("Lemmatization")
        data = dataLemmatization(data)
    if withDropping:
        print("summing columns")
        summed_colums = data.sum(axis=0, skipna=True)

        print("dropping columns")
        data = data[data.columns[data.sum() > minCount]]


    #add column with wordCount
    print("adding wordCount Column")
    data['Word_Count'] = data.sum(axis=1, skipna=True)

    print("adding the path_nationality column")
    keyPath = 'path_from_file'
    data['path_from_file']=df[keyPath]

    print("saving to file")
    data.to_csv(pathTo)



if __name__ == '__main__':
    ClearData(withLemmatization=True)
