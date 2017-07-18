from peewee import Model, CharField, IntegerField, SqliteDatabase

db = SqliteDatabase('fuziontables.db')


class FuzionTable(Model):
    identifier = CharField(unique=True)
    table = CharField()
    fr = IntegerField()
    to = IntegerField()
    re = CharField()
    leads_to_table = CharField(null=True)

    class Meta:
        database = db

    @staticmethod
    def count_options(table):
        return len(FuzionTable.select().where(FuzionTable.table == table))

    @staticmethod
    def get_table(table):
        return FuzionTable.select().where(FuzionTable.table == table)

    @staticmethod
    def add_option(identifier, table, fr, to, re, leads_to=None):
        option, created = FuzionTable.get_or_create(identifier=identifier, table=table,
                                                    defaults={'fr': fr,
                                                              'to': to,
                                                              're': re,
                                                              'leads_to_table': leads_to})
        if created:
            print('added option')
        else:
            print('option already exists, modifying')
            option.fr = fr
            option.to = to
            option.re = re
            option.leads_to_table = leads_to

    @staticmethod
    def add_many(list_of_options):
        with db.atomic():
            for index in range(0, len(list_of_options), 100):
                FuzionTable.insert_many(list_of_options[index:index + 100]).execute()

    def delete_table(self, table):
        FuzionTable.delete().where(FuzionTable.table == table)


class DBManager(object):
    def __init__(self):
        super(DBManager, self).__init__()
        db.connect()
        db.create_tables([FuzionTable], True)
        self.fuzion_tables = FuzionTable()

    def __del__(self):
        db.close()
