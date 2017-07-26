from __future__ import print_function

from traits.api import HasTraits, Enum, String, Instance, Method, ListStr, Button, Dict
from traitsui.api import View, Item, HGroup, ListStrEditor

from database import DBManager
from models import JsonListOfActors

list_of_actors = JsonListOfActors()



class Name(HasTraits):
    name = String()
    change_listener = Method()
    view = View(
        Item('name')
    )

    def _name_changed(self):
        self.change_listener()


class Loader(HasTraits):
    role = Enum('NPC', 'PC', 'INPC')
    selection = String()
    name_field = Instance(Name)
    source = Enum('local', 'cloud')

    choose_character = ListStr(editor=ListStrEditor(selected='selection'))
    load = Button()
    choose = Button()
    chosen = Dict()
    view = View(
        Item('role'),
        Item('source'),
        Item('load', show_label=False),
        Item('choose_character'),
        Item('choose'),
        Item('chosen', style='custom')
    )

    def _choose_fired(self):
        if self.source == 'cloud':
            self.chosen = list_of_actors.actors[self.selection]
        self.name_field.name = self.selection

    def _load_fired(self):
        if self.source == 'cloud':
            list_of_actors.load(self.role)
            self.choose_character = list_of_actors.get_name_list()
        else:
            db = DBManager()
            actors = db.actors.get_all_with_role(self.role)
            names = []
            for actor in actors:
                names.append(str(actor.name))
            self.choose_character = names


class CharacterName(HasTraits):
    role = Enum('NPC', 'PC', 'INPC')
    name = Instance(Name, ())
    loader = Instance(Loader)
    name_change_handler = Method()
    save = Button()

    view = View(
        # Item('actor_db_file_location', show_label=False, style='custom'),
        HGroup(
            Item('role'),
            Item('name', style='custom', show_label=False),
            Item('loader', show_label=False),
            # Item('save', show_label=False)
        )
    )

    def get_name(self):
        return self.name.name

    def set_name(self, new_name):
        self.name.name = new_name

    def _loader_default(self):
        return Loader(name_field=self.name)

    def _name_default(self):
        return Name(change_listener=self.name_change_handler)
        # n.master = self.load_handler

    def _save_fired(self):
        db = DBManager()
        db.actors.add_or_get(role=self.role, name=self.get_name())

    def _name_changed(self):
        print('hello')


class Foo(object):
    def bar(self):
        print('foobar')


if __name__ == '__main__':
    foo = Foo()
    c = CharacterName(name_change_handler=foo.bar)

    c.configure_traits()
