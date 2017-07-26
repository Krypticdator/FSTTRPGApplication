from random import randint

from application.tables.models import Table

event_menu = Table('event_menu')


class Event(object):
    def __init__(self, owner, year, owners_age):
        super(Event, self).__init__()
        self.year = year
        self.lifepath_chain = ""
        self.owner = owner
        self.owners_age = owners_age

    def assign_random_event(self):
        event_menu.calc_max()
        r = randint(1, event_menu.max)
        self.lifepath_chain = event_menu.get_random_chain_string(r)


if __name__ == '__main__':
    e = Event('toni', 2035, 18)
    e.assign_random_event()
    print(e.lifepath_chain)
