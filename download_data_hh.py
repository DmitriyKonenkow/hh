import json as j

import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

import create_db
import vacancy

__author__ = 'Loiso'

mapper(vacancy.Vacancy, create_db.vacancies_table)
engine = create_engine('postgresql://hh:USERPASS@192.168.40.131:5432/hh')
Session = sessionmaker(bind=engine)
session = Session()
url = 'https://api.hh.ru/vacancies'
columns = ['area', 'billing_type', 'city', 'created_at', 'description',
           'employer', 'employment', 'experience', 'id', 'key_skills', 'name',
           'published_at', 'salary_cur', 'salary_from', 'salary_to',
           'schedule', 'specializations', 'street', 'type']
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
    i = 0
    condition = True
    while condition:
        paging = '&period=30&per_page={0}&page={1}&specialization={2}&area={3}'.format(per_page, i, spec,
                                                                                       area_id)
        request = url + '?' + path + paging
        print(request)
        res = requests.get(request).text
        data = j.loads(res)
        pages = data['pages']
        for urlv in data['items']:
            res_v = requests.get(urlv['url']).text
            vacancy_ = convert_json(j.loads(res_v))
            session.merge(vacancy.Vacancy(vacancy_['id'], vacancy_['name'], vacancy_['created_at'],
                                          vacancy_['published_at'], vacancy_['area'], vacancy_['city'],
                                          vacancy_['street'], vacancy_['employer'], vacancy_['employment'],
                                          vacancy_['experience'], vacancy_['description'], vacancy_['key_skills'],
                                          vacancy_['salary_cur'], vacancy_['salary_from'], vacancy_['salary_to'],
                                          vacancy_['schedule'], vacancy_['specializations'],
                                          vacancy_['billing_type'], vacancy_['type']))
        session.commit()
        print('End update_data ' + str(i))
        i += 1
        condition = (i <= pages - 1)


def convert_json(json):
    series = pd.Series(json)
    if series['area']:
        series['area_id'] = series['area']['id']
        if series['area']['name']:
            series['area'] = series['area']['name']
        else:
            series['area'] = None
    if series['address']:
        series['city'] = series['address']['city']
        series['street'] = series['address']['street']
    else:
        series['city'] = None
        series['street'] = None
    series.drop(['address'], inplace=True)
    if series['billing_type']:
        series['billing_type'] = series['billing_type']['name']
    if series['salary']:
        series['salary_from'] = series['salary']['from']
        series['salary_to'] = series['salary']['to']
        series['salary_cur'] = series['salary']['currency']
    else:
        series['salary_from'] = None
        series['salary_to'] = None
        series['salary_cur'] = None
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
    series['created_at'] = pd.to_datetime(series['created_at'])
    series['published_at'] = pd.to_datetime(series['published_at'])
    series.drop(['test'], inplace=True)
    series.drop(['department'], inplace=True)
    series.drop(['branded_description'], inplace=True)
    series.drop(['contacts'], inplace=True)
    return series


def load_all_data_from_areas():
    for ar in areas:
        update_data('', area_id=ar)


if __name__ == '__main__':
    load_all_data_from_areas()
    #update_data('', area_id='97')
