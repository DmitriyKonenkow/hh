import re

from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
import pandas as pd
from settings import engine

Session = sessionmaker(bind=engine)
session = Session()

sql_select_regexp = 'SELECT id, name, regex FROM key_requirement WHERE  regex IS NOT NULL'
regexp = pd.read_sql(sql_select_regexp, engine, index_col='id')

def parse_req(string):
    soup = BeautifulSoup(string, "lxml")
    text = soup.get_text()
    result_req = []
    for index, row in regexp.iterrows():
        try:
            res = re.search(row['regex'], text)
            if res:
                result_req.append(index)
        except AttributeError:
            pass
            # print('Unparsed string: ' + string)
    print(result_req)

if __name__ == '__main__':
    pass
parse_req('js asdfasd fkjsdalfkjasdkj html')