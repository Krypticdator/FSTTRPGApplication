# https://stackoverflow.com/questions/3283306/finding-out-absolute-path-to-a-file-from-python
import os

from peewee import Model, SqliteDatabase

folder = str(os.path.abspath(os.path.dirname(__file__)))
print(folder)
fuziondb = SqliteDatabase(folder + '/fuzion.db')


class BaseModel(Model):
    @staticmethod
    def get_connection():
        return fuziondb.get_conn()

    @staticmethod
    def create_tables(models, safe=True):

        fuziondb.create_tables(models, safe=safe)

    @staticmethod
    def get_db():
        return fuziondb

    def __del__(self):
        try:
            if fuziondb:
                fuziondb.close()
                # print('successfully closed the database')
        except TypeError:
            print('failed to close the database')

    class Meta:
        database = fuziondb
