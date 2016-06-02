import pandas as pd
from gensim import corpora, models

import hh_load

descr = pd.read_pickle('work_data/descr.pkl').drop_duplicates()
list_req = []
for row in descr.head(100).iterrows():
    requirements = hh_load.extract_requirements(row[1][0])
    if len(requirements) > 0:
        list_req.append(' '.join(requirements))
#print(list_req)
texts = [[word for word in document.lower().split()] for document in list_req]

dictionary = corpora.Dictionary(texts)
#print(dictionary)
#print(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)
#tfidf = models.TfidfModel(corpus)
#corpus_tfidf = tfidf[corpus]
#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
#corpus_lsi = lsi[corpus_tfidf]
#print(lsi.print_topics(5))
lda = models.LdaModel(corpus, num_topics=20)
print(lda.show_topics())