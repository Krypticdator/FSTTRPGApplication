from peewee import Model, ForeignKeyField, IntegerField, CharField, SqliteDatabase

from application.basicinfo.databases import DBManager as BasicInfoDBManager
from application.characterloader.database import Actor, DBManager as ActorDBManager

lifepath_db = SqliteDatabase('lifepath.db')


class Event(Model):
    actor = ForeignKeyField(Actor, related_name='event actors')
    age = IntegerField()
    event_chain = CharField()


    @staticmethod
    def add_event(actor_role, actor_name, age, event_chain):
        act = Actor.add_or_get(role=actor_role, name=actor_name)
        event, created = Event.get_or_create(actor=act,
                                             age=age,
                                             defaults={'event_chain': event_chain})
        if created:
            print('created new event')
            return True
        else:
            print('didnt create new event')
            return False

    @staticmethod
    def get_event_of_age(actor_role, actor_name, age):
        act = Actor.add_or_get(actor_role, actor_name)
        event = Event.get(Event.actor == act, Event.age == age)
        return event

    @staticmethod
    def get_all_events_of_actor(actor_role, actor_name):
        act = Actor.add_or_get(actor_role, actor_name)
        events = Event.select().where(Event.actor == act).order_by(Event.age)
        return events

    class Meta:
        database = lifepath_db


class EventRelation(Model):
    owner = ForeignKeyField(Actor, 'owners')
    relation = CharField
    detail = CharField
    mutual_feelings = CharField(null=True)
    sibling_relation = CharField(null=True)
    event = ForeignKeyField(Event, 'events')
    to_person = ForeignKeyField(Actor, 'event targets')
    cause = CharField(null=True)
    who = CharField(null=True)
    who_is_mad = CharField(null=True)
    action = CharField(null=True)
    resources = CharField(null=True)

    @staticmethod
    def save_event_relation(to_actor_role, to_actor_name, to_event_age, relation, ep_name, detail="", ep_role='NPC',
                            mutual_feelings=None, sibling_relation=None, cause=None, who=None,
                            who_is_mad=None, action=None, resources=None):
        # type: (str, str, int, str, str, str, str, str, str, str, str, str, str, str) -> object
        event = Event.get_event_of_age(actor_role=to_actor_role, actor_name=to_actor_name, age=to_event_age)
        owner = Actor.add_or_get(to_actor_role, to_actor_name)
        target = Actor.add_or_get(ep_role, ep_name)
        relation_count = EventRelation.get_relation_count_of_age(owner_role=to_actor_role, owner_name=to_actor_name,
                                                                 age=to_event_age)
        if relation_count < 3:
            relation, created = EventRelation.get_or_create(owner=owner, to_person=target, event=event,
                                                            defaults={'relation': relation, 'detail': detail,
                                                                      'mutual_feelings': mutual_feelings,
                                                                      'sibling_relation': sibling_relation,
                                                                      'cause': cause,
                                                                      'who': who,
                                                                      'who_is_mad': who_is_mad,
                                                                      'action': action,
                                                                      'resources': resources})
            if created:
                print('created new relation')

            return relation

    @staticmethod
    def get_relations_of_person(actor_role, actor_name):
        act = Actor.add_or_get(actor_role, actor_name)
        return EventRelation.select().where(EventRelation.owner == act)

    @staticmethod
    def get_relation_count_of_age(owner_role, owner_name, age):
        act = Actor.add_or_get(owner_role, owner_name)
        event = Event.get_event_of_age(owner_role, owner_name, age)
        return len(EventRelation.select().where(EventRelation.owner == act, EventRelation.event == event))

    @staticmethod
    def get_persons_related_to_event(owner_role, owner_name, age):
        act = Actor.add_or_get(owner_role, owner_name)
        event = Event.get_event_of_age(owner_role, owner_name, age)
        return EventRelation.select().where(EventRelation.owner == act, EventRelation.event == event)

    @staticmethod
    def get_relation_to_person(owner_role, owner_name, age, ep_name, ep_role='NPC'):
        act = Actor.add_or_get(owner_role, owner_name)
        event = Event.get_event_of_age(owner_role, owner_name, age)
        ep = Actor.add_or_get(ep_role, ep_name)
        return EventRelation.select().where(EventRelation.owner == act, EventRelation.event == event,
                                            EventRelation.to_person == ep)

    class Meta:
        database = lifepath_db



class DBManager(object):
    def __init__(self):
        self.actor_db_mgr = ActorDBManager()
        self.basic_info_mgr = BasicInfoDBManager()
        lifepath_db.get_conn()
        lifepath_db.create_tables([Event, EventRelation], safe=True)

        self.events = Event()
        self.relations = EventRelation()

    def __del__(self):
        if lifepath_db:
            lifepath_db.close()
