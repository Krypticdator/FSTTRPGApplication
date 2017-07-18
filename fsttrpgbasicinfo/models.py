from random import choice, randint

import utilities
from databases import DBManager


class Names(object):
    def __init__(self, country, check_aws):
        super(Names, self).__init__()
        self.country = country
        self.check_aws = check_aws
        self.female_names = []
        self.male_names = []
        self.last_names = []
        self.faliases = []
        self.laliases = []

        self.load_names(country, check_aws)
        self.load_names('alias', check_aws)

    def load_names(self, country, check_aws):
        mgr = DBManager()

        country_names = mgr.names_table.get_names_of_country(country, check_aws=check_aws)
        if len(country_names) == 0:
            country_names = mgr.names_table.get_names_of_country(country, check_aws=True)

        for name in country_names:
            if name.group == 'fname':
                if name.gender == 'male':
                    if name.name not in self.male_names:
                        self.male_names.append(name.name)
                elif name.gender == 'female':
                    if name.name not in self.female_names:
                        self.female_names.append(name.name)
            elif name.group == 'lname':
                if name.name not in self.last_names:
                    self.last_names.append(name.name)
            elif name.group == 'falias':
                self.faliases.append(name.name)
            elif name.group == 'lalias':
                self.laliases.append(name.name)

    def random_name(self, gender):
        fname = None
        lname = None
        if gender == 'male':
            fname = choice(self.male_names)
        else:
            fname = choice(self.female_names)
        lname = choice(self.last_names)
        return fname + " " + lname

    def random_alias(self):
        return choice(self.faliases) + " " + choice(self.laliases)


class BasicInfo(object):
    def __init__(self, name, gender, dob, age, country=None, alias=None):
        super(BasicInfo, self).__init__()
        self.name = name
        self.gender = gender
        self.dob = dob
        self.age = age
        self.country = country
        self.alias = alias

    def random_name(self, check_from_aws=False):
        if self.gender is None:
            return None
        if self.country is not None:
            names = Names(country=self.country, check_aws=check_from_aws)
            self.name = names.random_name(self.gender)
            return self.name
        else:
            return None

    def random_alias(self):
        n = Names(self.country, check_aws=False)
        self.alias = n.random_alias()
        return self.alias

    def random_age(self, bottom_age=14, min=2, max=25):
        self.age = bottom_age + randint(min, max)
        return self.age

    def random_dob(self):
        self.dob = utilities.random_birthday()
        return self.dob

    def random_gender(self):
        random_gender = randint(1, 2)
        if random_gender == 1:
            self.gender = 'male'
        else:
            self.gender = 'female'

        return self.gender

    def random_all(self):
        self.random_gender()
        self.random_name()
        self.random_alias()
        self.random_age()
        self.random_dob()
        return {'gender': self.gender, 'alias': self.alias, 'name': self.name, 'age': self.age, 'dob': self.dob}

    def save(self, name, role):
        db_mgr = DBManager()
        db_mgr.basic_info.add_actor(name=name, role=role,
                                    gender=self.gender, country=self.country, birthday=self.dob,
                                    alias=self.alias, age=self.age)

    def load(self, name, role):
        db_mgr = DBManager()
        bi = db_mgr.basic_info.get_basic_info(name=name, role=role)
        self.name = name
        self.gender = bi.gender
        self.alias = bi.alias
        self.age = bi.age
        self.dob = bi.birthday
