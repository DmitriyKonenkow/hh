import os

import numpy as np
import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

from classificator_add import *
from settings import *

vectorizer = StemmedTfidfVectorizer(min_df=1, decode_error='ignore', stop_words=stop)
if os.path.isfile(vectorizer_file):
    vectorizer = load_vectorizer(vectorizer_file)

clf = OneVsRestClassifier(LinearSVC())
if os.path.isfile(clf_file):
    clf = load_clf(clf_file)
labels = None
if os.path.isfile(clf_labels_file):
    labels = load_labels(clf_labels_file)


def get_test_data(learn_vect=0):
    descr = pd.read_sql(sql_select_descriptions, engine, index_col='id')
    label_data = pd.read_sql(select_labels, engine)
    label_data['val'] = 1
    vacancy_label = label_data.pivot(index='vacancy_id', columns='name', values='val').fillna(0)
    if learn_vect:
        learn_vectorizer(vectorizer, descr['description'])
    descr_transform = vectorizer.transform(descr['description'])
    return descr_transform, vacancy_label


def predict_labels(string):
    vect_str = vectorizer.transform([string])
    labels_id = clf.predict(vect_str)
    return labels[np.where(labels_id[0] == 1)[0]]


if __name__ == '__main__':
    pass
    #x, y = get_test_data(learn_vect=1)
    #learn_clf(clf, x, y)
    print(predict_labels("sql"))
    # learn_clf():
    # print(get_test_data())
