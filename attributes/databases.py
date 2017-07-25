from collections import namedtuple

from peewee import CharField, IntegerField, BooleanField, ForeignKeyField, DoubleField, \
    DoesNotExist

import aws
from application.characterloader.database import Actor, DBManager as ActorDBManager
from application.common.database.masterdb import BaseModel


class AttributeBlueprint(BaseModel):
    attribute_type = CharField()
    name = CharField(unique=True)
    category = CharField(null=True)
    cost = DoubleField()
    desc = CharField()

    @staticmethod
    def get_blueprint(attribute_type, name):
        bp = AttributeBlueprint.get(AttributeBlueprint.name == name,
                                    AttributeBlueprint.attribute_type == attribute_type)
        return bp

    @staticmethod
    def count_rows():
        return len(AttributeBlueprint.select())

    @staticmethod
    def add_or_modify(attribute_type, name, category, cost, desc):

        blueprint, created = AttributeBlueprint.get_or_create(attribute_type=attribute_type, name=name,
                                                              defaults={'category': category,
                                                                        'cost': cost,
                                                                        'desc': desc})
        if created:
            print('created new blueprint: ' + name)
        else:
            blueprint.category = category
            blueprint.cost = cost
            blueprint.desc = desc
            blueprint.save()

    @staticmethod
    def get_all_of_type(type):
        return AttributeBlueprint.select().where(AttributeBlueprint.attribute_type == type)


class CareerPack(BaseModel):
    career_name = CharField()
    attribute_blueprint = ForeignKeyField(AttributeBlueprint, related_name='careers')

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


class SkillBlueprint(BaseModel):
    blueprint = ForeignKeyField(AttributeBlueprint, related_name='skill_addons')
    chip_lvl_cost = IntegerField()
    chippable = BooleanField()
    diff = IntegerField()
    short = CharField()
    stat = CharField()

    @staticmethod
    def create_skill_blueprint(blueprint_name, chip_lvl_cost, chippable, diff, short, stat):
        blueprint = AttributeBlueprint.get_blueprint('skill', blueprint_name)
        skill_blueprint = SkillBlueprint(blueprint=blueprint, chip_lvl_cost=chip_lvl_cost, chippable=chippable,
                                         diff=diff, short=short, stat=stat)
        skill_blueprint.save()


# name category chip_lvl_cost chippable diff short stat chipped ip lvl carbon_lvl field
SkillTuple = namedtuple('SkillTuple',
                        field_names='name category chip_lvl_cost chippable diff short stat chipped ip lvl carbon_lvl field')


class Skill(BaseModel):
    blueprint = ForeignKeyField(SkillBlueprint, related_name='effective_skills')
    actor = ForeignKeyField(Actor, related_name='actors')
    chipped = BooleanField(default=False)
    ip = IntegerField()
    lvl = IntegerField()
    carbon_lvl = IntegerField()
    field = CharField()

    @staticmethod
    def add_or_modify_skill(character_name, character_role, skill_name, chipped, ip, lvl, field):
        actor = Actor.add_or_get(name=character_name, role=character_role)
        blueprint = AttributeBlueprint.get_blueprint('skill', skill_name)
        skill, created = Skill.get_or_create(actor=actor, blueprint=blueprint,
                                             defaults={'chipped': chipped,
                                                       'ip': ip,
                                                       'lvl': lvl,
                                                       'carbon_lvl': lvl,
                                                       'field': field})
        if created:
            print('created new skill')
        else:
            print('modifying already existing skill')
            skill.chipped = chipped
            skill.ip = ip
            skill.lvl = lvl
            skill.field = field
            skill.blueprint = blueprint
            skill.save()

    @staticmethod
    def load_skills_of(actor_role, actor_name):
        act = Actor.add_or_get(role=actor_role, name=actor_name)
        q = Skill.select(Skill, SkillBlueprint).join(SkillBlueprint).where(Skill.actor == act)
        skills = []
        for skill in q:
            name = skill.blueprint.blueprint.name
            category = skill.blueprint.blueprint.category
            chip_lvl_cost = skill.blueprint.chip_lvl_cost
            chippable = skill.blueprint.chippable
            diff = skill.blueprint.diff
            short = skill.blueprint.short
            stat = skill.blueprint.stat
            chipped = skill.chipped
            ip = skill.ip
            lvl = skill.lvl
            carbon_lvl = skill.carbon_lvl
            field = skill.field
            # name category chip_lvl_cost chippable diff short stat chipped ip lvl carbon_lvl field
            s = SkillTuple(name=name, category=category, chip_lvl_cost=chip_lvl_cost, chippable=chippable, diff=diff,
                           short=short, stat=stat, chipped=chipped, ip=ip, lvl=lvl, carbon_lvl=carbon_lvl, field=field)
            skills.append(s)
        return skills


