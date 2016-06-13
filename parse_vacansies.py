import json as j

import pandas as pd
from sqlalchemy.orm import sessionmaker

import sql_mapper
from settings import *

Session = sessionmaker(bind=engine)
session = Session()


def parse_data():
    print('Start parse')
    status_query = session.query(sql_mapper.Status).filter(sql_mapper.Status.status == '1').limit(100)
    dirty_status = status_query.all()
    while len(dirty_status) > 0:
        for d_s in dirty_status:
            uid = d_s.id
            dirty_vc = session.query(sql_mapper.Dirty).get(uid)
            vacancy_ = convert_json(j.loads(dirty_vc.data))
            session.merge(sql_mapper.Vacancy(vacancy_['id'], vacancy_['name'], vacancy_['created_at'],
                                             vacancy_['published_at'], vacancy_['area'], vacancy_['city'],
                                             vacancy_['street'], vacancy_['employer'], vacancy_['employment'],
                                             vacancy_['experience'], vacancy_['description'], vacancy_['key_skills'],
                                             vacancy_['salary_cur'], vacancy_['salary_from'], vacancy_['salary_to'],
                                             vacancy_['schedule'], vacancy_['specializations'],
                                             vacancy_['billing_type'], vacancy_['type']))
            session.merge((sql_mapper.Status(d_s.id, 2)))
        session.commit()
        dirty_status = status_query.all()
        count = session.query(sql_mapper.Status).filter(sql_mapper.Status.status == '1').count()
        print('left to parse {}'.format(count))
    print('End parse data')


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


if __name__ == '__main__':
    parse_data()
