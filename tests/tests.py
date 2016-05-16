import json as j
import unittest

from test_data import vacancy_json, vacancy_description, vacancy_description_extracted

import hh_load


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
        self.assertEquals(vacancy_description_extracted, result, 'incorrect parse requirements from vacancy description')


class ExtractRequirementsFromVacancy(unittest.TestCase):
    def runTest(self):
        result = hh_load.extract_requirements(vacancy_description)
        self.assertEquals(5, len(result), 'incorrect parse requirements from vacancy description')
        self.assertEquals('Уверенное знание Java SE (опыт работы от 2 лет).', result[0], 'incorrect parse requirements from vacancy description')


if __name__ == '__main__':
    unittest.main()
