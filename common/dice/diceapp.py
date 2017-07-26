from traits.api import HasTraits, Int, Button, String
from traitsui.api import View, Item

from application.common.dice.models import RandomDice


class DiceRoller(HasTraits):
    how_many_times = Int(default_value=1)
    amount = Int(default_value=1)
    dice = Int(default_value=10)
    roll = Button()
    result = String()
    total = Int()

    def _roll_fired(self):
        d = RandomDice(dices=self.amount, sides=self.dice)
        r = []
        for i in range(0, self.how_many_times):
            r.append(d.roll())

        self.result = str(r)
        # self.total = sum(r)

    view = View(
        Item('how_many_times'),
        Item('amount'),
        Item('dice'),
        Item('roll'),
        Item('result'),
        # Item('total')
    )


class InfiniteDiceRoller(DiceRoller):
    end_daemon = Button()
    configure_daemon = Button()

    def __init__(self):
        super(InfiniteDiceRoller, self).__init__()
        self.daemon = RandomDice(self.amount, self.dice, max_life=-1)

    def _end_daemon_fired(self):
        self.daemon.r_dice.daemon.end()

    def _configure_daemon_fired(self):
        self.daemon.r_dice.daemon.end()
        self.daemon = RandomDice(self.amount, self.dice, max_life=-1)

    def _roll_fired(self):
        r = []
        for i in range(0, 1):
            r.append(self.daemon.roll())

        self.result = str(r)

    view = View(
        Item('configure_daemon'),
        Item('amount'),
        Item('dice'),
        Item('roll'),
        Item('result'),
        Item('end_daemon', show_label=False)
    )




if __name__ == '__main__':
    dr = InfiniteDiceRoller()
    dr.configure_traits()
