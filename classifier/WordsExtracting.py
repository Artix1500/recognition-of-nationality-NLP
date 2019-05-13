import pandas as pd

path = "ProcessedData.csv"
savePath = "SelectedData.csv"

print("Reading data")
data = pd.read_csv(path)

print("sorting")

print(len(data.sum().sort_values(ascending=False)))
data = data.reindex(data.sum().sort_values(ascending=False).index, axis=1)

print("cutting the words")
cutNumber = 1000
data = data.iloc[:, 0:cutNumber]


print("saving to file")
data.to_csv(savePath)
