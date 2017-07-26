from random import randint

from traits.api import HasTraits, Instance, Enum, String, Range

from application.basicinfo.databases import DBManager
from application.basicinfo.models import Names
from application.basicinfo.utilities import random_birthday
from application.characterloader.traitsmodels import CharacterName
from application.tables.models import Table

AGE_TABLE = Table('ages')


class BasicInfo(HasTraits):
    character_name = Instance(CharacterName)
    country = Enum('us')
    alias = String
    gender = Enum('male', 'female')
    age = Range(14, 100, mode='spinner')
    names = None
    birthday = String()

    def _character_name_default(self):
        return CharacterName(name_change_handler=self.load_name)

    def load_name(self):
        pass

    def random_name(self):
        country = self.country
        gender = self.gender
        if self.names is None:
            self.names = Names(country, False)
        if self.names.country != self.country:
            self.names = Names(country)

        self.character_name.name.name = self.names.random_name(gender)

    def random_alias(self):
        if self.names is None:
            self.names = Names(self.country, self.configure_names.check_aws_for_names)
        self.alias = self.names.random_alias()

    def set_last_name(self, surname):
        name = self.character_name.get_name()

        array = name.split(' ')
        new_name = array[0] + ' ' + surname
        self.character_name.set_name(new_name)

    def get_last_name(self):
        name = self.character_name.get_name()
        array = name.split(' ')
        return array[1]

    def random_age(self, random_min=2, random_max=25, use_3d6_table=False):
        if use_3d6_table:
            dice = sum([randint(1, 6), randint(1, 6), randint(1, 6)])
            result = AGE_TABLE.get_result(index=dice)
            array = result.split('-')
            n1 = int(array[0])
            n2 = int(array[1])
            self.age = randint(n1, n2)
        else:

            self.age = 14 + randint(random_min, random_max)

    def random_dob(self):
        self.birthday = random_birthday()

    def random_all(self, gender=None):
        if gender is None:
            random_gender = randint(1, 2)
            if random_gender == 1:
                self.gender = 'male'
            else:
                self.gender = 'female'
        else:
            self.gender = gender

        self.random_age()
        self.random_name()
        self.random_alias()
        self.random_dob()

    def save(self):
        db_mgr = DBManager()
        name = self.character_name.get_name()
        role = self.character_name.role
        gender = self.gender
        country = self.country
        birthday = self.birthday
        alias = self.alias
        age = self.age
        print('saving basicinfo with name: ' + name + ', role: ' + role + ', gender: ' + gender + ', country: ' +
              country + ', dob: ' + birthday + ', alias: ' + alias + ', age: ' + str(age))
        db_mgr.basic_info.add_actor(name=name, role=role, gender=gender, country=country, birthday=birthday,
                                    alias=alias, age=age)

    def load(self):
        db_mgr = DBManager()
        bi = db_mgr.basic_info.get_basic_info(name=self.character_name.get_name(), role=self.character_name.role)
        self.gender = bi.gender
        self.alias = bi.alias
        self.age = bi.age
        self.birthday = bi.birthday
