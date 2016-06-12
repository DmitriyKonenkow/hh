import json as j

import pandas as pd
import requests
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

import create_db
import sql_mapper
from settings import *

__author__ = 'Loiso'

mapper(sql_mapper.Vacancy, create_db.vacancies_table)

Session = sessionmaker(bind=engine)
session = Session()


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
            session.merge(sql_mapper.Vacancy(vacancy_['id'], vacancy_['name'], vacancy_['created_at'],
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



