import glob

def load_pdfs():
    root_dir = 'data'
    files = []
    for filename in glob.iglob(root_dir + '**/**/*.pdf', recursive=True):
        files.append(filename)
        print(filename)

load_pdfs()