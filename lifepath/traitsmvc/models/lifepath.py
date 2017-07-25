from random import randint

from traits.api import Button, Method, Bool

from application.lifepath.models import event_menu
from application.lifepath.traitsmvc.models.eventpersons import *


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

