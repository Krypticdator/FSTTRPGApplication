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


if __name__ == '__main__':
    dr = DiceRoller()
    dr.configure_traits()
