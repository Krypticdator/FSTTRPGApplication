from random import randint

from traits.api import HasTraits, String, Button, List, Instance, Int, Enum, Method, Bool
from traitsui.api import Item, View, HGroup, VGroup, Group, Tabbed, ListEditor

from application.basicinfo.traitmvc.models import BasicInfo, CharacterName
from application.lifepath.globals import *
from db import DBManager
from models import event_menu


class Relationships(HasTraits):
    relationship = Enum('none', 'combat teacher', 'mentor', 'friend', 'enemy', 'lover', 'ex-lover', 'lovers ex',
                        'ex-friend', 'ex-ally', 'child', 'lovers enemy', 'contact', 'sensei', 'teacher', 'favor',
                        'sibling', 'parent')
    detail = String()

    view = View(
        HGroup(
            Item('relationship', show_label=False),
            Item('detail', style='readonly')
        )

    )


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

    view = View(
        VGroup(
            HGroup(
                Item('name'),
                Item('status', show_label=False),
            ),

            HGroup(

                Item('current_relationship', style='custom', show_label=False),
            )

        ),

        Item('past_relationships', style='readonly', show_label=True)
    )


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

    def load_relation(self, owner_role, owner_name, event_age):
        db_mgr = DBManager()
        enemy = db_mgr.enemy_relations.get_enemy_of_owner(owner_role, owner_name, event_age)
        self.cause = enemy.cause
        self.who = enemy.who
        self.who_is_mad = enemy.who_is_mad
        self.do = enemy.action
        self.resources = enemy.resources
        self.name = enemy.enemytargets.name

    view = View(
        VGroup(
            HGroup(
                Item('name'),
                Item('status', show_label=False),
            ),

            HGroup(

                Item('current_relationship', style='custom', show_label=False),
            ),
            Item('cause'),
            Item('who'),
            Item('who_is_mad'),
            Item('do'),
            Item('resources')

        ),

        Item('past_relationships', style='readonly', show_label=True)
    )


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

    view = View(
        VGroup(
            HGroup(
                Item('name'),
                Item('status', show_label=False),
            ),

            HGroup(

                Item('current_relationship', style='custom', show_label=False),
            ),
            Item('mutual_feelings')

        ),

        Item('past_relationships', style='readonly', show_label=True)
    )


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

    view = View(
        VGroup(
            HGroup(
                Item('name'),
                Item('status', show_label=False),
                Item('gender'),
                Item('relation'),
            ),

        )
    )


class TwoEventPersons(HasTraits):
    person1 = Instance(EventPerson, ())
    person2 = Instance(EventPerson, ())

    view = View(
        HGroup(
            Item('person1', style='custom'),
            Item('person2', style='custom')
        )

    )


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



def handler_1_2(path):
    if BETRAYEL_PATTERN_1.match(path):  # 1.2.4.1.X
        # print('bl_p1 match')
        return make_event_person(relationship='enemy', status='alive', detail='blackmails you',
                                 needs_validation='no')

    elif BETRAYEL_PATTERN_2.match(path):  # 1.2.4.3.X
        # print('bl_p2 match')
        return make_event_person(relationship='ex-friend', detail='betrayed you', status='alive')

    elif FRND_KILLED_PATTERN_1.match(path):
        return make_event_person(relationship='ex-ally', status='dead', detail='died accidentally')

    elif FRND_KILLED_PATTERN_2.match(path) or FRND_KILLED_PATTERN_3.match(path):
        ep1 = make_event_person(relationship='ex-ally', status='dead', detail='murdered')
        ep2 = make_event_person(relationship='enemy', status='unknown', detail='murdered your loved one',
                                needs_validation='no')
        if FRND_KILLED_PATTERN_3.match(path):
            ep2.status = 'alive'

        return TwoEventPersons(person1=ep1, person2=ep2)
    else:
        return None


