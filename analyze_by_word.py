from sklearn.feature_extraction.text import CountVectorizer
from sqlalchemy.orm import sessionmaker

from settings import engine
from sql_mapper import Vacancy

Session = sessionmaker(bind=engine)
session = Session()


def top_words(word):
    descr = session.query(Vacancy.description).filter(Vacancy.description.ilike('%{}%'.format(word))).limit(5).all()
    vectorizer = CountVectorizer()
    result = vectorizer.fit_transform([r for r, in descr])
    print(result)
    np.sort(result.sum(axis=0),)[0, -5:]


if __name__ == '__main__':
    pass
    top_words('java')
