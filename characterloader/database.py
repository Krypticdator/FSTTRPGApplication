from peewee import CharField

from application.common.database.masterdb import BaseModel


class Actor(BaseModel):
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



class DBManager(object):
    def __init__(self, actor_db_filepath=None):
        super(DBManager, self).__init__()
        self.conn = BaseModel.get_connection()
        BaseModel.create_tables([Actor])

        self.actors = Actor()