class Event(HasTraits):
    age = Int()
    path = String()
    desc = String()
    chain = String()
    random_event = Button()
    life_path_method = Method()
    person = Instance(EventPerson)
    two_event_persons = Instance(TwoEventPersons)
    locked = Bool()
    do_generate_event_persons = Bool(default_value=True)

    def load_event_from_chain(self, chain):
        c, path_array = event_menu.decode_table_chain_string(chain)
        self.do_generate_event_persons = False
        # self.chain = chain
        self.path = self.transform_path_array_to_string(path_array)

    def _random_event_fired(self):
        self.random_life_event()

    def random_life_event(self):
        r = randint(1, 4)
        chain, array = event_menu.get_random_chain_string(first_index=r)
        self.path = self.transform_path_array_to_string(array)
        print(chain)

    def generate_event_persons(self, path):

        self.person = None
        self.two_event_persons = None
        ep1 = None
        ep2 = None
        # Big Problems, Big Wins DISASTER STRIKES Betrayal  you are being blackmailed.

        if path[0] == '1':
            if len(path) >= 3:
                if path[2] == '2':
                    person_or_persons = handler_1_2(path)
                    if person_or_persons.__class__ == EventPerson:
                        self.person = person_or_persons
                    elif person_or_persons.__class__ == TwoEventPersons:
                        self.two_event_persons = person_or_persons
                elif path[2] == '1':
                    # print('lucky')
                    if POWERFUL_CONNECTION_PATTERN.match(path):
                        # print('powerful connection')
                        if path == '1.1.1.1':
                            ep1 = make_event_person(relationship='contact', status='alive',
                                                    detail='local security force', needs_validation='no')
                        elif path == '1.1.1.2':
                            ep1 = make_event_person(relationship='contact', status='alive',
                                                    detail='local altcult office', needs_validation='no')
                        elif path == '1.1.1.3':
                            ep1 = make_event_person('contact', 'alive', detail='city leaders office',
                                                    needs_validation='no')
                    elif path == '1.1.4':
                        ep1 = make_event_person('sensei', 'alive', needs_validation='no')
                    elif path == '1.1.5':
                        ep1 = make_event_person('teacher', status='alive', needs_validation='no')
                    elif path == '1.1.6':
                        ep1 = make_event_person('favor', status='alive', detail='powerful altcult member',
                                                needs_validation='no')
                    elif path == '1.1.7':
                        ep1 = make_event_person('friend', status='alive', detail='nomad pack member',
                                                needs_validation='no')
                    elif path == '1.1.8':
                        ep1 = make_event_person('friend', status='alive', detail='local altcult member',
                                                needs_validation='no')
                    elif path == '1.1.9':
                        ep1 = make_event_person('friend', status='alive', detail='local boostergang member',
                                                needs_validation='no')
                    elif path == '1.1.10':
                        ep1 = make_event_person('combat teacher', status='alive', needs_validation='no')

        elif FRIEND_PATTERN.match(path):
            a = path.split('.', -1)
            ep1 = make_event_person('friend', status='alive', needs_validation='no')
            detail_num = int(a[2])
            ep1.current_relationship.detail = TABLE_FRIENDS.get_option(index=detail_num).re
            if path == '2.1.5' or path == '2.1.6':
                ep1.validation_needed = 'yes'

        elif ENEMY_PATTERN.match(path):
            print('enemy pattern')
            a = path.split('.', -1)
            print(a)
            ep1 = make_enemy()
            ep1.who = TABLE_ENEMY_TYPE.get_option(index=int(a[2])).re
            ep1.cause = TABLE_ENEMY_CAUSES.get_option(index=int(a[3])).re
            ep1.who_is_mad = TABLE_ENEMY_HATE.get_option(index=int(a[4])).re
            ep1.do = TABLE_ENEMY_DO.get_option(index=int(a[5])).re
            ep1.resources = TABLE_ENEMY_RESOURCES.get_option(index=int(a[6])).re

            if PATTERN_ENEMY_FRIEND.match(path) or PATTERN_ENEMY_EX_LOVER.match(path) or \
                    PATTERN_ENEMY_RELATIVE.match(path):
                print('enemy needs validation')
                ep1.validation_needed = 'yes'

        elif path == '3.1':
            ep1 = make_lover('alive')

        elif PATTERN_TRAGIC_LOVE.match(path):
            print('tragic love pattern')
            a = path.split('.', -1)
            print(a)
            if PATTERN_TRAGIC_LOVE_LOVER_DIED.match(path):
                detail_index = int(a[2])
                detail_text = TABLE_LOVE_TRAGIC.get_option(index=detail_index).re
                ep1 = make_tragic_lover('dead', detail=detail_text)
            elif PATTERN_TRAGIC_LOVE_LOVER_VANISHED.match(path):
                ep1 = make_tragic_lover('unknown', 'mysteriously vanished')
            else:
                ep1 = make_tragic_lover('alive', detail=TABLE_LOVE_TRAGIC.get_option(index=int(a[2])).re)
            ep1.mutual_feelings = TABLE_LOVE_MUTUAL_FEELINGS.get_option(index=int(a[3])).re

        elif PATTERN_LOVE_WITH_PROBLEMS.match(path):
            a = path.split('.', -1)
            d_text = TABLE_LOVE_PROBLEMS.get_option(index=int(a[2])).re
            ep1 = make_lover('alive', detail=d_text)

        elif ROMANCE_COMPLICATED_PATTERN.match(path):

            ep1 = make_lover('alive')
            if path == '3.5.1':
                print('3.5.1')
                ep2 = make_event_person(relationship='child', status='alive', needs_validation='yes')

            elif path == '3.5.2' or path == '3.5.3':
                print('3.5.2-3.5.3')

                # Your old lover just secretly showed up
                if path == '3.5.2':
                    ep2 = EventPerson(current_relationship=Relationships(relationship='ex-lover'), status='alive',
                                      validation_needed='yes')

                # Their old Lover just secretly showed up
                else:
                    ep2 = make_event_person(relationship='lovers ex', status='alive', needs_validation='no')

            # One of you had a kid in the past and they just showed up
            elif path == '3.5.4':
                ep2 = make_event_person(relationship='child', status='alive', needs_validation='no')
                # TODO - figure out how to make this matter

            # You have a terrible secret you are hiding from them
            elif path == '3.5.5':
                pass
            elif path == '3.5.6':
                ep2 = make_event_person(relationship='enemy', status='alive')
            elif path == '3.5.7':
                ep2 = make_event_person(relationship='lovers enemy', status='alive', needs_validation='no')

        if ep1 is not None and ep2 is not None:
            self.two_event_persons = TwoEventPersons(person1=ep1, person2=ep2)
        elif ep1 is not None:
            self.person = ep1
        if self.person is not None:
            self.person.random_all()
        if self.two_event_persons is not None:
            self.two_event_persons.person1.random_all()
            self.two_event_persons.person2.random_all()

    @staticmethod
    def try_loading_shortcut_description(path):
        short_option = LIFEPATH_SHORTCUTS_TABLE.get_option(identifier=path)
        if short_option:
            short_result = short_option.re
            short_array = short_result.split('@')
            return short_array[1]

    @staticmethod
    def transform_path_string_to_num_array(path):
        path_array = path.split('.', -1)
        num_array = []
        for cell in path_array:
            try:
                num_array.append(int(cell))
            except ValueError:
                pass
        return num_array

    @staticmethod
    def transform_path_array_to_string(path):
        string_path = ""
        for cell in path:
            string_path = string_path + str(cell) + '.'

        string_path = string_path[:-1]
        return string_path

    def _path_changed(self):
        num_array = self.transform_path_string_to_num_array(self.path)

        self.chain = event_menu.get_result_chain_string(*num_array)
        short_option = self.try_loading_shortcut_description(self.path)
        if short_option:
            self.desc = short_option
        else:
            decoded_chain, array = event_menu.decode_table_chain_string(self.chain)
            array_of_results = []
            for table in decoded_chain:
                option = table['option']
                array_of_results.append(option.re + " ")

            string_of_results = ''.join(array_of_results)
            self.desc = string_of_results
        if self.do_generate_event_persons:
            self.generate_event_persons(self.path)

    view = View(
        Tabbed(
            Group(
                HGroup(
                    Item('random_event', show_label=False),
                    Item('path', width=15),
                ),
                HGroup(
                    Item('age', width=2),
                    Item('desc', width=600, show_label=False),
                ),
                label='Event'),
            HGroup(
                Item('person', show_label=False),
                Item('two_event_persons', show_label=False),
                label='People involved')

        )
    )


