from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy import create_engine
from settings import dbserver

engine = create_engine('postgresql://hh:USERPASS@%s:5432/hh' % dbserver)
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
metadata.create_all(engine)
