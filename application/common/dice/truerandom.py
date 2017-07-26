import Queue
from threading import Thread

from rdoclient import RandomOrgClient
from time import sleep


class DiceInputDaemon(Thread):
    def run(self):
        life_counter = 0
        while not self.wants_abort:
            sleep(self.update_frequency)
            if self.queue.qsize() < self.buffer_size:
                # print('adding more results')
                r = RandomOrgClient('aeaaf602-ba2e-4004-a6de-160dddf44059', blocking_timeout=2.0, http_timeout=10.0)
                bits_left = r.get_bits_left()
                reqs_left = r.get_requests_left()
                if bits_left > 300 and reqs_left > 5:
                    # print('got more numbers!')
                    result = r.generate_integers(self.batch_size, self.min, self.max)
                    for d in result:
                        self.queue.put(d)
                else:
                    self.wants_abort = True
                    self.no_more_requests = True

            else:
                pass
            if self.max_life != -1:
                life_counter += 1
                if life_counter > self.max_life:
                    self.wants_abort = True
        print('stopped')

    def configure(self, min, max, queue, buffer_size=30, batch_size=60, update_frequency=.5, max_life=-1):
        self.queue = queue
        self.wants_abort = False
        self.no_more_requests = False
        self.min = min
        self.max = max
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.update_frequency = update_frequency
        self.max_life = max_life

    def end(self):
        self.wants_abort = True


class Dice(object):
    def __init__(self, dices, sides, daemon_buffer_size=20, daemon_batch_size=30, daemon_update_frequency=.5,
                 daemon_max_life=-1):
        super(Dice, self).__init__()
        self.dice_queue = Queue.Queue()
        self.daemon = DiceInputDaemon()
        # self.backup_daemon = DiceInputDaemon()
        self.daemon.configure(1, sides, self.dice_queue, daemon_buffer_size, daemon_batch_size, daemon_update_frequency,
                              daemon_max_life)
        # self.backup_daemon.configure(1, sides, self.dice_queue, daemon_buffer_size*2, daemon_batch_size,
        #                              daemon_update_frequency, .1)
        self.daemon.start()
        # self.backup_daemon.start()
        self.dices = dices

    def roll(self):
        results = []
        for i in range(0, self.dices):
            results.append(self.dice_queue.get())
            self.dice_queue.task_done()
        return results


class ThreeDeeSix(Dice):
    def __init__(self, daemon_max_life=300):
        super(ThreeDeeSix, self).__init__(3, 6, daemon_max_life=daemon_max_life)
