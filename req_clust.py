import pandas as pd
from sklearn.cluster import Birch, MiniBatchKMeans
from sqlalchemy.orm import sessionmaker

import sql_mapper
from classificator_add import StemmedTfidfVectorizer, stop
from settings import engine

Session = sessionmaker(bind=engine)
session = Session()

select_req_to_cluster = 'SELECT id, vacancy_id, requirement, key_req_id FROM requirements'
sql_clear_cluster = 'UPDATE requirements SET cluster = NULL WHERE cluster IS NOT NULL;'


def cluster_req():
    execute_sql(sql_clear_cluster)
    req = pd.read_sql(select_req_to_cluster, engine, index_col='id')
    vectorizer = StemmedTfidfVectorizer(min_df=1, decode_error='ignore', stop_words=stop)
    x_train_tfidf = vectorizer.fit_transform(req['requirement'])
    model = MiniBatchKMeans(n_clusters=150, batch_size=20000)
    #model = Birch(branching_factor=10, n_clusters=None, threshold=0.95, compute_labels=True)
    # model = AffinityPropagation()
    # model = MeanShift()
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


def execute_sql(sql):
    connection = engine.connect()
    result = connection.execute(sql)
    connection.close()
    return result


if __name__ == '__main__':
    pass
    cluster_req()