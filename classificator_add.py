import pickle

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer_file = 'work_data/vectorizer.pkl'
clf_file = 'work_data/clf.pkl'
clf_labels_file = 'work_data/clf_labels.pkl'
sql_select_key_skills = 'SELECT id, name FROM key_skills'
sql_select_descriptions = """
SELECT
  DISTINCT v.id,
  v.description
FROM vacancies v
  JOIN vacancy_to_key_req vkr ON v.id = vkr.vacancy_id

"""
select_labels = """
SELECT
    vkr.vacancy_id,
    kr.name
    FROM vacancy_to_key_req vkr JOIN key_requirement kr ON vkr.key_id = kr.id
"""


def load_vectorizer(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


def load_clf(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


def load_labels(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


rus_stemmer = nltk.stem.snowball.RussianStemmer()
stop = stopwords.words('russian')
stop.extend(['знан', 'умен', 'оп', 'работ', 'разработк', 'принцип', 'платформ'])


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: filter(lambda x: x not in stop, (rus_stemmer.stem(w) for w in analyzer(
            doc.replace('c#', 'c_sharp').replace('c++', 'c_plus_plus'))))


def learn_vectorizer(vectorizer, x):
    vectorizer.fit(x)
    with open(vectorizer_file, 'wb') as f:
        pickle.dump(vectorizer, f)
    return vectorizer


def learn_clf(clf, x, y):
    clf.fit(x, y)
    with open(clf_file, 'wb') as f:
        pickle.dump(clf, f)
    with open(clf_labels_file, 'wb') as f:
        pickle.dump(y.columns, f)
    return clf, y.columns
