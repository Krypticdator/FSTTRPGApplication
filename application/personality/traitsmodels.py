from __future__ import print_function

from traits.api import HasTraits, List, Button, Enum, Instance, String, Method, TraitError
from traitsui.api import View, Item, CheckListEditor, Group, HGroup, Handler, Action, Menu, MenuBar, Tabbed

from application.characterloader.traitsmodels import CharacterName
from structures import Personality as PersonalityModel

personality = PersonalityModel()


class PersonalityHandler(Handler):
    def do_save(self, UIInfo):
        status = personality.save(role=UIInfo.object.character_name.role,
                                  actor_name=UIInfo.object.character_name.get_name())
        UIInfo.object.messages = status

    def do_load(self, UIInfo):
        try:
            personality.load(role=UIInfo.object.character_name.role, name=UIInfo.object.character_name.get_name())
            UIInfo.object.personality.personality.update_from_model()
        except Exception:
            print('could not load the name')


class ChangeListener(Handler):
    def object__updated_changed(self, info):
        print('object changed')

    def setattr(self, info, object, name, value):
        Handler.setattr(self, info, object, name, value)


action_save = Action(name='Save', action='do_save')
action_load = Action(name='Load', action='do_load')


class SendsSignal(HasTraits):
    signal_method = Method()

    def send_signal(self):
        try:
            self.signal_method()
        except TypeError:
            print('signal method not defined')


class Phobias(SendsSignal):
    # phobias = List(editor=CheckListEditor(values=personality.phobias.source_table.results(), cols=6))
    phobias = List()
    random_phobia = Button()

    traits_view = View(
        Item('phobias', editor=CheckListEditor(values=personality.phobias.source_table.results(), cols=6)),
        Item('random_phobia', show_label=False)
    )

    def _random_phobia_fired(self):
        self.phobias = personality.phobias.get_random()

    def _phobias_changed(self):
        personality.phobias.value = self.phobias
        self.send_signal()


class Disorders(SendsSignal):
    # disorders = List(editor=CheckListEditor(values=personality.disorders.source_table.results(), cols=3))
    disorders = List()
    random_disorder = Button()

    def _random_disorder_fired(self):
        self.disorders = personality.disorders.get_random()

    def _disorders_changed(self):
        personality.disorders.value = self.disorders
        self.send_signal()

    view = View(
        Item('disorders', style='custom',
             editor=CheckListEditor(values=personality.disorders.source_table.results(), cols=3)),
        Item('random_disorder', show_label=False)
    )


class Quirks(SendsSignal):
    quirks = List(editor=CheckListEditor(values=personality.quirks.source_table.results(), cols=3))
    random_quirks = Button()

    def _random_quirks_fired(self):
        self.quirks = personality.quirks.get_random()

    def _quirks_changed(self):
        personality.quirks.value = self.quirks
        self.send_signal()

    view = View(
        Item('quirks', style='custom'),
        Item('random_quirks', show_label=False)
    )


class Hair(SendsSignal):
    hairstyles = List(editor=CheckListEditor(values=personality.hairstyle.source_table.results(), cols=2))
    random_hairstyle = Button()

    def _random_hairstyle_fired(self):
        self.hairstyles = personality.hairstyle.get_random()

    def _hairstyles_changed(self):
        personality.hairstyle.value = self.hairstyles
        self.send_signal()

    view = View(
        Item('hairstyles', style='custom'),
        Item('random_hairstyle', show_label=False)
    )


class Clothes(SendsSignal):
    clothes = List(editor=CheckListEditor(values=personality.clothes.source_table.results(), cols=2))
    random_clothes = Button()

    def _random_clothes_fired(self):
        self.clothes = personality.clothes.get_random()

    def _clothes_changed(self):
        personality.clothes.value = self.clothes
        self.send_signal()

    view = View(
        Item('clothes', style='custom'),
        Item('random_clothes', show_label=False)
    )


class Affections(SendsSignal):
    affections = List(editor=CheckListEditor(values=personality.affections.source_table.results(), cols=2))
    random_affection = Button()

    def _random_affection_fired(self):
        self.affections = personality.affections.get_random()

    def _affections_changed(self):
        personality.affections.value = self.affections
        self.send_signal()

    view = View(
        Item('affections', style='custom'),
        Item('random_affection', show_label=False)
    )


