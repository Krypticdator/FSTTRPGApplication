import os

from peewee import Model, SqliteDatabase, CharField


def find_or_create(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            result = os.path.join(root, name)
            print('found db in: ' + str(result))
            return result
    print('didnt find any db, creating new: ' + name)
    return name


current_dir = os.path.dirname(__file__)
database_name = find_or_create('actors.db', current_dir)
actor_db = SqliteDatabase(database=database_name)


class Actor(Model):
    name = CharField(unique=True)
    role = CharField()

    @staticmethod
    def add_or_get(role, name):
        actor, created = Actor.get_or_create(role=role, name=name)
        if created:
            print('created new actor')
        else:
            print('loaded already existing character')
        return actor

    @staticmethod
    def get_all():
        return Actor.select()

    @staticmethod
    def get_all_with_role(role):
        return Actor.select().where(Actor.role == role)

    class Meta:
        database = actor_db


class DBManager(object):
    def __init__(self, actor_db_filepath=None):
        super(DBManager, self).__init__()
        actor_db.connect()
        actor_db.create_tables([Actor], safe=True)
        self.actors = Actor()

    def __del__(self):
        if actor_db:
            actor_db.close()
