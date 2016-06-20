import re

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

from settings import engine, LOAD, PARSE_REQ
from sql_mapper import VacancyToKeyReq, Status, Vacancy

Session = sessionmaker(bind=engine)
session = Session()

sql_select_regexp = 'SELECT id, name, regex FROM key_requirement WHERE  regex IS NOT NULL'
regexp = pd.read_sql(sql_select_regexp, engine, index_col='id')


def parse_req(string):
    soup = BeautifulSoup(string, "lxml")
    text = soup.get_text()
    result_req = []
    for index, row in regexp.iterrows():
        res = re.search(row['regex'], text, re.IGNORECASE)
        if res:
            result_req.append(index)
    return result_req


def save_parced_keys(keys_list, vacancy_id):
    session.query(VacancyToKeyReq).filter(VacancyToKeyReq.vacancy_id == vacancy_id).delete()
    for key in keys_list:
        key_entity = VacancyToKeyReq(vacancy_id, int(key))
        session.merge(key_entity)
    session.commit()


def parse_requirements_keys():
    status_to_parse = session.query(Status).filter(Status.status == LOAD).limit(500)
    to_parse = status_to_parse.all()
    while len(to_parse) > 0:
        for p_s in to_parse:
            uid = p_s.id
            vacancy = session.query(Vacancy).get(uid)
            requirements = parse_req(vacancy.description)
            if len(requirements) > 0:
                save_parced_keys(requirements, uid)
            session.merge((Status(uid, PARSE_REQ)))
        session.commit()
        to_parse = status_to_parse.all()
        count = session.query(Status).filter(Status.status == LOAD).count()
        print('left to parse requirements {}'.format(count))


if __name__ == '__main__':
    pass
    # parse_req('js asdfasd fkjsdalfkjasdkj html')
    # save_parced_keys([3, 4], 3500642)
    parse_requirements_keys()
