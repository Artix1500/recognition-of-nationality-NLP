import pandas as pd


# WordsExtracting - extracts the toCutNumnber-fromCutNumber words that appear the most often
# gets path csv and saves csv to savePath
def WordsExtracting(path="ProcessedData.csv", savePath = "SelectedData.csv", fromCutNumber=0, toCutNumber=999):

   print("Reading data")
   data = pd.read_csv(path)
   df= data
   keyPath="path_from_file"
   print("sorting")
    #print(len(data.sum().sort_values(ascending=False)))
   if "path_from_file" in data.keys():
      data = data.drop("path_from_file", axis=1)
   if "Unnamed: 0" in data.keys():
      keyPath="Unnamed: 0"
      data = data.drop("Unnamed: 0", axis=1)
   data = data.drop("Word_Count", axis=1)

   data = data.reindex(data.sum().sort_values(ascending=False).index, axis=1)

   print("cutting the words")
   data = data.iloc[:, fromCutNumber:toCutNumber]

   print("saving to csv file")
   data['path_from_file'] = df[keyPath]
   data['Word_Count'] = df['Word_Count']

   data.to_csv(savePath)
  

def TakeMatchingWords(pathNewCSV = "ProcessedData.csv", savePath = "SelectedData.csv", trainedDataPath = "classifier/SelectedData.csv"):
   print("Reading new data")
   dataNew = pd.read_csv(pathNewCSV)
   dfNew= dataNew

   print("reading old data")
   dataOld= pd.read_csv(trainedDataPath)


   print("droping path and word count")
   dataNew = dataNew.drop("path_from_file", axis=1)
   dataNew = dataNew.drop("Word_Count", axis=1)
   if "path_from_file" in dataOld.keys():
      dataOld = dataOld.drop("path_from_file", axis=1)
   dataOld = dataOld.drop("Word_Count", axis=1)
   if "Unnamed: 0" in dataOld.keys():
      dataNew = dataNew.drop("Unnamed: 0", axis=1)
      

   print("take the matching words")
   # wez slowa dataOld i wsadz do dataNewToSave
   dataNewToSave = pd.DataFrame(columns=dataOld.keys())
   columnLength=dataNew.shape[0] 
   # iteruj po slwach dataOld
   for key in dataOld.keys():
      # iteruj po kolumnach dataNew
      if key in dataNew.keys():
         # jesli takie samo slowo to przepisz cala kolumne-> continue
         dataNewToSave[key]=dataNew[key]
      else:
         # jesli nie ma tego slowa to dopisz kolumne zer
         dataNewToSave[key] = [0 for i in range(columnLength)]


   print("saving to csv file")
   dataNewToSave['path_from_file'] = dfNew['path_from_file']
   dataNewToSave['Word_Count'] = dfNew['Word_Count']

   dataNewToSave.to_csv(savePath)


if __name__ == '__main__':
   WordsExtracting()