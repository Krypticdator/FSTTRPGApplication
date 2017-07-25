from random import randint

from traits.api import HasTraits, Instance, Button, List, Enum, Int, String

from application.lifepath.globals import *
from application.lifepath.traitsmvc.models.eventpersons import EventPerson, Sibling


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
