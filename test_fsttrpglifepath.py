import unittest

from application.lifepath.models import event_menu


class testLifePath(unittest.TestCase):
    def test_luck_paths(self):
        e01 = event_menu.get_result_chain_string(1, 1, 1, 1)
        e02 = event_menu.get_result_chain_string(1, 1, 1, 2)
        e03 = event_menu.get_result_chain_string(1, 1, 1, 3)

        e04 = event_menu.get_result_chain_string(1, 1, 2, )
        e05 = event_menu.get_result_chain_string(1, 1, 3, )
        e06 = event_menu.get_result_chain_string(1, 1, 4, )
        e07 = event_menu.get_result_chain_string(1, 1, 5, )
        e08 = event_menu.get_result_chain_string(1, 1, 6, )
        e09 = event_menu.get_result_chain_string(1, 1, 7, )
        e10 = event_menu.get_result_chain_string(1, 1, 8, )
        e11 = event_menu.get_result_chain_string(1, 1, 9, )
        e12 = event_menu.get_result_chain_string(1, 1, 10, )

        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table0'
                         '|powerful_connection:powerful_connection0', e01)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table0'
                         '|powerful_connection:powerful_connection1', e02)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table0'
                         '|powerful_connection:powerful_connection2', e03)

        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table1', e04)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table2', e05)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table3', e06)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table4', e07)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table5', e08)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table6', e09)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table7', e10)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table8', e11)
        self.assertEqual('event_menu:event_menu0|4A:4A0|lucky_table:lucky_table9', e12)

    def test_disaster_paths(self):
        e01 = event_menu.get_result_chain_string(1, 2, 1, 1, 1)
        e02 = event_menu.get_result_chain_string(1, 2, 2, 1, 1)
        e03 = event_menu.get_result_chain_string(1, 2, 3, 1, 1, )
        e04 = event_menu.get_result_chain_string(1, 2, 4, 1, 1)
        e05 = event_menu.get_result_chain_string(1, 2, 5, 1, 1)

        print(e01)
