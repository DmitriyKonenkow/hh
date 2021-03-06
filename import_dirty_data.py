"""
Файл импорта не разобранных данных по вакансиям
"""

import json as j

import requests
from sqlalchemy.orm import sessionmaker

import sql_mapper
from settings import *

Session = sessionmaker(bind=engine)
session = Session()


def update_data(path, spec=specialisation, area_id=area):
    print('Start spec = {} area = {}'.format(spec, area_id))
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
            uid = urlv['id']
            if session.query(sql_mapper.Dirty).get(uid) is None:
                res_v = requests.get(urlv['url']).text
                session.merge(sql_mapper.Dirty(uid, res_v))
                session.merge(sql_mapper.Status(uid, 1))
        session.commit()
        print('End update_data ' + str(i))
        i += 1
        condition = (i <= pages - 1)


def load_all_data_from_areas():
    count = len(areas)
    for ar in areas:
        update_data('', area_id=ar)
        count -= 1
        print('left areas to load {}'.format(count))


if __name__ == '__main__':
    load_all_data_from_areas()
    # update_data('', area_id='2114')
