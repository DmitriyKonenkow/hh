import json as j

import pandas as pd
import re
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

import sql_mapper
from settings import *

Session = sessionmaker(bind=engine)
session = Session()

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
        list = [text.get_text() for text in list_req]
    except AttributeError:
        # print('Unparsed string: ' + string)
        return []
    return list


if __name__ == '__main__':
    pass