class Lifepath(HasTraits):
    starting_age = Int()
    to_age = Int()
    random_lifepath = Button()
    save_lifepath = Button()
    gender = Enum(['male', 'female'])
    sexual_orientation = Enum('hetero', 'homo', 'both')
    events = List(Instance(Event()))

    def event_change_listener(self):
        print('some method')

    def generate_random_lifepath(self, starting_year, actor_age):
        self.events = []
        for i in range(starting_year, actor_age):
            e = Event(age=i, life_path_method=self.event_change_listener)
            e.random_life_event()
            self.events.append(e)

    def validate(self):
        num = 0
        self.correct_love_interests()
        while self.is_validation_needed() and num < 20:
            self.validate_lifepath(familymembers=None)
            num += 1
        print('validated lifepath with ' + str(num) + ' tries')

    def _random_lifepath_fired(self):
        self.generate_random_lifepath(self.starting_age, self.to_age)
        self.validate()

    def _save_lifepath_fired(self):
        self.save('Toni', 'PC')

    def correct_love_interests(self, actor_gender=None):
        if actor_gender is None:
            actor_gender = self.gender
        eps = self.collect_event_persons()
        for year, array in eps.iteritems():
            for ep in array:
                if ep.get_relationship() == 'lover':
                    if self.sexual_orientation == 'hetero':
                        if actor_gender == 'male' and ep.gender == 'male':
                            print('rerolling lover')
                            ep.random_all(gender='female')
                        elif actor_gender == 'female' and ep.gender == 'female':
                            print('rerolling lover')
                            ep.random_all(gender='male')
                    elif self.sexual_orientation == 'homo':
                        if actor_gender == 'male' and ep.gender == 'female':
                            print('rerolling lover')
                            ep.random_all(gender='male')
                        elif actor_gender == 'female' and ep.gender == 'male':
                            print('rerolling lover')
                            ep.random_all(gender='female')

    def collect_event_persons(self):
        event_persons = {}
        for event in self.events:
            if event.person is not None:
                event_persons[event.age] = [event.person]
            elif event.two_event_persons is not None:
                event_persons[event.age] = [event.two_event_persons.person1, event.two_event_persons.person2]
        return event_persons

    def search_empty_year(self, to_year):
        for e in self.events:
            if e.age < to_year:
                if e.path == '4':
                    return e.age
            else:
                break

    def search_event_of_age(self, age):
        for e in self.events:
            if e.age == age:
                return e

    def search_person_with_relation(self, relation, before_age):
        ep_dict = self.collect_event_persons()
        for year, array in ep_dict.iteritems():
            for ep in array:
                event = self.search_event_of_age(year)
                if ep.get_relationship() == relation:
                    if event.age < before_age:
                        return {'ep': ep, 'year': year}

    def is_validation_needed(self):
        ep_dict = self.collect_event_persons()
        for year, array in ep_dict.iteritems():
            for ep in array:
                if ep.validation_needed == 'yes':
                    return True
        return False

    def validate_lifepath(self, familymembers):
        ep_dict = self.collect_event_persons()
        ep_dict_keys = ep_dict.keys()
        ep_dict_keys.sort()

        # for year, array in ep_dict.iteritems():
        for year in ep_dict_keys:
            array = ep_dict[year]
            for ep in array:
                if ep.validation_needed == 'yes':
                    event = self.search_event_of_age(year)
                    path = event.path
                    if BETRAYEL_PATTERN_2.match(path):  # 1.2.4.3.X
                        self.bind_past_person(from_relation='friend', before_age=year, to_relation='ex-friend',
                                              to_detail='betrayed you', empty_year_path='2.1.r:1:10', to_event=event)
                    elif FRND_KILLED_PATTERN_1.match(path):
                        self.bind_past_person('friend', before_age=year, to_relation='ex-friend',
                                              to_detail='died accidentally',
                                              empty_year_path='2.1.r:1:10', to_event=event, to_status='dead')
                    elif FRND_KILLED_PATTERN_2.match(path) or FRND_KILLED_PATTERN_3.match(path):
                        self.bind_past_person('friend:relative:lover', before_age=year, to_relation='ex-ally',
                                              to_detail='murdered', empty_year_path='3.1', to_event=event,
                                              to_status='dead')
                    elif path == '2.1.5':
                        self.bind_past_person('lover', before_age=year, to_relation='friend', to_detail='old lover',
                                              empty_year_path='3.1', to_event=event)
                    elif path == '2.1.6':
                        # 2.2.10.5.2.3.3
                        self.bind_past_person('enemy', before_age=year, to_relation='friend', to_detail='old enemy',
                                              empty_year_path='2.2.r:1:10.r:1:10.r:1:3.r:1:5.r:1:6', to_event=event)
                    elif PATTERN_ENEMY_FRIEND.match(path):
                        self.bind_past_person('friend', before_age=year, to_relation='enemy', to_detail='ex friend',
                                              empty_year_path='2.1.r:1:10', to_event=event)
                    elif PATTERN_ENEMY_EX_LOVER.match(path):
                        self.bind_past_person('lover', before_age=year, to_relation='enemy', to_detail='ex lover',
                                              empty_year_path='3.1', to_event=event)
                    elif PATTERN_ENEMY_RELATIVE.match(path):
                        # TODO - familymembers here
                        # self.bind_past_person('relative', before_age=year, to_relation='enemy', to_detail='relative',
                        #                       empty_year_path='2.1.8', to_event=event)
                        pass
                    elif path == '3.5.1':
                        event.two_event_persons.person2.age = self.to_age - year
                        event.two_event_persons.person2.validation_needed = 'no'
                    elif path == '3.5.2':
                        self.bind_past_person(from_relation='lover', before_age=year, to_relation='lover',
                                              to_detail='secret', to_event=event, two_event_persons_target='ep2',
                                              empty_year_path='3.1')
                    elif path == '3.5.6':
                        self.bind_past_person(from_relation='enemy', before_age=year, to_relation='enemy',
                                              to_detail='showed up', to_event=event, two_event_persons_target='ep2',
                                              empty_year_path='2.2.r:1:10.r:1:10.r:1:3.r:1:5.r:1:6')

    def bind_past_person(self, from_relation, before_age, to_relation, to_detail, empty_year_path, to_event,
                         to_status=None, two_event_persons_target='ep1'):
        print ('need to bind: ' + from_relation + ' before age: ' + str(before_age) + ' to relation: ' + to_relation)
        ep = None
        year = None
        from_event = None
        search_results = None
        if MANY_RELATIONS_SEARCH_PATTERN.match(from_relation):
            search_array = from_relation.split(':', -1)
            for search in search_array:
                search_results = self.search_person_with_relation(search, before_age=before_age)
                if search_results is not None:
                    break
        else:
            search_results = self.search_person_with_relation(from_relation, before_age=before_age)
        if search_results is not None:
            ep = search_results['ep']
            year = search_results['year']
            print('found a match. ep: ' + ep.name + ' year: ' + str(year))
            from_event = self.search_event_of_age(year)

        if ep is not None:
            ep.set_relationship(to_relation, detail=to_detail)
            ep.validation_needed = 'no'
            # return ep
            if to_status is not None:
                ep.status = to_status
            if to_event.person is not None:
                to_event.person = ep
            elif to_event.two_event_persons is not None:
                if two_event_persons_target == 'ep1':
                    to_event.two_event_persons.person1 = ep
                else:
                    to_event.two_event_persons.person2 = ep
            from_event.locked = True
            to_event.locked = True
            print('successfully binded ep to year: ' + str(to_event.age))
        else:
            empty_age = self.search_empty_year(before_age)
            if empty_age is not None:
                empty_year = self.search_event_of_age(empty_age)
                print('found empty year')
                a = empty_year_path.split('.', -1)
                r = []
                for c in a:
                    if PATTERN_RANDOM_PATH.match(c):
                        a2 = c.split(':', -1)
                        x1 = int(a2[1])
                        x2 = int(a2[2])
                        r.append(str(randint(x1, x2)))

                    else:
                        r.append(c)
                    r.append('.')
                del r[-1]
                path = ''.join(r)
                empty_year.path = path
                print('empty year: ' + str(empty_age) + ' changed to: ' + str(path))


                # print(path)
            else:
                print('illegal event, rerolling')
                if to_event.locked:
                    print('this event is locked')
                else:
                    to_event.random_life_event()

    def save(self, actor_role, actor_name):
        db_mgr = DBManager()
        for event in self.events:
            db_mgr.events.add_event(actor_role=actor_role, actor_name=actor_name, age=event.age,
                                    event_chain=event.chain)
            if event.person is not None:
                event.person.save()
                event.person.save_relation(actor_role, actor_name, event.age)
            elif event.two_event_persons is not None:
                event.two_event_persons.person1.save()
                event.two_event_persons.person2.save()
                event.two_event_persons.person1.save_relation(actor_role, actor_name, event.age)
                event.two_event_persons.person2.save_relation(actor_role, actor_name, event.age)

    def load(self, actor_role, actor_name):
        db_mgr = DBManager()
        events = db_mgr.events.get_all_events_of_actor(actor_role, actor_name)
        if events is not None:
            for event in events:
                chain = event.event_chain
                e = Event()
                e.load_event_from_chain(chain)
                e.age = event.age
                self.events.append(e)
                amount_of_eps = db_mgr.relations.get_relation_count_of_age(actor_role, actor_name, e.age)
                eps = db_mgr.relations.get_persons_related_to_event(actor_role, actor_name, e.age)
                ep1 = None
                ep2 = None
                print('amount of eps on loading: ' + str(amount_of_eps))
                if amount_of_eps == 1:
                    ep1 = eps[0]
                    print(ep1)
                elif amount_of_eps == 2:
                    ep1 = eps[0]
                    ep2 = eps[1]
                    print(ep2)
                if amount_of_eps > 0:
                    if PATTERN_TRAGIC_LOVE.match(e.path):
                        e.person = TragicLove()
                        e.person.load(actor_role, actor_name, e.age, ep1.to_person.name)
                    elif ENEMY_PATTERN.match(e.path):
                        e.person = Enemy
                        e.person.load_relation(actor_role, actor_name, e.age)
                    else:

                        if amount_of_eps == 1:
                            e.person = EventPerson()
                            e.person.load(ep1.to_person.name)
                        elif amount_of_eps == 2:
                            e.two_event_persons = TwoEventPersons()
                            e.two_event_persons.person1 = EventPerson()
                            e.two_event_persons.person2 = EventPerson()
                            e.two_event_persons.person1.load(ep1.to_person.name)
                            e.two_event_persons.person2.load(ep2.to_person.name)

    view = View(
        Tabbed(
            Item('events', show_label=False, editor=ListEditor(style='custom')),
            Group(
                Item('starting_age'),
                Item('to_age'),
                Item('gender'),
                Item('sexual_orientation'),
                Item('random_lifepath'),
                Item('save_lifepath'),
                label='Settings')

        )

    )



