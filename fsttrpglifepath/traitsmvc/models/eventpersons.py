from traits.api import HasTraits, String, Enum, Int, List, Instance

from fsttrpgbasicinfo.traitmvc.models import BasicInfo, CharacterName
from fsttrpglifepath.db import DBManager
from fsttrpglifepath.globals import *


class Relationships(HasTraits):
    relationship = Enum('none', 'combat teacher', 'mentor', 'friend', 'enemy', 'lover', 'ex-lover', 'lovers ex',
                        'ex-friend', 'ex-ally', 'child', 'lovers enemy', 'contact', 'sensei', 'teacher', 'favor',
                        'sibling', 'parent')
    detail = String()


class EventPerson(BasicInfo):
    name = String()
    status = Enum('none', 'dead', 'alive', 'missing', 'unknown')
    current_relationship = Instance(Relationships, ())
    past_relationships = List(Instance(Relationships, ()))
    validation_needed = Enum('no', 'yes')
    age = Int()

    def _character_name_default(self):
        return CharacterName(name_change_handler=self.load_name)

    def load_name(self):
        self.name = self.character_name.get_name()

    def set_relationship(self, relation, detail=""):
        cr = self.current_relationship.relationship
        cd = self.current_relationship.detail
        if self.current_relationship.relationship == 'none':
            self.current_relationship.relationship = relation
            self.current_relationship.detail = detail
        else:
            self.past_relationships.append(Relationships(relationship=cr, detail=cd))
            self.current_relationship.relationship = relation
            self.current_relationship.detail = detail

    def get_relationship(self):
        return self.current_relationship.relationship

    def save_relation(self, actor_role, actor_name, event_age):
        db_mgr = DBManager()
        rel = self.get_relationship()
        detail = self.current_relationship.detail
        db_mgr.relations.save_event_relation(to_actor_role=actor_role, to_actor_name=actor_name, to_event_age=event_age,
                                             relation=rel, ep_name=self.name, detail=detail)

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

        db_mgr.basic_info_mgr.basic_info.add_actor(name=name, role=role, gender=gender, country=country,
                                                   birthday=birthday, alias=alias, age=age, status=self.status)

    def load(self, actor_name, actor_role='NPC'):
        # TODO - Do this better, must update basicinfo project
        self.character_name.set_name(actor_name)
        self.character_name.role = actor_role
        super(EventPerson, self).load()
        db_mgr = DBManager()
        db_basic_info = db_mgr.basic_info_mgr.basic_info.get_basic_info(actor_name, actor_role)
        self.status = db_basic_info.status

    def load_relation(self, owner_role, owner_name, age, ep_name):
        db_mgr = DBManager()
        r = db_mgr.relations.get_relation_to_person(owner_role=owner_role, owner_name=owner_name, age=age,
                                                    ep_name=ep_name)
        for rel in r:
            self.set_relationship(rel.relation, rel.detail)


class Enemy(EventPerson):
    cause = Enum(TABLE_ENEMY_CAUSES.results())
    who = Enum(TABLE_ENEMY_TYPE.results())
    who_is_mad = Enum(TABLE_ENEMY_HATE.results())
    do = Enum(TABLE_ENEMY_DO.results())
    resources = Enum(TABLE_ENEMY_RESOURCES.results())

    def save_relation(self, actor_role, actor_name, event_age):
        db_mgr = DBManager()
        db_mgr.enemy_relations.save_enemy_relation(actor_role, actor_name, event_age, enemy_name=self.name,
                                                   cause=self.cause, who=self.who, who_is_mad=self.who_is_mad,
                                                   action=self.do, resources=self.resources)

    def load_relation(self, owner_role, owner_name, event_age, ep_name):
        db_mgr = DBManager()
        enemy = db_mgr.enemy_relations.get_enemy_of_owner(owner_role, owner_name, event_age)
        self.cause = enemy.cause
        self.who = enemy.who
        self.who_is_mad = enemy.who_is_mad
        self.do = enemy.action
        self.resources = enemy.resources
        self.name = enemy.enemytargets.name


class TragicLove(EventPerson):
    mutual_feelings = Enum(TABLE_LOVE_MUTUAL_FEELINGS.results())

    def save_relation(self, actor_role, actor_name, event_age):
        db_mgr = DBManager()
        rel = self.get_relationship()
        detail = self.current_relationship.detail
        db_mgr.relations.save_event_relation(to_actor_role=actor_role, to_actor_name=actor_name, to_event_age=event_age,
                                             relation=rel, ep_name=self.name, detail=detail,
                                             mutual_feelings=self.mutual_feelings)

    def load_relation(self, owner_role, owner_name, age, ep_name):
        db_mgr = DBManager()
        r = db_mgr.relations.get_relation_to_person(owner_role=owner_role, owner_name=owner_name, age=age,
                                                    ep_name=ep_name)
        for rel in r:
            self.set_relationship(rel.relation, rel.detail)
            self.mutual_feelings = rel.mutual_feelings


class Sibling(EventPerson):
    relation = Enum(TABLE_SIBLING_RELATION.results())

    def random_sibling(self):
        self.random_all()
        self.relation = TABLE_SIBLING_RELATION.random_result()
        self.status = 'alive'
        self.set_relationship('sibling')

    def save_relation(self, actor_role, actor_name, event_age):
        db_mgr = DBManager()
        rel = self.get_relationship()
        detail = self.current_relationship.detail
        db_mgr.relations.save_event_relation(to_actor_role=actor_role, to_actor_name=actor_name, to_event_age=event_age,
                                             relation=rel, ep_name=self.name, detail=detail,
                                             sibling_relation=self.relation)


class TwoEventPersons(HasTraits):
    person1 = Instance(EventPerson, ())
    person2 = Instance(EventPerson, ())


def make_event_person(relationship, status, detail="", needs_validation='yes'):
    return EventPerson(current_relationship=Relationships(relationship=relationship, detail=detail),
                       status=status, validation_needed=needs_validation)


def make_lover(status, detail="", needs_validation='no'):
    return EventPerson(current_relationship=Relationships(relationship='lover', detail=detail), status=status,
                       validation_needed=needs_validation)


def make_enemy(detail="", needs_validation='no'):
    return Enemy(current_relationship=Relationships(relationship='enemy', detail=detail), status='alive',
                 validation_needed=needs_validation)


def make_tragic_lover(status, detail="", needs_validation='no'):
    return TragicLove(current_relationship=Relationships(relationship='lover', detail=detail), status=status,
                      validation_needed=needs_validation)
