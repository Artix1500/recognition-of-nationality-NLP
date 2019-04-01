import glob
import textract


def load_pdfs():
    root_dir = 'data'
    files = []
    for filename in glob.iglob(root_dir + '**/**/*.pdf', recursive=True):
        print(filename)
        text = textract.process(filename)
        print(text)


load_pdfs()