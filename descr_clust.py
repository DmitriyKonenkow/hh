import pandas as pd
from sklearn.cluster import MiniBatchKMeans
desc = pd.read_pickle('work_data/req.pkl').drop_duplicates()

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(desc[0])
print(X_train_counts.shape)
from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf = X_train_tfidf.toarray()
print(X_train_tfidf.shape)
model = MiniBatchKMeans(n_clusters=30, batch_size=2000)
desc['label'] = model.fit_predict(X_train_tfidf)
print(desc.head())