from traits.api import Instance, List
from traitsui.api import View, HGroup, VGroup, Item

from application.lifepath.traitsmvc.models.eventpersons import Relationships, EventPerson, Enemy, TragicLove, Sibling, \
    TwoEventPersons


class RelationshipView(Relationships):
    view = View(
        HGroup(
            Item('relationship', show_label=False),
            Item('detail', style='readonly')
        )

    )


class EventPersonView(EventPerson):
    current_relationship = Instance(RelationshipView, ())
    past_relationships = List(Instance(RelationshipView, ()))
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


class EnemyView(Enemy):
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


class TragicLoveView(TragicLove):
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


class SiblingView(Sibling):
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


class TwoEventPersonsView(TwoEventPersons):
    person1 = Instance(EventPersonView, ())
    person2 = Instance(EventPersonView, ())
    view = View(
        HGroup(
            Item('person1', style='custom'),
            Item('person2', style='custom')
        )

    )
