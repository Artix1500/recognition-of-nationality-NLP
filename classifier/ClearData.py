import pandas as pd

print("Reading data")
data = pd.read_csv("data.csv")
print("dropping first column")
data = data.drop("Unnamed: 0", axis=1)

#print(data.head())
print("summing columns")
summed_colums = data.sum(axis=0, skipna=True)
#print(summed_colums)

print("dropping columns")
minCount = 10
data = data[data.columns[data.sum() > minCount]]

# data = data.drop(summed_colums[summed_colums.score < minCount].index)
# data = data.drop([col for col, val in data.sum().iteritems() if val < minCount], axis=1, inplace=True)
#print(data)

print("saving to file")
data.to_csv("ProcessedData.csv")
