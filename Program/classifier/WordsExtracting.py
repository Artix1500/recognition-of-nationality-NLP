import pandas as pd


# WordsExtracting - extracts the toCutNumnber-fromCutNumber words that appear the most often
# gets path csv and saves csv to savePath
def WordsExtracting(path="ProcessedData.csv", savePath = "SelectedData.csv", fromCutNumber=0, toCutNumber=1000):

   print("Reading data")
   data = pd.read_csv(path)
   df= data
   print("sorting")
    #print(len(data.sum().sort_values(ascending=False)))
   data = data.drop("path_nationality:", axis=1)
   data = data.drop("WordCount", axis=1)

   data = data.reindex(data.sum().sort_values(ascending=False).index, axis=1)

   print("cutting the words")
   data = data.iloc[:, fromCutNumber:toCutNumber]

   print("saving to csv file")
   data['path_nationality:'] = df['path_nationality:']
   data['WordCount'] = df['WordCount']

   data.to_csv(savePath)
   # return data