AttributeTuple = namedtuple('AttributeTuple', 'name lvl field')


class Attribute(BaseModel):
    attribute_type = CharField()
    blueprint = ForeignKeyField(AttributeBlueprint, related_name='effective_attributes')
    actor = ForeignKeyField(Actor, related_name='character_attributes')
    lvl = IntegerField(null=True)
    field = CharField(null=True)

    @staticmethod
    def add_or_modify(attribute_type, blueprint_name, actor_name, actor_role, lvl, field):
        blueprint = AttributeBlueprint.get_blueprint(attribute_type=attribute_type, name=blueprint_name)
        act = Actor.add_or_get(role=actor_role, name=actor_name)
        attribute, created = Attribute.get_or_create(attribute_type=attribute_type, blueprint=blueprint, actor=act,
                                                     defaults={'lvl': lvl,
                                                               'field': field})
        if created:
            print('created new attribute: ' + blueprint_name)
        else:
            attribute.lvl = lvl
            attribute.field = field
        return attribute

    @staticmethod
    def get_attribute(attribute_type, actor_role, actor_name, blueprint_name):
        try:
            blueprint = AttributeBlueprint.get_blueprint(attribute_type=attribute_type, name=blueprint_name)
            act = Actor.add_or_get(role=actor_role, name=actor_name)
            attribute = Attribute.get(Attribute.actor == act, Attribute.blueprint == blueprint)
            return attribute
        except DoesNotExist as e:
            print(str(e))
            return None

    @staticmethod
    def load_attributes_of(actor_role, actor_name, attribute_type):
        act = Actor.add_or_get(actor_role, actor_name)
        q = Attribute.select().where(Attribute.attribute_type == attribute_type, Attribute.actor == act)
        attributes = []
        for a in q:
            name = a.blueprint.name
            lvl = a.lvl
            field = a.field
            attribute = AttributeTuple(name=name, lvl=lvl, field=field)
            attributes.append(attribute)
        return attributes


PerkTuple = namedtuple('PerkTuple', field_names='name lvl field target_name target_role')


class Perk(BaseModel):
    base_attribute = ForeignKeyField(Attribute, related_name='perks')
    target = ForeignKeyField(Actor, related_name='targets', null=True)

    @staticmethod
    def add_or_modify_perk(actor_role, actor_name, blueprint_name, lvl, field, target_role=None, target_name=None):
        attribute = Attribute.get_attribute('perk', actor_role=actor_role, actor_name=actor_name,
                                            blueprint_name=blueprint_name)
        target = None
        if attribute is None:
            attribute = Attribute.add_or_modify('perk', blueprint_name=blueprint_name, actor_name=actor_name,
                                                actor_role=actor_role,
                                                lvl=lvl, field=field)
        if target_name is not None:
            target = Actor.add_or_get(role=target_role, name=target_name)
        perk, created = Perk.get_or_create(base_attribute=attribute, target=target)
        if created:
            print('created new perk')
        else:
            pass

    @staticmethod
    def get_perks_of_actor(actor_role, actor_name):
        actor = Actor.add_or_get(actor_role, actor_name)
        # Perk.select().where(Perk.base_attribute.actor == actor)

        q = Perk.select(Perk, Attribute).join(Attribute).where(Attribute.actor == actor)
        perks = []
        for p in q:
            name = p.base_attribute.blueprint.name
            lvl = p.base_attribute.lvl
            field = p.base_attribute.field
            target = p.target
            if target is not None:
                perks.append(PerkTuple(name=name, lvl=lvl, field=field, target_name=target.name,
                                       target_role=target.role))
            else:
                perks.append(PerkTuple(name=name, lvl=lvl, field=field, target_name=None, target_role=None))
        return perks


