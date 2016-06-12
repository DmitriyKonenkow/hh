from sqlalchemy import create_engine

""" DB """
engine = create_engine('sqlite+pysqlite:///work_data/hh.db')

""" Import data """
url = 'https://api.hh.ru/vacancies'
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

""" Parse data """
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