class Family(HasTraits):
    # family_name = String()
    # actor_age = Int()
    father = Instance(EventPerson, ())
    mother = Instance(EventPerson, ())
    siblings = List(Instance(Sibling, ()))
    random_parents = Button()

    def set_parent_status(self, status):
        self.mother.status = status
        self.father.status = status

    def correct_sibling_ages(self, actor_age):
        older_by = 1
        younger_by = 1
        for sibling in self.siblings:
            coin = randint(1, 2)
            if coin == 1:
                sibling.age = actor_age + older_by
                older_by += 1
            else:
                sibling.age = actor_age - younger_by
                younger_by += 1

        self.correct_parent_ages(actor_age + older_by)

    def correct_parent_ages(self, oldest_sibling_age):
        max_age = oldest_sibling_age + 30
        min_age = oldest_sibling_age + 16
        self.mother.random_age(min_age, max_age)
        self.father.random_age(min_age, max_age)

    def collect_family(self):
        f = []
        for sibling in self.siblings:
            f.append(sibling)
        f.append(self.mother)
        f.append(self.father)
        return f

    def roll_parents(self):
        # parents_max_age = self.actor_age + 30

        self.mother.random_all(gender='female')
        self.father.random_all(gender='male')

        self.mother.set_relationship('parent')
        self.father.set_relationship('parent')

    view = View(
        HGroup(
            Item('father', style='custom'),
            Item('mother', style='custom')
        ),
        Item('siblings', editor=ListEditor(style='custom'))
    )


