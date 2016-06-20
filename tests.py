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
        self.assertIsNone(testRegEx('имеете опыт работы с Internet', 28), 'Incorrect parse')
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
        self.assertIsNotNone(testRegEx('знание шаблона mvc', 48), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с pl sql.', 46), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('или pl-sql на уровне проектирования бд', 46), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('принципов работы http', 43), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хорошо поставленная грамотная речь.', 47), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('использования twitter bootstrap', 54), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с системами контроля версий svn', 53), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('желательно знание фрэймворка yii', 56), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание графических пакетов (photoshop). умение "нарезать" макет под верстку', 58), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('высшее профильное техническое образование', 2), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт разработки restful api', 41), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с rest api', 41), 'Incorrect parse')
        self.assertIsNone(testRegEx('prestashop', 41), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с bitrix', 63), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('специальные навыки:  опыт использования soap', 60), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('владение hibernate', 62), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с maven', 67), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('уверенное знание delphi 7', 68), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знакомство с фреймворкоми (backbone', 70), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('препроцессоров less.', 72), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('технологиями доступа к данным (jdbc', 71), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с hadoop', 92), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('библиотеками angularjs', 61), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с nosql (redis', 101), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('no-sql', 101), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('scala: опыт разработки от 2 лет', 97), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('фреймворка django', 88), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хорошее знание sqlite', 79), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с apache kafka', 99), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с hadoop-экосистемой (apache spark', 95), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с nosql хранилищами (mongodb', 96), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание основных диаграмм uml', 80), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хорошее владение java se', 64), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('отличное знание cocoa touch', 83), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хорошо знает node.js', 87), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('хорошая обучаемость', 59), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('драйверов. мы используем cassandra', 94), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('практика применения java ee', 91), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('веб-сервера (nginx', 90), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание cms wordpress', 89), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание adobe illustrator (обязательно)', 75), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('coregraphics', 82), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('tls', 84), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('желательно: entityframework', 78), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание entity framework', 78), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('уверенные знания objectivec', 86), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('профессиональное владение objective-c', 86), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с subversion', 81), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('cloud-сервисы: aws', 100), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы с amazon web services.', 100), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('умение использовать apache big data стэк (hadoop', 98), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('фреймворков bigdata (hortonworks', 98), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('личные качества: стрессоустойчивость', 55), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('ответственность‚ исполнительность‚ самостоятельность.', 57), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('управленческого учета', 66), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('управленческий учет', 66), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('пунктуальный', 76), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('целеустремленный', 74), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт разработки сложных отчетов с использованием скд.', 69), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('практический опыт управления проектами', 85), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание основных библиотек машинного обучения', 93), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('релевантного поставленным задачам - machine learning', 93), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание структур данных', 52), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('знание основных алгоритмов', 50), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('высокая степень внимательности', 49), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('здоровая инициатива', 51), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('проактивность.', 51), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('сопровождения информационных систем', 65), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('аналитическое мышление.', 45), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('опыт работы: 1-3 года в сфере программирования', 1), 'Incorrect parse')
        self.assertIsNotNone(testRegEx('asdasgitdasdasd', 14), 'Incorrect parse')

if __name__ == '__main__':
    unittest.main()
