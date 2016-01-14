import pandas as pd
from sqlalchemy import create_engine
from gensim import corpora, models, matutils

engine = create_engine('postgresql://hh:USERPASS@192.168.40.131:5432/hh')

data = pd.read_sql_query('SELECT description from descr', engine)

corpus = corpora.BleiCorpus(data)
model = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=corpus.id2word, alpha=None)
for ti in range(model.num_topics):
    words = model.show_topic(ti, 64)
    tf = sum(f for f, w in words)
    with open('topics.txt', 'w') as output:
        output.write('\n'.join('{}:{}'.format(w, int(1000. * f / tf)) for f, w in words))
        output.write("\n\n\n")
