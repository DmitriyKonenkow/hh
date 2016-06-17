import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sqlalchemy.orm import sessionmaker

from old.hh_load import extract_description
from settings import engine
from sql_mapper import Vacancy

Session = sessionmaker(bind=engine)
session = Session()

stop_words = stopwords.words('russian') + stopwords.words('english') \
             + ['доступа', 'полисы', 'опыт', 'работы', 'знание', 'компании', 'условия', 'знания', 'праздники',
                'разработки', 'требования', 'разработка', 'приложений', 'умение', 'работа', 'обязанности', 'понимание',
                'experience', 'development', 'офис', 'лет', 'работать', 'данных', 'возможность','software','skills',
                'систем','work','участие','компания','knowledge','working','technical','requirements','systems','business',
                'solutions','technologies','project','environment','00', 'тк','проектов','плата','заработная','рф',
                'технологий','задачи','оформление','принципов','системы','программирования','навыки','уровне','data',
                'плюсом','офисе','системами','языков','график','end','работу','company','code','good','projects',
                'new','бизнес','разработке','developer','языка','программного','world','years','решений','кода','роста',
                'strong','ciklum','applications','social','time','understanding','application']


def top_words(word):
    descr = session.query(Vacancy.description).filter(Vacancy.description.ilike('%{}%'.format(word)), Vacancy.salary_cur=='RUR', Vacancy.salary_from > 100000).all()
    vectorizer = CountVectorizer(stop_words=stop_words)
    result = vectorizer.fit_transform([extract_description(r) for r, in descr])
    vocabulary = pd.Series(vectorizer.vocabulary_)
    data = pd.DataFrame(result.sum(axis=0), columns=vocabulary.keys())
    print(data.T.sort_values(0, ascending=0).head(20))


if __name__ == '__main__':
    pass
    top_words(' java ')
