from peewee import Model, IntegerField, SqliteDatabase, ForeignKeyField

from application.basicinfo.databases import Actor, ActorDBManager

database = SqliteDatabase('stats.db')


class PrimaryStats(Model):
    actor = ForeignKeyField(Actor, 'primarystats')
    intelligence = IntegerField()
    reflexes = IntegerField()
    technique = IntegerField()
    dexterity = IntegerField()
    presense = IntegerField()
    willpower = IntegerField()
    constitution = IntegerField()
    strength = IntegerField()
    body = IntegerField()
    move = IntegerField()

    @staticmethod
    def save_character(character_name, role, intelligence, reflexes, technique, dexterity, presense, willpower,
                       constitution, strength, body, move):
        act = Actor.add_or_get(role=role, name=character_name)
        new_character, created = PrimaryStats.get_or_create(actor=act,
                                                            defaults={'intelligence': intelligence,
                                                                      'reflexes': reflexes,
                                                                      'technique': technique,
                                                                      'dexterity': dexterity,
                                                                      'presense': presense,
                                                                      'willpower': willpower,
                                                                      'constitution': constitution,
                                                                      'strength': strength,
                                                                      'body': body,
                                                                      'move': move})

        if created:
            print('created new character')
        else:
            print('modifying character')
            new_character.intelligence = intelligence
            new_character.reflexes = reflexes
            new_character.technique = technique
            new_character.dexterity = dexterity
            new_character.presense = presense
            new_character.willpower = willpower
            new_character.constitution = constitution
            new_character.strength = strength
            new_character.body = body
            new_character.move = move
            new_character.save()

    def get_character(self, role, name):
        act = Actor.add_or_get(role, name)
        return PrimaryStats.get(PrimaryStats.actor == act)

    class Meta:
        database = database


class DBManager(object):
    def __init__(self):
        super(DBManager, self).__init__()
        self.actor_db_mgr = ActorDBManager()
        database.connect()
        database.create_tables([PrimaryStats], safe=True)
        self.table_primary_stats = PrimaryStats()

    def __del__(self):
        database.close()
