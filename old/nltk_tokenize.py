import nltk
from nltk.corpus import stopwords


def clear_text(text):
    rus_stemmer = nltk.stem.snowball.RussianStemmer()
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)
    stop = stopwords.words('russian')
    filtered_words = [rus_stemmer.stem(word) for word in words if word not in stop]
    # bad_words = ['умен', 'проект', 'язык', 'работа']
    # filtered_words = filter(lambda x: x not in bad_words, filtered_words)
    return filtered_words
