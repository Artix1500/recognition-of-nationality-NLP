import numpy as np
import lda
import lda.datasets


def topicExtractring(topicsCount=1000,n_top_words=8):

    #redcsv Sdata.csv
    print("start")
    X = lda.datasets.load_reuters() # it is a ready DTM
    #X=(N(iletekstow) x liczbe total words )
    #X[0][0] = w pierwszym tekscie ile jest pierwszego slowa
    print(X.shape)
    print(X[0][1:100])

    vocab = lda.datasets.load_reuters_vocab()
    #print(vocab.shape)
    # (slowo1,slowo2,slowo3)
    print(vocab)
    
    titles = lda.datasets.load_reuters_titles()
    #print(titles.shape)
    
    # (title1,title2,title3)
    print(titles)
    
    '''
    #create lda model
    model = lda.LDA(n_topics=topicsCount, n_iter=1500, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available

    topic_word = model.topic_word_  # model.components_ also works
    
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))


    doc_topic = model.doc_topic_
    for i in range(10):
        print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
    '''

if __name__ == '__main__':
    topicExtractring()    