ComplicationTuple = namedtuple('ComplicationTuple', field_names='name intensity frequency importance')


class Complication(BaseModel):
    base_attribute = ForeignKeyField(Attribute, related_name='complications')
    intensity = IntegerField()
    frequency = IntegerField()
    importance = IntegerField()

    @staticmethod
    def add_or_modify(actor_name, actor_role, blueprint_name, intensity, frequency, importance):

        attribute = Attribute.get_attribute(attribute_type='complication', actor_role=actor_role, actor_name=actor_name,
                                            blueprint_name=blueprint_name)
        if attribute is None:
            attribute = Attribute.add_or_modify('complication', blueprint_name=blueprint_name, actor_name=actor_name,
                                                actor_role=actor_role, lvl=0, field="")
        complication, created = Complication.get_or_create(base_attribute=attribute, defaults={'intensity': intensity,
                                                                                               'frequency': frequency,
                                                                                               'importance': importance})
        if created:
            print('created new complication')
        else:
            complication.intensity = intensity
            complication.frequency = frequency
            complication.importance = importance
            complication.save()

    @staticmethod
    def load_complications_of(actor_role, actor_name):
        act = Actor.add_or_get(role=actor_role, name=actor_name)
        q = Complication.select(Complication, Attribute).join(Attribute).where(Attribute.actor == act,
                                                                               Attribute.attribute_type == 'complication')
        complications = []
        for row in q:
            name = row.base_attribute.blueprint.name
            freq = row.frequency
            inte = row.intensity
            impo = row.importance
            complications.append(ComplicationTuple(name=name, frequency=freq, intensity=inte, importance=impo))
        return complications


class DBManager(object):
    def __init__(self):
        self.actor_db_mgr = ActorDBManager()
        BaseModel.get_connection()
        BaseModel.create_tables([AttributeBlueprint, Skill, SkillBlueprint, Attribute, Perk, Complication,
                                     CareerPack], safe=True)

        self.attribute_blueprints = AttributeBlueprint()
        self.skill_blueprints = SkillBlueprint()
        self.attributes = Attribute()
        self.complications = Complication()
        self.perks = Perk()
        self.career_packs = CareerPack()

        if self.attribute_blueprints.count_rows() == 0:
            self.populate_attribute_blueprints()
        self.skills = Skill()

    def populate_attribute_blueprints(self):
        skills = aws.import_attributes_of_type('skill')
        perks = aws.import_attributes_of_type('perk')
        talents = aws.import_attributes_of_type('talent')
        complications = aws.import_attributes_of_type('complication')
        attributes = [skills, perks, talents, complications]
        # print(skills)

        for list_of_attributes in attributes:
            for a in list_of_attributes:
                self.attribute_blueprints.add_or_modify(attribute_type=a['type'], name=a['name'], category=a['category']
                                                        , cost=a['cost'], desc=a['desc'])
                if a['type'] == 'skill':
                    chippable = False
                    if a['chippable'] == 'yes':
                        chippable = True

                    self.skill_blueprints.create_skill_blueprint(blueprint_name=a['name'],
                                                                 chip_lvl_cost=a['chip_lvl_cost'],
                                                                 chippable=chippable, diff=a['diff'],
                                                                 short=a['short'], stat=a['stat'])


if __name__ == '__main__':
    db_mgr = DBManager()
