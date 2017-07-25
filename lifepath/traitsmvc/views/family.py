from traits.api import Instance, List
from traitsui.api import View, HGroup, Group, VGroup, Item, ListEditor, Tabbed

from application.lifepath.traitsmvc.models.family import Family, FamilyBackground, FamilyBackgroundWithControls
from application.lifepath.traitsmvc.views.eventpersons import EventPersonView, SiblingView


class FamilyView(Family):
    father = Instance(EventPersonView, ())
    mother = Instance(EventPersonView, ())
    siblings = List(Instance(SiblingView, ()))
    view = View(
        HGroup(
            Item('father', style='custom'),
            Item('mother', style='custom')
        ),
        Item('siblings', editor=ListEditor(style='custom'))
    )


class FamilyBackgroundView(FamilyBackground):
    family = Instance(FamilyView, ())
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


class FamilyBackgroundWithControlsView(FamilyBackgroundWithControls):
    family_background = Instance(FamilyBackgroundView, ())
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
