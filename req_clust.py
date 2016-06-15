import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sqlalchemy.orm import sessionmaker

import sql_mapper
from classificator_add import StemmedTfidfVectorizer, stop
from settings import engine

Session = sessionmaker(bind=engine)
session = Session()

select_req_to_cluster = 'SELECT id, vacancy_id, requirement, key_req_id FROM requirements'


def cluster_req():
    req = pd.read_sql(select_req_to_cluster, engine, index_col='id')
    vectorizer = StemmedTfidfVectorizer(min_df=1, decode_error='ignore', stop_words=stop)
    x_train_tfidf = vectorizer.fit_transform(req['requirement'])
    model = MiniBatchKMeans(n_clusters=100, batch_size=20000)
    req['cluster'] = model.fit_predict(x_train_tfidf)
    count = len(req)
    print('Item to save {}'.format(count))
    for index, row in req.iterrows():
        session.merge(sql_mapper.Requirements(int(index), row.vacancy_id, row.requirement, row.cluster))
        count -= 1
        if count % 10000 == 0:
            session.commit()
            print('left to save {}'.format(count))
    session.commit()
    print('The end')


if __name__ == '__main__':
    pass
    cluster_req()
