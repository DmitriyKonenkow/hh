import json as j
import unittest

import pandas as pd
from test_data import *

from old import hh_load

work_data = '../work_data/'


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
        result = hh_load.extract_requirements(vacancy_description1)
        self.assertEquals(3, len(result), 'incorrect parse requirements from vacancy description')
        self.assertEquals('- опыт программирования С++, желательно С#, VBA;', result[0],
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


class TokenizeText(unittest.TestCase):
    def runTest(self):
        text = vacancy_description_extracted
        clear_text = clear_text(text)
        print(clear_text)

if __name__ == '__main__':
    unittest.main()