class FamilyBackground(HasTraits):
    childhood_enviroment = Enum(TABLE_CHILDHOOD_ENVIROMENT.results())
    childhood_event = Enum(TABLE_CHILDHOOD_EVENT.results())
    your_parents_are = Enum(TABLE_PARENTS_ARE.results())
    your_parents_were = Enum(TABLE_PARENT_RANK.results())
    parent_event = Enum(TABLE_PARENT_EVENT.results())
    parent_problems = Enum(PARENT_PROBLEMS_ARRAY)
    family_status = Enum(TABLE_FAMILY_STATUS.results())
    family_tragedy = Enum(FAMILY_TRAGEDY_ARRAY)
    family_contact = Enum(TABLE_FAMILY_CONTACT.results())
    siblings = Int()
    family = Instance(Family, ())

    def _family_status_default(self):
        return TABLE_FAMILY_STATUS.get_result(index=2)

    def _parent_event_changed(self):
        if self.parent_event == TABLE_PARENT_EVENT.get_result(index=1):
            self.parent_problems = 'none'
            self.family.father.status = 'alive'
            self.family.mother.status = 'alive'
        else:
            self.parent_problems = TABLE_PARENT_PROBLEMS.random_result()
            for i in range(1, 11):
                print(str(i) + ': ' + TABLE_PARENT_PROBLEMS.get_result(index=i))

    def _parent_problems_changed(self):
        p = self.parent_problems
        warfare_death = TABLE_PARENT_PROBLEMS.get_result(index=1)
        accident_death = TABLE_PARENT_PROBLEMS.get_result(index=2)
        murder_death = TABLE_PARENT_PROBLEMS.get_result(index=3)

        n_knew = TABLE_PARENT_PROBLEMS.get_result(index=5)
        # hiding = TABLE_PARENT_PROBLEMS.get_result(index=6)
        street = TABLE_PARENT_PROBLEMS.get_result(index=8)

        if p == 'none':
            self.family.set_parent_status('alive')
        elif p == warfare_death or p == accident_death or p == murder_death:
            self.family.set_parent_status('dead')
        elif p == n_knew or p == street:
            self.family.set_parent_status('unknown')
        else:
            self.family.set_parent_status('missing')

    def _family_status_changed(self):
        if self.family_status == TABLE_FAMILY_STATUS.get_result(index=2):
            self.family_tragedy = 'none'
        else:
            self.family_tragedy = TABLE_FAMILY_TRAGEDY.random_result()

    def _your_parents_are_changed(self):
        self.family.roll_parents()

    def _siblings_changed(self):
        self.family.siblings = []
        for i in range(0, self.siblings):
            s = Sibling()
            s.random_sibling()
            # s.set_last_name(self.family.family_name)
            self.family.siblings.append(s)

    def random_enviroment(self):
        self.childhood_enviroment = TABLE_CHILDHOOD_ENVIROMENT.random_result()

    def random_childhood_event(self):
        self.childhood_event = TABLE_CHILDHOOD_EVENT.random_result()

    def random_parents(self):
        self.your_parents_are = TABLE_PARENTS_ARE.random_result()

    def random_parent_rank(self):
        self.your_parents_were = TABLE_PARENT_RANK.random_result()

    def random_parent_event(self):
        self.parent_event = TABLE_PARENT_EVENT.random_result()

    def random_parent_problems(self):
        self.parent_problems = TABLE_PARENT_PROBLEMS.random_result()

    def random_family_status(self):
        self.family_status = TABLE_FAMILY_STATUS.random_result()

    def random_family_tragedy(self):
        self.family_tragedy = TABLE_FAMILY_TRAGEDY.random_result()

    def random_family_contact(self):
        self.family_contact = TABLE_FAMILY_CONTACT.random_result()

    def random_sibling_amount(self):
        self.siblings = randint(0, 7)

    def random_all(self):
        self.random_enviroment()
        self.random_childhood_event()
        self.random_parents()
        self.random_parent_rank()
        self.random_parent_event()
        self.random_family_status()
        self.random_family_contact()
        self.random_sibling_amount()

    view = View(
        Tabbed(
            Group(
                Item('childhood_enviroment'),
                Item('childhood_event'),
                Item('your_parents_are'),
                Item('your_parents_were'),
                HGroup(
                    Item('parent_event'),
                    VGroup(
                        Item('parent_problems')
                    )
                ),
                HGroup(
                    Item('family_status'),
                    Item('family_tragedy')

                ),
                Item('siblings'),
                Item('family_contact'),
                label='background'
            ),
            Item('family', style='custom', show_label=False)
        )

    )


