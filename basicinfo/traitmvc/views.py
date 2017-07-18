from traits.api import HasTraits, Button, Instance, String, Int
from traitsui.api import View, Item, HGroup, Menu, MenuBar, OKButton, Tabbed, VGroup

from handlers import BasicInfoHandler, action_save, action_load, action_random_age, action_random_alias, \
    action_random_all, action_random_name, action_random_birthday, action_upload
from models import BasicInfo


class BasicInfoDefaultView(BasicInfo):
    view = View(

        Item('character_name', style='custom', show_label=False),
        HGroup(
            Item('gender'),
            Item('country'),
            Item('age'),
            Item('birthday'),
        ),
        HGroup(
            Item('alias'),

        )

    )


class BasicInfoTabbedView(HasTraits):
    basic_info_view = Instance(BasicInfoDefaultView, ())
    random_name = Button()
    random_alias = Button()
    random_age = Button()
    random_dob = Button()
    random_all = Button()
    name = String()
    alias = String()
    age = Int()
    dob = String()

    def _random_name_fired(self):
        self.basic_info_view.random_name()
        self.name = self.basic_info_view.character_name.get_name()

    def _random_alias_fired(self):
        self.basic_info_view.random_alias()
        self.alias = self.basic_info_view.alias

    def _random_age_fired(self):
        self.basic_info_view.random_age()
        self.age = self.basic_info_view.age

    def _random_dob_fired(self):
        self.basic_info_view.random_dob()
        self.dob = self.basic_info_view.birthday

    def _random_all_fired(self):
        self._random_name_fired()
        self._random_alias_fired()
        self._random_age_fired()
        self._random_dob_fired()

    view = View(
        Tabbed(
            Item('basic_info_view', style='custom', show_label=False),
            VGroup(
                HGroup(
                    Item('random_all', show_label=False),
                    Item('random_name', show_label=False),
                    Item('random_alias', show_label=False),
                    Item('random_age', show_label=False),
                    Item('random_dob', show_label=False)
                ),
                HGroup(
                    Item('name'),
                    Item('alias'),

                ),
                HGroup(
                    Item('age'),
                    Item('dob')
                ),
                label='controls'
            )
        )
    )


class Standalone(HasTraits):
    basic_info = Instance(BasicInfoDefaultView, ())

    view = View(
        Item('basic_info', style='custom', show_label=False),
        menubar=MenuBar(Menu(action_upload, action_save, action_load, name='File')),
        # Item('upload', show_label=False),
        handler=BasicInfoHandler(),
        buttons=[OKButton, action_random_all, action_random_name, action_random_alias, action_random_age,
                 action_random_birthday]
    )


if __name__ == '__main__':
    b = Standalone()
    b.configure_traits()
    # b.edit_traits()
