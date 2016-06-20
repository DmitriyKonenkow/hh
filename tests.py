import json as j
import re
import unittest

import pandas as pd
from sqlalchemy.orm import sessionmaker
from test_data import *

from old import hh_load
from parse_requirements import extract_requirements
from settings import engine
from sql_mapper import KeyRequirement

work_data = '../work_data/'

Session = sessionmaker(bind=engine)
session = Session()


def testRegEx(string, uid):
    regex = re.compile(session.query(KeyRequirement).get(uid).regexp)
    return regex.search(string)

def testParseRegEx():
    re.compile('.*js.*').search('твердое знание html + css + js.')

@unittest.skip("not ready yet")
class LoadVacancyCase(unittest.TestCase):
    def runTest(self):
        vacancy = hh_load.load_vacancy(9252535)
        print(vacancy)


class ConvertJsonVacancyCase(unittest.TestCase):
    def runTest(self):
        vacancy = j.loads(vacancy_json)
        vacancy = hh_load.convert_json_vacancy(vacancy)


class ConvertVacancyDescription(unittest.TestCase):
    def runTest(self):
        result = hh_load.extract_description(vacancy_description)
        self.assertEquals(vacancy_description_extracted, result,
                          'incorrect parse requirements from vacancy description')


class ExtractRequirementsFromVacancy(unittest.TestCase):
    def runTest(self):
        result = hh_load.extract_requirements(vacancy_description)
        self.assertEquals(5, len(result), 'incorrect parse requirements from vacancy description')
        self.assertEquals('Уверенное знание Java SE (опыт работы от 2 лет).', result[0],
                          'incorrect parse requirements from vacancy description')


class ExtractRequirementsFromVacancy1(unittest.TestCase):
    def runTest(self):
        result = extract_requirements(vacancy_description1)
        self.assertEquals(7, len(result), 'incorrect parse requirements from vacancy description')
        self.assertEquals('- опыт программирования с++', result[0],
                          'incorrect parse requirements from vacancy description')


# @unittest.skip("code to extract example requirements")
class ExtractReq(unittest.TestCase):
    def runTest(self):
        descr = pd.read_pickle(work_data + 'descr.pkl')
        list_req = []
        unparsed = 0
        for row in descr.head(1000).iterrows():
            requirements = hh_load.extract_requirements(row[1][0])
            if len(requirements) == 0:
                unparsed += 1
            list_req.extend(requirements)
        req = pd.DataFrame(list_req)
        req.to_pickle(work_data + 'req.pkl')
        print('Unparsed rows {}'.format(unparsed))


# @unittest.skip("code to extract example descr")
class ExtractDescr(unittest.TestCase):
    def runTest(self):
        descr = pd.read_pickle(work_data + 'descr.pkl')
        list_desc = []
        for row in descr.head(1000).iterrows():
            descr = hh_load.extract_description(row[1][0])
            list_desc.append(descr)
        desc = pd.DataFrame(list_desc)
        desc.to_pickle(work_data + 'descr_cl.pkl')


class TestRegEx(unittest.TestCase):
    def runTest(self):
        self.assertIsNotNone(testRegEx('отличное знание perl.', 73), 'Incorrect parse')
        self.assertIsNone(testRegEx('hyperlynx.', 73), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('навыки html5.', 3), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('твердое знание html + css + js.', 3), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('твердое знание html + css + js.', 4), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с javascript ', 4), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('css3 на реальных проектах', 5), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('твердое знание html + css + js.', 5), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание sql от 2-х лет', 6), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('работы c api cms: 1c-битрикс', 7), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хорошее знание php', 8), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('личная ответственность за результат', 9), 'Incorrect parse')
        self.assertIsNone(testRegEx('знание javascript', 10), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('уверенное владение java se 6', 10), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание фреймворков (jquery)', 11), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('умение работать в команде.', 12), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хранилищ данных (mysql)', 13), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хранилищ данных (my sql)', 13), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с git', 14), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с ms sql', 15), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с mssql', 15), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('upper-intermediate english', 16), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('технический английский достаточный для общения.', 16), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('понимание принципов ооп', 17), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('принципов объектно-ориентированного программирования', 17), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание основ тестирования по.', 18), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('qunit', 18), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('понимать чужой код', 19), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хорошее знание linux (ubuntu', 20), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('или oracle db', 21), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('технологии c#.net', 22), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('личные качества: коммуникабельность', 24), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт администрирования ', 26), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('контейнеров данных (xml', 27), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('имеете опыт работы с asp.net', 28), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с ajax', 29), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('нескольких из предметных областей: бухгалтерский учет', 30), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('обладаете огромным желанием развиваться в сфере программирования', 31), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт применения шаблонов проектирования (gof', 33), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('умение применять паттерны проектирования', 33), 'Incorrect parse')
        self.assertIsNone(testRegEx('шаблоны интеграции)', 33), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('умение работать самостоятельно', 35), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт разработки приложений под ios', 36), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт разработки приложений под android', 36), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт разработки мобильных приложений', 36), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('глубокое знание c++ с опытом работы от 2х лет', 37), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знания spring framework (core)', 39), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт разработки приложений под android', 42), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('предпочтительно postgresql.', 44), 'Incorrect parse')
        #self.assertIsNotNone(testRegEx('asdasdasdasd', 14), 'Incorrect parse')

if __name__ == '__main__':
    unittest.main()
