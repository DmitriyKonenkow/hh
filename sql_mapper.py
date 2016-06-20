from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    keys = relationship('KeySkills', secondary='vacancy_to_key')

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
    __tablename__ = 'dirty_data'

    id = Column('id', Integer, primary_key=True)
    data = Column('data', Text)

    def __init__(self, id, data):
        self.id = id
        self.data = data


class Status(Base):
    __tablename__ = 'status_parse'

    id = Column('id', Integer, primary_key=True)
    status = Column('status', Integer)

    def __init__(self, id, status):
        self.id = id
        self.status = status


class KeySkills(Base):
    __tablename__ = 'key_skills'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(32))
    define = Column('define', Boolean, default=False)

    def __init__(self, id, name, define):
        self.id = id
        self.name = name
        self.define = define

    @classmethod
    def init_from_session(cls, session, name, define=True):
        obj = session.query(KeySkills).filter_by(name=name).first()
        uid = None
        if obj:
            uid = obj.id
        return cls(uid, name, define)


class VacancyToKey(Base):
    __tablename__ = 'vacancy_to_key'

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), primary_key=True)
    key_id = Column(Integer, ForeignKey('key_skills.id'), primary_key=True)


class KeyRequirement(Base):
    __tablename__ = 'key_requirement'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(32))
    regexp = Column('regex', String(1024))
    parent_id = Column(Integer, ForeignKey('key_requirement.id'))


class Requirements(Base):
    __tablename__ = 'requirements'

    id = Column('id', Integer, primary_key=True)
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'))
    requirement = Column('requirement', String(128))
    cluster = Column('cluster', Integer)
    key_req_id = Column(Integer, ForeignKey('key_requirement.id'))

    def __init__(self, id, vacancy_id, requirement, cluster=None, key_req_id=None):
        self.id = id
        self.vacancy_id = vacancy_id
        self.requirement = requirement
        self.cluster = cluster
        self.key_req_id = key_req_id


class VacancyToKeyReq(Base):
    __tablename__ = 'vacancy_to_key_req'

    vacancy_id = Column(Integer, ForeignKey('vacancies.id'), primary_key=True)
    key_id = Column(Integer, ForeignKey('key_requirement.id'), primary_key=True)
    checked = Column('checked', Boolean)

    def __init__(self, vacancy_id, key_id, checked=False):
        self.vacancy_id = vacancy_id
        self.key_id = key_id
        self.checked = checked


if __name__ == '__main__':
    Base.metadata.create_all(engine)
