import json as j
import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from settings import url, per_page, specialisation, area, areas, engine




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
    try:
        soup_req = soup.find(string=re.compile('ребования|'
                                               '(будущий сотрудник)|'
                                               '(видеть кандидата)|'
                                               '(профессиональные навыки)|'
                                               '(то нужно:)|'
                                               '(ожелания к кандидатам)|'
                                               '(ожидаем, что Вы:)|'
                                               '(успешным на данной)|'
                                               '(ожидаем от Вас навыков:)|'
                                               '(чтобы Вы знали)|'
                                               '(уметь и знать)|'
                                               '(бязательные знания)|'
                                               '(Необходимые навыки)|'
                                               '(потребуется)|'
                                               '(знать и уметь)|'
                                               '(владеющим)|'
                                               '(ребуемый опыт работы)|'
                                               '(вас ждем)|'
                                               '(ы ждем от)'))
        if soup_req.find_next('ul'):
            list_req = soup_req.find_next('ul').find_all('li')
        else:
            soup_usl = soup_req.find_next(string=re.compile('ловия|'
                                                            '(бязанности)'))
            for usl in soup_usl.find_all_next():
                usl.decompose()
            soup_usl.find_parent().decompose()
            list_req = soup_req.find_all_next('p')
        list = [text.get_text() for text in list_req]
    except AttributeError:
        # print('Unparsed string: ' + string)
        return []
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
