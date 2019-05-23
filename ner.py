from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os

root_dir = 'stanford'
path1 = os.path.join(root_dir, 'english.all.3class.distsim.crf.ser.gz')
path2 = os.path.join(root_dir, 'stanford-ner.jar')

st = StanfordNERTagger(path1,
                       path2,
                       encoding='utf-8')


def properNounsOut(rawtext):
    tokenized_text = word_tokenize(rawtext)
    classified_text = st.tag(tokenized_text)
    words = []

    for taggedWord in classified_text:
        if taggedWord[1] == 'O':
            words.append(taggedWord[0])
        # else:
        #     print("WYWALAM: " + taggedWord[0])

    return words

# words = properNounsOut("Mark and Derek work at Google, therefore me and other 5463524 people too!")
# print(words)