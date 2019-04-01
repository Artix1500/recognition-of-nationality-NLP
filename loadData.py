import glob
import PyPDF2

def load_pdfs():
    root_dir = 'data'
    files = []
    for filename in glob.iglob(root_dir + '**/**/*.pdf', recursive=True):

        # creating an object
        file = open(filename, 'rb')

        # creating a pdf reader object
        fileReader = PyPDF2.PdfFileReader(file)

        # print the number of pages in pdf file
        print(filename)
        print(fileReader.numPages)
        num_pages = fileReader.numPages
        count = 0
        text = ""
        # The while loop will read each page
        while count < num_pages:
            pageObj = fileReader.getPage(count)
            count += 1
            text += pageObj.extractText()

        print(text)


if __name__ == "__main__":
    load_pdfs()