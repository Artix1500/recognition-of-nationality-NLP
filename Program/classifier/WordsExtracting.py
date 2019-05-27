import pandas as pd


# WordsExtracting - extracts the toCutNumnber-fromCutNumber words that appear the most often
# gets path csv and saves csv to savePath
# xendcolumn not included -> if you want the last piece as well =None
def WordsExtracting(path="../preprocessing/ProcessedData.csv", savePath = "SelectedData.csv", fromCutNumber=0, toCutNumber=999,wordCountColumn=-1, xStartColumn =1, xEndColumn=-1, pathColumn=0):

   print("Reading data")
   data = pd.read_csv(path)
   df= data

   if xEndColumn is not None:
      data = data.iloc[:, xStartColumn:xEndColumn]
   else:
      data = data.iloc[:, xStartColumn:]
  

   print("sorting")
   
   data = data.reindex(data.sum().sort_values(ascending=False).index, axis=1)

   print("cutting the words")
   data = data.iloc[:, fromCutNumber:toCutNumber]

   
   data['Word_Count'] = df[(list(df.columns))[wordCountColumn]]
   data['path_from_file'] = df[(list(df.columns))[pathColumn]]
   
   print("saving to csv file")
   data.to_csv(savePath, index=False)
  

# parameters for column indeces
# wordCountColumnNew - where in pathNewCSV is the Word_Count column 
# pathColumnNew - where is the path column
# xStartColumnNew - where the words start in the new file
# xEndColumnNew - where the words end in the new file + 1 (not included) if you want the last piece as well =None )
# Old by analogy

def TakeMatchingWords(pathNewCSV = "ProcessedData.csv", savePath = "SelectedData.csv", trainedDataPath = "classifier/SelectedData.csv",wordCountColumnNew=-1, xStartColumnNew =1, xEndColumnNew=-1, pathColumnNew=0, xStartColumnOld=1, xEndColumnOld=-1):
   print("Reading new data")
   dataNew = pd.read_csv(pathNewCSV)
   dfNew= dataNew
   
   print("reading old data")
   dataOld= pd.read_csv(trainedDataPath)


   print("droping path and word count")
   if xEndColumnOld is not None:
      dataOld = dataOld.iloc[:, xStartColumnOld:xEndColumnOld]
   else:
      dataOld = dataOld.iloc[:, xStartColumnOld:]

   if xEndColumnNew is not None:
      dataNew = dataNew.iloc[:, xStartColumnNew:xEndColumnNew]
   else:
      dataNew = dataNew.iloc[:, xStartColumnNew:]

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


   dataNewToSave['Word_Count'] = dfNew[(list(dfNew.columns))[wordCountColumnNew]]
   dataNewToSave['path_from_file'] = dfNew[(list(dfNew.columns))[pathColumnNew]]

   print("saving to csv file")
   dataNewToSave.to_csv(savePath, index=False)


if __name__ == '__main__':
   WordsExtracting()