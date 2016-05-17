import json as j
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

__author__ = 'Loiso'

url = 'https://api.hh.ru/vacancies'
columns = ['area', 'billing_type', 'city', 'created_at', 'description',
           'employer', 'employment', 'experience', 'id', 'key_skills', 'name',
           'published_at', 'salary_cur', 'salary_from', 'salary_to',
           'schedule', 'specializations', 'street', 'type']
old_columns = ['accept_handicapped', 'allow_messages', 'alternate_url',
               'apply_alternate_url', 'archived', 'area', 'area_id', 'billing_type',
               'city', 'code', 'contacts', 'created_at',
               'description', 'employer', 'employment', 'experience', 'hidden', 'id',
               'key_skills', 'name', 'negotiations_url', 'premium', 'published_at',
               'relations', 'response_letter_required', 'response_url', 'salary_cur',
               'salary_from', 'salary_to', 'schedule', 'site', 'specializations',
               'street', 'suitable_resumes_url', 'type']
per_page = 50
key = 'vacancies'
specialisation = '1.221'
area = '1'
areas = ['1', '2114', '1620', '1624', '1646', '1652', '1192', '1124', '1146', '1118', '1174', '1169', '1187', '1661',
         '1679', '1704', '1217', '1229', '1202', '1249', '1216', '1255', '2019', '1932', '1941', '1943', '1946', '1948',
         '1960', '1975', '1982', '1008', '1020', '145', '1061', '1985', '1051', '1090', '1077', '1041', '2', '1103',
         '1716', '1739', '1754', '1771', '1783', '1806', '1563', '1575', '1556', '1586', '1596', '1614', '1308',
         '1317', '1347', '1261', '1342', '1368', '1384', '1414', '1463', '1471', '1438', '1422', '1424', '1434', '1475',
         '1481', '1500', '1817', '1828', '1844', '1859', '1880', '1890', '1898', '1905', '1913', '1505', '1511', '1553',
         '1530', '113', '5', '40', '9', '16', '1001', '28', '48', '97']


def update_data(path, spec=specialisation, area_id=area):
    print('Start spec = ' + spec + ' area = ' + area_id)
    csv = spec + '.csv'
    i = 0
    indexes = []
    if os.path.exists(csv):
        indexes = pd.read_csv(csv, sep=';').id.tolist()
    condition = True
    while condition:
        paging = '&period=30&per_page={0}&page={1}&specialization={2}&area={3}'.format(per_page, i, spec,
                                                                                       area_id)
        request = url + '?' + path + paging
        print(request)
        res = requests.get(request).text
        data = j.loads(res)
        pages = data['pages']
        vacancies = []
        index = []
        for urlv in data['items']:
            if urlv['id'] in indexes:
                continue
            res_v = requests.get(urlv['url']).text
            vacancy = convert_json_vacancy(j.loads(res_v))
            index.append(vacancy['id'])
            vacancies.append(vacancy)
        result = pd.DataFrame(vacancies, index=index)
        if os.path.exists(csv):
            result.to_csv(csv, sep=';', mode='a', header=False)
        else:
            result.to_csv(csv, sep=';', mode='a')
        print('End update_data ' + str(i))
        i += 1
        condition = (i <= pages - 1)


def load_vacancy(id):
    res_v = requests.get(url + '/{}'.format(id)).text
    vacancy = convert_json_vacancy(j.loads(res_v))
    return vacancy


def convert_json_vacancy(json):
    series = pd.Series(json)
    if series['area']:
        series['area_id'] = series['area']['id']
        series['area'] = series['area']['name']
    if series['address']:
        series['city'] = series['address']['city']
        series['street'] = series['address']['street']
    series.drop(['address'], inplace=True)
    if series['billing_type']:
        series['billing_type'] = series['billing_type']['name']
    if series['salary']:
        series['salary_from'] = series['salary']['from']
        series['salary_to'] = series['salary']['to']
        series['salary_cur'] = series['salary']['currency']
    series.drop(['salary'], inplace=True)
    if series['employer']:
        series['employer'] = series['employer']['name']
    if series['employment']:
        series['employment'] = series['employment']['name']
    if series['experience']:
        series['experience'] = series['experience']['name']
    if series['schedule']:
        series['schedule'] = series['schedule']['name']
    if series['site']:
        series['site'] = series['site']['name']
    if series['type']:
        series['type'] = series['type']['name']
    if len(series['specializations']) > 0:
        series['specializations'] = '|'.join(pd.DataFrame(series['specializations'])['name'].values)
    if len(series['key_skills']) > 0:
        series['key_skills'] = '|'.join(pd.DataFrame(series['key_skills'])['name'].values)
    else:
        series['key_skills'] = ''
    if len(series['relations']) > 0:
        series['relations'] = series['relations'].to_string()
    else:
        series['relations'] = ''
    series.drop(['test'], inplace=True)
    series.drop(['department'], inplace=True)
    series.drop(['branded_description'], inplace=True)
    series.drop(['contacts'], inplace=True)
    return series


def load_data(path):
    data = pd.DataFrame()
    if os.path.exists(path):
        data = pd.read_csv(path, sep=';')
    print('End load_data')
    return data


def extract_description(string):
    soup = BeautifulSoup(string, "lxml")
    return soup.get_text()


def extract_requirements(string):
    soup = BeautifulSoup(string, "lxml")
    list = [text.get_text() for text in soup.find(string='Требования:').find_next('ul').find_all('li')]
    return list


def show_key_skills(path):
    data = load_data(path)
    all_key_skills = pd.DataFrame('|'.join(data['key_skills'].dropna()).split('|'))
    print(all_key_skills[0].groupby(all_key_skills[0]).count().sort_values(ascending=False)[:20])


def load_all_data_from_areas():
    for ar in areas:
        update_data('', area_id=ar)


def show_descriptions(path):
    data = load_data(path)
    all_descriptions = ''.join((data['description']).tolist())
    descriptions_pars = all_descriptions.split(' ')
    result = pd.DataFrame(descriptions_pars)
    print(result[0].groupby(result[0]).count().sort_values(ascending=False)[:20])


if __name__ == '__main__':
    load_all_data_from_areas()
    show_key_skills('1.221.csv')
    # show_descriptions()
    # update_data('')
    # update_data('', area_id='5')
    # convertJson(j.loads(requests.get(url+'/'+str(14155307)).text))
