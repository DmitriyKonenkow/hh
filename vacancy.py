class Vacancy(object):
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

    def __repr__(self):
        return "<Vacancy('%s','%s')>" % (self.id, self.name)