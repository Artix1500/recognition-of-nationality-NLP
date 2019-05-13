import pandas as pd

path = "ProcessedData.csv"
savePath = "SelectedData.csv"

print("Reading data")
data = pd.DataFrame()
for chunk in pd.read_csv(path,  chunksize=100):
    data = pd.concat([data, chunk])
    print(data)


wc = data['path_from_file']

data = data.drop("path_from_file", axis=1)

print("sorting")

print(len(data.sum().sort_values(ascending=False)))
data = data.reindex(data.sum().sort_values(ascending=False).index, axis=1)

print("cutting the words")
cutNumber = 1001
data = data.iloc[:, 0:cutNumber]


e = wc[:]
data['path_from_file'] = e.values

print("saving to file")
data.to_csv(savePath)