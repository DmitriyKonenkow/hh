from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Text

from settings import engine

metadata = MetaData()

vacancies_table = Table('vacancies', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String),
                        Column('created_at', DateTime),
                        Column('published_at', DateTime),
                        Column('area', String),
                        Column('city', String),
                        Column('street', String),
                        Column('employer', String),
                        Column('employment', String),
                        Column('experience', String),
                        Column('description', String),
                        Column('key_skills', String),
                        Column('salary_cur', String),
                        Column('salary_from', String),
                        Column('salary_to', String),
                        Column('schedule', String),
                        Column('specializations', String),
                        Column('billing_type', String),
                        Column('type', String))

dirty_vacancies_table = Table('dirty_data', metadata,
                              Column('id', Integer, primary_key=True),
                              Column('data', Text))

status_parse = Table('status_parse', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('status', Integer))

if __name__ == '__main__':
    metadata.create_all(engine)
