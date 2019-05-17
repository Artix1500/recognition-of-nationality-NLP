import wget
import os

# download stanford files
stanford_directory = os.path.join('stanford')
stanford_urls = ['https://www.dropbox.com/s/nl837eto7h3mpe5/stanford-ner.jar',
                 'https://www.dropbox.com/s/dhu2opiomrn8iqr/english.all.3class.distsim.crf.ser.gz']
if not os.path.exists(stanford_directory):
    os.mkdir(stanford_directory)

for url in stanford_urls:
    filename = url.split('/')[-1]
    if not os.path.exists(os.path.join(stanford_directory, filename)):
        wget.download(url, out=stanford_directory)
        print("{} downloaded".format(filename))
    else:
        print("{} already up-to-date".format(filename))

# download nltk punkt files
import nltk
nltk.download('punkt')
