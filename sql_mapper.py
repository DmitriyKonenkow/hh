from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from settings import engine

Base = declarative_base()


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    created_at = Column('created_at', DateTime)
    published_at = Column('published_at', DateTime)
    area = Column('area', String)
    city = Column('city', String)
    street = Column('street', String)
    employer = Column('employer', String)
    employment = Column('employment', String)
    experience = Column('experience', String)
    description = Column('description', String)
    key_skills = Column('key_skills', String)
    salary_cur = Column('salary_cur', String)
    salary_from = Column('salary_from', String)
    salary_to = Column('salary_to', String)
    schedule = Column('schedule', String)
    specializations = Column('specializations', String)
    billing_type = Column('billing_type', String)
    type = Column('type', String)

    def __init__(self, id, name, created_at, published_at, area, city,
                 street, employer, employment, experience, description, key_skills,
                 salary_cur, salary_from, salary_to, schedule, specializations, billing_type, type):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.published_at = published_at
        self.area = area
        self.city = city
        self.street = street
        self.employer = employer
        self.employment = employment
        self.experience = experience
        self.description = description
        self.key_skills = key_skills
        self.salary_cur = salary_cur
        self.salary_from = salary_from
        self.salary_from = salary_to
        self.schedule = schedule
        self.specializations = specializations
        self.billing_type = billing_type
        self.type = type


class Dirty(Base):
    __tablename__ = 'status_parse'

    id = Column('id', Integer, primary_key=True)
    data = Column('data', Text)

    def __init__(self, id, data):
        self.id = id
        self.data = data


class Status(Base):
    __tablename__ = 'dirty_data'

    id = Column('id', Integer, primary_key=True)
    status = Column('status', Integer)

    def __init__(self, id, status):
        self.id = id
        self.status = status


class KeySkills(Base):
    __tablename__ = 'key_skills'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(32))

    def __init__(self, id, name):
        self.id = id
        self.name = name

if __name__ == '__main__':
    Base.metadata.create_all(engine)