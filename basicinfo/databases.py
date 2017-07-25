from __future__ import print_function

import os

from peewee import CharField, IntegerField, ForeignKeyField

import utilities
from application.characterloader.database import Actor, DBManager as ActorDBManager
from application.common.database.masterdb import BaseModel

'''def find_or_create(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            result = os.path.join(root, name)
            print('found db in: ' + str(result))
            return result
    print('didnt find any db, creating new: ' + name)
    return name'''


current_dir = os.path.dirname(__file__)


class Names(BaseModel):
    name = CharField()
    country = CharField()
    group = CharField()
    gender = CharField()

    @staticmethod
    def add_name(name, country, group, gender):
        new_name, created = Names.get_or_create(name=name,
                                                defaults={'country': country,
                                                          'group': group,
                                                          'gender': gender})
        if created:
            print('already created')

    @staticmethod
    def add_many(list_of_names):
        with BaseModel.get_db().atomic():
            for index in range(0, len(list_of_names), 100):
                print('adding indexes: ' + str(index) + " - " + str(index + 100))
                Names.insert_many(list_of_names[index:index + 100]).execute()

    def get_names_of_country(self, country, check_aws):
        country_names = Names.select().where(Names.country == country)
        if check_aws:
            aws_names = utilities.get_aws_names_group(country)

            if len(aws_names) > len(country_names):
                self.add_many(aws_names)
        return Names.select().where(Names.country == country)

    @staticmethod
    def delete_country(country):
        query = Names.delete().where(Names.country == country)
        return query


class BasicInfo(BaseModel):
    actor = ForeignKeyField(rel_model=Actor, related_name='basics')
    gender = CharField()
    country = CharField()
    birthday = CharField()
    alias = CharField()
    age = IntegerField()
    status = CharField()

    @staticmethod
    def add_actor(name, role, gender, country, birthday, alias, age, status='alive'):
        if name is "":
            print('save failed, no name')
            return
        act = Actor.add_or_get(role=role, name=name)
        # print('birthday at save: ' + birthday)
        actor, created = BasicInfo.get_or_create(actor=act,
                                                 defaults={'gender': gender,
                                                           'country': country,
                                                           'birthday': birthday,
                                                           'alias': alias,
                                                           'age': int(age),
                                                           'status': status})
        if created:
            print('added new character to BasicInfo database')
            return None
        else:
            return actor

    @staticmethod
    def get_basic_info(name, role):
        act = Actor.get(Actor.name == name, Actor.role == role)
        bi = BasicInfo.get(BasicInfo.actor == act)
        print('birthday at load: ' + bi.birthday)
        return bi


class DBManager(object):
    def __init__(self):
        super(DBManager, self).__init__()
        self.actors_db_mgr = ActorDBManager()

        # https://stackoverflow.com/questions/42964254/peewee-operational-error-in-flask-app
        # namedb.connect()
        self.conn = BaseModel.get_connection()
        # characterdb.connect()

        BaseModel.create_tables([Names, BasicInfo])

        self.names_table = Names()
        self.basic_info = BasicInfo()
