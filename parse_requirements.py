import re

from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

import sql_mapper
from settings import *

Session = sessionmaker(bind=engine)
session = Session()


def parse_description():
    status_to_parse = session.query(sql_mapper.Status).filter(sql_mapper.Status.status == LOAD).limit(100)
    to_parse = status_to_parse.all()
    while len(to_parse) > 0:
        for p_s in to_parse:
            uid = p_s.id
            vacancy = session.query(sql_mapper.Vacancy).get(uid)
            requirements = extract_requirements(vacancy.description)
            if len(requirements) > 0:
                for req in requirements:
                    session.merge(sql_mapper.Requirements(None, uid, req))
            session.merge((sql_mapper.Status(uid, PARSE_REQ)))
        session.commit()
        to_parse = status_to_parse.all()
        count = session.query(sql_mapper.Status).filter(sql_mapper.Status.status == LOAD).count()
        print('left to parse requirements {}'.format(count))


def extract_requirements(string):
    soup = BeautifulSoup(string, "lxml")
    try:
        soup_req = soup.find(string=re.compile('ребования|'
                                               '(будущий сотрудник)|'
                                               '(видеть кандидата)|'
                                               '(профессиональные навыки)|'
                                               '(то нужно:)|'
                                               '(ожелания к кандидатам)|'
                                               '(ожидаем, что Вы:)|'
                                               '(успешным на данной)|'
                                               '(ожидаем от Вас навыков:)|'
                                               '(чтобы Вы знали)|'
                                               '(уметь и знать)|'
                                               '(бязательные знания)|'
                                               '(Необходимые навыки)|'
                                               '(потребуется)|'
                                               '(знать и уметь)|'
                                               '(владеющим)|'
                                               '(ребуемый опыт работы)|'
                                               '(вас ждем)|'
                                               '(ы ждем от)'))
        if soup_req.find_next('ul'):
            list_req = soup_req.find_next('ul').find_all('li')
        else:
            soup_usl = soup_req.find_next(string=re.compile('ловия|'
                                                            '(бязанности)'))
            for usl in soup_usl.find_all_next():
                usl.decompose()
            soup_usl.find_parent().decompose()
            list_req = soup_req.find_all_next('p')
        text_list = [text.get_text() for text in list_req]
        result = []
        for item in text_list:
            result.extend(filter(lambda x: len(x) > 1, re.split(',|;| и |/', item)))
    except AttributeError:
        # print('Unparsed string: ' + string)
        return []
    return result


if __name__ == '__main__':
    pass
    parse_description()