class Personality(SendsSignal):
    prime_motivation = Enum(personality.prime_motivation.source_table.results())
    most_valued_person = Enum(personality.most_valued_person.source_table.results())
    most_valued_posession = Enum(personality.most_valued_posession.source_table.results())
    how_feels_about_most_people = Enum(personality.how_feels_about_most_people.source_table.results())
    inmode = Enum(personality.inmode.source_table.results())
    exmode = Enum(personality.exmode.source_table.results())
    quirks = Instance(Quirks, ())
    disorders = Instance(Disorders, ())
    phobias = Instance(Phobias, ())
    hairstyle = Instance(Hair, ())
    clothes = Instance(Clothes, ())
    affections = Instance(Affections, ())

    def _quirks_default(self):
        return Quirks(signal_method=self.signal_method)

    def _disorders_default(self):
        return Disorders(signal_method=self.signal_method)

    def _phobias_default(self):
        return Phobias(signal_method=self.signal_method)

    def _hairstyle_default(self):
        return Hair(signal_method=self.signal_method)

    def _clothes_default(self):
        return Clothes(signal_method=self.signal_method)

    def _affections_default(self):
        return Affections(signal_method=self.signal_method)

    def _prime_motivation_changed(self):
        personality.prime_motivation.value = self.prime_motivation
        print(personality.prime_motivation.value)
        self.send_signal()

    def _most_valued_person_changed(self):
        personality.most_valued_person.value = self.most_valued_person
        self.send_signal()

    def _most_valued_posession_changed(self):
        personality.most_valued_posession.value = self.most_valued_posession
        self.send_signal()

    def _how_feels_about_most_people_changed(self):
        personality.how_feels_about_most_people.value = self.how_feels_about_most_people
        self.send_signal()

    def _inmode_changed(self):
        personality.inmode.value = self.inmode
        self.send_signal()

    def _exmode_changed(self):
        personality.exmode.value = self.exmode
        self.send_signal()

    def update_from_model(self):
        self.prime_motivation = personality.prime_motivation.value
        self.most_valued_person = personality.most_valued_person.value
        self.most_valued_posession = personality.most_valued_posession.value
        self.how_feels_about_most_people = personality.how_feels_about_most_people.value
        self.inmode = personality.inmode.value
        self.exmode = personality.exmode.value
        self.quirks.quirks = personality.quirks.value
        self.disorders.disorders = personality.disorders.value
        self.phobias.phobias = personality.phobias.value
        self.hairstyle.hairstyles = personality.hairstyle.value
        self.clothes.clothes = personality.clothes.value
        self.affections.affections = personality.affections.value
        self.send_signal()

    traits_view = View(
        HGroup(
            Group(
                Item('prime_motivation'),
                Item('most_valued_person'),
                Item('most_valued_posession'),
                Item('how_feels_about_most_people'),
                Item('inmode'),
                Item('exmode'),
                HGroup(
                    Group(
                        Item('quirks'),
                        Item('disorders')

                    ),
                    Group(
                        Item('hairstyle'),
                        Item('clothes')

                    ),
                    Group(
                        Item('affections'),
                        Item('phobias'),
                    )
                )
            ),
        ),
    )


class PersonalityRandomizer(HasTraits):
    personality = Instance(Personality, ())
    primem = String()
    valper = String()
    valpos = String()
    fappl = String()
    inmod = String()
    exmod = String()
    qurks = List(editor=CheckListEditor(values=[], cols=1))
    dsrds = List(editor=CheckListEditor(values=[], cols=1))
    phbas = List(editor=CheckListEditor(values=[], cols=1))
    hairs = List(editor=CheckListEditor(values=[], cols=1))
    clths = List(editor=CheckListEditor(values=[], cols=1))
    ffcns = List(editor=CheckListEditor(values=[], cols=1))

    random_motivation = Button()
    random_valued_person = Button()
    random_posession = Button()
    random_feels = Button()
    random_inmode = Button()
    random_exmode = Button()

    random_all = Button()

    def signal_receiver(self):
        try:
            self.primem = personality.prime_motivation.value
            self.valper = personality.most_valued_person.value
            self.valpos = personality.most_valued_posession.value
            self.fappl = personality.how_feels_about_most_people.value
            self.inmod = personality.inmode.value
            self.exmod = personality.exmode.value
            self.qurks = personality.quirks.value
            self.dsrds = personality.disorders.value
            self.phbas = personality.phobias.value
            self.hairs = personality.hairstyle.value
            self.clths = personality.clothes.value
            self.ffcns = personality.affections.value
        except TraitError:
            print('could not update readonly stats')

    def _personality_default(self):
        return Personality(signal_method=self.signal_receiver)

    def _random_motivation_fired(self):
        self.personality.prime_motivation = personality.prime_motivation.get_random()

    def _random_valued_person_fired(self):
        self.personality.most_valued_person = personality.most_valued_person.get_random()

    def _random_posession_fired(self):
        self.personality.most_valued_posession = personality.most_valued_posession.get_random()

    def _random_feels_fired(self):
        self.personality.how_feels_about_most_people = personality.how_feels_about_most_people.get_random()

    def _random_inmode_fired(self):
        self.personality.inmode = personality.inmode.get_random()

    def _random_exmode_fired(self):
        self.personality.exmode = personality.exmode.get_random()

    def _random_all_fired(self):
        personality.random_all()
        self.personality.update_from_model()

    view = View(
        Tabbed(
            Item('personality', style='custom', show_label=False),
            HGroup(
                Group(
                    Item('primem', style='readonly'),
                    Item('valper', style='readonly'),
                    Item('valpos', style='readonly'),
                    Item('fappl', style='readonly'),
                    Item('inmod', style='readonly'),
                    Item('exmod', style='readonly'),
                    Item('qurks', style='readonly'),
                    Item('dsrds', style='readonly'),
                    Item('phbas', style='readonly'),
                    Item('hairs', style='readonly'),
                    Item('clths', style='readonly'),
                    Item('ffcns', style='readonly')
                ),
                Group(
                    Item('random_motivation', show_label=False),
                    Item('random_valued_person', show_label=False),
                    Item('random_posession', show_label=False),
                    Item('random_feels', show_label=False),
                    Item('random_inmode', show_label=False),
                    Item('random_exmode', show_label=False),
                    Item('random_all', show_label=False)
                ),

            ),
        ),
    )


class Standalone(HasTraits):
    character_name = Instance(CharacterName, ())
    messages = String()
    personality = Instance(PersonalityRandomizer, ())

    view = View(
        Item('character_name', style='custom', show_label=False),
        Item('messages', style='readonly'),
        Item('personality', style='custom', show_label=False),
        menubar=MenuBar(Menu(action_save, action_load, name='File')),
        handler=PersonalityHandler()
    )

    def _character_name_default(self):
        return CharacterName(name_change_handler=self.load_personality)

    def load_personality(self):
        try:
            personality.load(role=self.character_name.role, name=self.character_name.get_name())
            self.personality.personality.update_from_model()
        except Exception:
            print('could not load the name')


if __name__ == '__main__':
    st = Standalone()
    st.configure_traits()