class FamilyBackgroundWithControls(HasTraits):
    family_background = Instance(FamilyBackground, ())
    ch_envi = String()
    ch_evnt = String()
    parents = String()
    p_rank = String()
    p_event = String()
    p_probl = String()
    f_statu = String()
    f_trage = String()
    f_conta = String()
    sibling = Int()

    all = Button()
    enviroment = Button()
    child_event = Button()
    parent = Button()
    parent_rank = Button()
    parent_event = Button()
    parent_problem = Button()
    family_status = Button()
    family_tragedy = Button()
    family_contact = Button()
    siblings = Button()

    def update_fields(self):
        self.ch_envi = self.family_background.childhood_enviroment
        self.ch_evnt = self.family_background.childhood_event
        self.parents = self.family_background.your_parents_are
        self.p_rank = self.family_background.your_parents_were
        self.p_event = self.family_background.parent_event
        self.p_probl = self.family_background.parent_problems
        self.f_statu = self.family_background.family_status
        self.f_trage = self.family_background.family_tragedy
        self.f_conta = self.family_background.family_contact
        self.sibling = self.family_background.siblings

    def _enviroment_fired(self):
        self.family_background.random_enviroment()
        self.update_fields()

    def _child_event_fired(self):
        self.family_background.random_childhood_event()
        self.update_fields()

    def _parent_fired(self):
        self.family_background.random_parents()
        self.update_fields()

    def _parent_rank_fired(self):
        self.family_background.random_parent_rank()
        self.update_fields()

    def _parent_event_fired(self):
        self.family_background.random_parent_event()
        self.update_fields()

    def _parent_problem_fired(self):
        self.family_background.random_parent_problems()
        self.update_fields()

    def _family_status_fired(self):
        self.family_background.random_family_status()
        self.update_fields()

    def _family_tragedy_fired(self):
        self.family_background.random_family_tragedy()
        self.update_fields()

    def _family_contact_fired(self):
        self.family_background.random_family_contact()
        self.update_fields()

    def _siblings_fired(self):
        self.family_background.random_sibling_amount()
        self.update_fields()

    def _all_fired(self):
        self.family_background.random_all()
        self.update_fields()

    view = View(
        Tabbed(
            Item('family_background', style='custom', show_label=False),
            HGroup(
                VGroup(
                    Item('ch_envi', style='readonly'),
                    Item('ch_evnt', style='readonly'),
                    Item('parents', style='readonly'),
                    Item('p_rank', style='readonly'),
                    Item('p_event', style='readonly'),
                    Item('p_probl', style='readonly'),
                    Item('f_statu', style='readonly'),
                    Item('f_trage', style='readonly'),
                    Item('f_conta', style='readonly'),
                    Item('sibling', style='readonly')
                ),
                VGroup(
                    Item('enviroment', show_label=False),
                    Item('child_event', show_label=False),
                    Item('parent', show_label=False),
                    Item('parent_rank', show_label=False),
                    Item('parent_event', show_label=False),
                    Item('parent_problem', show_label=False),
                    Item('family_status', show_label=False),
                    Item('family_tragedy', show_label=False),
                    Item('family_contact', show_label=False),
                    Item('siblings', show_label=False),
                    Item('all', show_label=False),
                    label='random', show_border=True
                ), label='Controls'
            )
        )

    )


class ActorBackground(HasTraits):
    lifepath = Instance(Lifepath, ())
    family = Instance(FamilyBackgroundWithControls, ())

    def validate_lifepath(self, actor_gender, sexual_orientation):
        if sexual_orientation == 'hetero':
            pass

    view = View(
        Tabbed(
            Item('family', style='custom', show_label=False),
            Item('lifepath', style='custom', show_label=False)
        )
    )


if __name__ == '__main__':
    # l = LifepathShortcutMaker()
    # l = Lifepath()
    # l.configure_traits()
    ab = ActorBackground()
    # ab.lifepath.generate_random_lifepath(16, 25)
    # ab.lifepath.save('pc', 'toni')
    # ab.lifepath.load('pc', 'toni')
    ab.configure_traits()
