from random import randrange

from truerandom import Dice as TrueRandomDice


class StaticDice(object):
    def __init__(self):
        super(StaticDice, self).__init__()

    @staticmethod
    def roll(num, sides):
        r = sum(randrange(sides) + 1 for die in range(num))
        return r


class BasicDice(object):
    def __init__(self, dices, sides):
        super(BasicDice, self).__init__()
        self.dices = dices
        self.sides = sides

    def roll(self, return_sum_only=False):
        results = []
        for i in range(0, self.dices):
            r = randrange(self.sides) + 1
            results.append(r)
        if return_sum_only:
            return sum(results)
        else:
            return results


class RandomDice(object):
    def __init__(self, dices, sides, buffer_size=20, batch_size=30, update_frequency=.5, max_life=20):
        super(RandomDice, self).__init__()
        self.r_dice = TrueRandomDice(dices=dices, sides=sides, daemon_buffer_size=buffer_size,
                                     daemon_batch_size=batch_size, daemon_update_frequency=update_frequency,
                                     daemon_max_life=max_life)
        self.n_dice = BasicDice(dices, sides)

    def roll(self):
        if self.r_dice.daemon.no_more_requests:
            print('out of truly randoms')
            return self.n_dice.roll()
        else:
            return self.r_dice.roll()


if __name__ == '__main__':
    d = RandomDice(1, 6)
    re = []
    for i in range(0, 1):
        r = d.roll()
        re.append(r)
    print(re)
