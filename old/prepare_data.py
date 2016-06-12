import pandas as pd
from sqlalchemy import create_engine
import nltk.stem
from settings import dbserver

engine = create_engine('postgresql://hh:USERPASS@%s:5432/hh' % dbserver)

english_stemmer = nltk.stem.SnowballStemmer('english')
russian_stemmer = nltk.stem.SnowballStemmer('russian')
stopwords = set(nltk.corpus.stopwords.words('english')+nltk.corpus.stopwords.words('russian'))

data = pd.read_sql_query('SELECT DISTINCT description from vacancies', engine)
data = data.drop_duplicates()
data = [t.split() for t in data]
data = [map(lambda w: w.lower(), t) for t in data]
data = [filter(lambda s: not len(set("+-.?!()>@012345689") & set(s)), t) for t in data]
data = [filter(lambda s: (len(s) > 3) and (s not in stopwords), t) for t in data]
print(data)
