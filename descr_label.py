import pprint

import pandas as pd
from gensim import corpora, models

import hh_load
from nltk_tokenize import clear_text
from tests.test_data import vacancy_description_extracted

pp = pprint.PrettyPrinter()
dictionary = None
model = None


def load_texts():
    descr = pd.read_pickle('work_data/descr.pkl').drop_duplicates()
    list_req = []
    for row in descr.head(100).iterrows():
        requirements = hh_load.extract_requirements(row[1][0])
        if len(requirements) > 0:
            list_req.append(' '.join(requirements))
    return list_req


def learn_model(texts, num_topics=100):
    texts = [clear_text(document) for document in texts]
    global dictionary
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=10, no_above=0.4)
    corpus = [dictionary.doc2bow(text) for text in texts]
    global model
    model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, alpha='auto', eval_every=5,minimum_probability=0.01)


def get_topics(text):
    text = clear_text(text)
    corp = dictionary.doc2bow(text)
    return model[corp]


if __name__ == '__main__':
    learn_model(load_texts())
    topics = get_topics(vacancy_description_extracted)
    pp.pprint([model.show_topic(topic[0], topn=3) for topic in topics])