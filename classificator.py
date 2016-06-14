import pickle

import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

from settings import *

rus_stemmer = nltk.stem.snowball.RussianStemmer()
stop = stopwords.words('russian')
vectorizer_file = 'work_data/vectorizer.pkl'


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: (rus_stemmer.stem(w) for w in analyzer(doc))


def get_test_data():
    descr = pd.read_sql('SELECT id, description FROM vacancies where id in (16894195, 17383649);', engine,
                        index_col='id')
    label_data = pd.read_sql('SELECT vacancy_id, key_id FROM vacancy_to_key where vacancy_id in (16894195, 17383649);',
                             engine)
    label_data['val'] = 1
    label = label_data.pivot(index='vacancy_id', columns='key_id', values='val').fillna(0)
    vectorizer = StemmedTfidfVectorizer(min_df=1, decode_error='ignore', stop_words=stop)
    with open(vectorizer_file, 'wb') as f:
        pickle.dump(vectorizer, f)
    descr_transform = vectorizer.fit_transform(descr['description'])
    return descr_transform, label


def vectorize():
    return pickle.load(vectorizer_file)


def learn_clf():
    clf = OneVsRestClassifier(LinearSVC(random_state=0))
    X, y = get_test_data()
    clf.fit(X, y)
    print(clf.predict(X))

if __name__ == '__main__':
    pass
    learn_clf()
    # print(get_test_data())
