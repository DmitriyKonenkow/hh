import unittest

import hh_load
from tests.test_data import vacancy_json


@unittest.skip("not ready yet")
class LoadVacancyCase(unittest.TestCase):
    def runTest(self):
        vacancy = hh_load.load_vacancy(9252535)
        print(vacancy)


class ConvertJsonVacancyCase(unittest.TestCase):
    def runTest(self):
        vacancy = vacancy_json
        vacancy = hh_load.convert_json_vacancy(vacancy)
        print(vacancy)


if __name__ == '__main__':
    unittest.main()
