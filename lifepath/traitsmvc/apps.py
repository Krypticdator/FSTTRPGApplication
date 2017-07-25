from traits.api import HasTraits, String, Button, Instance
from traitsui.api import Item, VGroup, View, Tabbed

from application.lifepath.globals import TABLE_EVENT_MENU
from application.lifepath.traitsmvc.views.family import FamilyBackgroundWithControlsView
from application.lifepath.traitsmvc.views.lifepath import LifepathView
from application.tables.utilities import export_to_aws


class LifepathShortcutMaker(HasTraits):
    identifier = String()
    chain_string = String()
    decoded_chain = String()
    short_description = String()
    upload = Button()

    def _identifier_changed(self):
        params_array = self.identifier.split('.', -1)
        numbers_array = []
        for param in params_array:
            try:
                numbers_array.append(int(param))
            except ValueError:
                pass
        table = TABLE_EVENT_MENU
        try:
            chain_string = table.get_result_chain_string(*numbers_array)
            self.chain_string = chain_string
            decoded_chain, array = table.decode_table_chain_string(chain_string)
            array_of_results = []
            for table in decoded_chain:
                option = table['option']
                array_of_results.append(option.re + " ")

            string_of_results = ''.join(array_of_results)
            self.decoded_chain = string_of_results
        except TypeError:
            print('type-error')

    def _upload_fired(self):
        identifier = self.identifier
        params_array = self.identifier.split('.', -1)
        numbers_array = []
        for param in params_array:
            try:
                int(param)
                numbers_array.append(param)
            except ValueError:
                pass
        numstring = ''.join(numbers_array)
        result = self.chain_string + "@" + self.short_description
        export_to_aws(name='lifepath_shortcuts', identifier=identifier, fr=numstring, to=numstring, re=result,
                      leads_to=None)
        print('done')

    view = View(
        VGroup(
            Item('identifier'),
            Item('chain_string', width=600),
            Item('decoded_chain', width=600),
            Item('short_description'),
            Item('upload', show_label=False)
        )
    )


class ActorBackgroundWidget(HasTraits):
    lifepath = Instance(LifepathView, ())
    family = Instance(FamilyBackgroundWithControlsView, ())

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
    ab = ActorBackgroundWidget()
    # ab.lifepath.generate_random_lifepath(16, 25)
    # ab.lifepath.save('pc', 'toni')
    # ab.lifepath.load('pc', 'toni')
    ab.configure_traits()
