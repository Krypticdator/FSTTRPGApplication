from traits.api import HasTraits, Instance, Button
from traitsui.api import Group, Item, Tabbed, View

from fsttrpgattributes.traitsmvc.views import AllAttributeListsTabbedView
from fsttrpgbasicinfo.traitmvc.views import BasicInfoTabbedView
from fsttrpglifepath.traitsmodels import Lifepath
from fsttrpgpersonality.traitsmodels import PersonalityRandomizer, personality as PERSONALITY
from fsttrpgprimarystats.traitsmodels import Stats


class CharacterCreatorFull(HasTraits):
    info = Instance(BasicInfoTabbedView, ())
    personality = Instance(PersonalityRandomizer, ())
    stats = Instance(Stats, ())
    attributes = Instance(AllAttributeListsTabbedView, ())
    lifepath = Instance(Lifepath, ())
    save = Button()
    load = Button()

    def _save_fired(self):
        self.info.basic_info_view.save()
        name = self.info.basic_info_view.character_name.get_name()
        role = self.info.basic_info_view.character_name.role
        PERSONALITY.save(role=role, actor_name=name)
        self.stats.save(name, role)
        self.attributes.skills.save(name, role)
        self.attributes.talents.save(name, role)
        self.attributes.perks.save(name, role)
        self.attributes.complications.save(name, role)

    def _load_fired(self):
        self.info.basic_info_view.load()
        name = self.info.basic_info_view.character_name.get_name()
        role = self.info.basic_info_view.character_name.role
        PERSONALITY.load(role, name)
        self.personality.personality.update_from_model()
        self.stats.load(name, role)
        self.attributes.skills.load(name, role)
        self.attributes.talents.load(name, role)
        self.attributes.perks.load(name, role)
        self.attributes.complications.load(name, role)

    view = View(
        Tabbed(
            Group(
                Item('info', style='custom', show_label=False),
                Item('personality', style='custom', show_label=False),
            ),

            Item('stats', style='custom', show_label=False),
            Item('attributes', style='custom', show_label=False),
            Item('lifepath', style='custom', show_label=False)
        ),
        Item('save', show_label=False),
        Item('load', show_label=False)

    )


if __name__ == '__main__':
    c = CharacterCreatorFull()
    c.configure_traits()
