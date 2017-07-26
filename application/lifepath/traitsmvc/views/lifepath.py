from traits.api import Instance, List
from traitsui.api import View, Tabbed, Group, HGroup, Item, ListEditor

from application.lifepath.traitsmvc.models.lifepath import Event, Lifepath
from application.lifepath.traitsmvc.views.eventpersons import EventPersonView, TwoEventPersonsView


class EventView(Event):
    person = Instance(EventPersonView)
    two_event_persons = Instance(TwoEventPersonsView)
    view = View(
        Tabbed(
            Group(
                HGroup(
                    Item('random_event', show_label=False),
                    Item('path', width=15),
                ),
                HGroup(
                    Item('age', width=2),
                    Item('desc', width=600, show_label=False),
                ),
                label='Event'),
            HGroup(
                Item('person', show_label=False),
                Item('two_event_persons', show_label=False),
                label='People involved')

        )
    )


class LifepathView(Lifepath):
    events = List(Instance(EventView()))

    # TODO - Delete this hack
    def generate_random_lifepath(self, starting_year, actor_age):
        self.events = []
        for i in range(starting_year, actor_age):
            e = EventView(age=i, life_path_method=self.event_change_listener)
            e.random_life_event()
            self.events.append(e)

    view = View(
        Tabbed(
            Item('events', show_label=False, editor=ListEditor(style='custom')),
            Group(
                Item('starting_age'),
                Item('to_age'),
                Item('gender'),
                Item('sexual_orientation'),
                Item('random_lifepath'),
                Item('save_lifepath'),
                label='Settings')

        )

    )
