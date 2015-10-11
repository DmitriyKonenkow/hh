import json as j

import requests
import pandas as pd
import os

__author__ = 'Loiso'

url = 'https://api.hh.ru/vacancies'
columns = ['accept_handicapped', 'address', 'allow_messages', 'alternate_url',
           'apply_alternate_url', 'archived', 'area', 'billing_type',
           'branded_description', 'code', 'contacts', 'created_at', 'department',
           'description', 'employer', 'employment', 'experience', 'hidden', 'id',
           'key_skills', 'name', 'negotiations_url', 'premium', 'published_at',
           'relations', 'response_letter_required', 'response_url', 'salary',
           'schedule', 'site', 'specializations', 'suitable_resumes_url', 'test',
           'type']
per_page = 50
all_count = 1950
pages = all_count / per_page
store = 'vacancies.h5'
specialisation = '1.221'
area = '1'
csv = specialisation + '.csv'


def update_data(path):
    i = 1
    indexes = []
    if os.path.exists(csv):
        indexes = pd.read_csv(csv, sep=';', encoding='cp1251').id.tolist()
    while i <= pages:
        paging = '&period=30&per_page={0}&page={1}&specialization={2}&area={3}'.format(per_page, i, specialisation, area)
        i += 1
        request = url + '?' + path + paging
        print(request)
        res = requests.get(request).text
        data = j.loads(res)
        vacancies = []
        index = []
        for urlv in data['items']:
            if urlv['id'] in indexes:
                continue
            res_v = requests.get(urlv['url']).text
            vacancie = convertJson(j.loads(res_v))
            index.append(vacancie['id'])
            print(vacancie['key_skills'])
            vacancies.append(vacancie)
        reslut = pd.DataFrame(vacancies, index=index)
        print(reslut['key_skills'])
        if os.path.exists(csv):
            reslut.to_csv(csv, sep=';', mode='a', header=False)
        else:
            reslut.to_csv(csv, sep=';', mode='a')
        print('End update_data ' + str(i))


def convertJson(json):
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
    return series


def load_data(path):
    data = pd.DataFrame()
    if os.path.exists(path):
        data = pd.read_csv(path, sep=';', encoding='cp1251')
    print('End load_data')
    return data


def show_key_skills():
    data = load_data(csv)
    all_key_skills = ''.join((data['key_skills']).tolist())
    key_skill_pars = j.loads(all_key_skills.replace('\'', '\"').replace('[]', '').replace('][',','))
    result = pd.DataFrame(key_skill_pars)
    print(result.name.groupby(result.name).count().order(ascending=False)[:100])

def show_descriptions():
    data = load_data(csv)
    all_descriptions = ''.join((data['description']).tolist())
    descriptions_pars = all_descriptions.split(' ')
    result = pd.DataFrame(descriptions_pars)
    print(result[0].groupby(result[0]).count().order(ascending=False)[:100])


if __name__ == '__main__':
    #show_key_skills()
    show_descriptions()
    #update_data('')
    #convertJson(j.loads(requests.get(url+'/'+str(14557264)).text))