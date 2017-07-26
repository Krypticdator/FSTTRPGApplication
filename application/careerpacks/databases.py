from peewee import CharField, ForeignKeyField

from application.attributes.databases import AttributeBlueprint, DBManager as AttributeDBManager
from application.common.database.masterdb import BaseModel


class CareerPack(BaseModel):
    career_name = CharField()
    attribute_blueprint = ForeignKeyField(AttributeBlueprint, related_name='career')

    @staticmethod
    def add(career_name, attr_type, attr_name):
        blueprint = AttributeBlueprint.get_blueprint(attribute_type=attr_type, name=attr_name)
        row, created = CareerPack.get_or_create(career_name=career_name, attribute_blueprint=blueprint)
        if created:
            print('created new skill to pack' + career_name)
        else:
            print('this skill is already part of pack: ' + career_name)

    @staticmethod
    def get_pack_names():
        names = []
        all = CareerPack.select()
        for row in all:
            if row.career_name in names:
                pass
            else:
                names.append(row.career_name)
        return names

    @staticmethod
    def get_pack_skills(pack_name):
        return CareerPack.select().where(CareerPack.career_name == pack_name)


class DBManager(object):
    def __init__(self):
        super(DBManager, self).__init__()
        self.attribute_db_mgr = AttributeDBManager()
        self.conn = BaseModel.get_connection()
        BaseModel.create_tables(models=[CareerPack], safe=True)
        self.career_packs = CareerPack()


if __name__ == '__main__':
    db_mgr = DBManager()
    solo = db_mgr.career_packs.get_pack_skills('solo')
