import unittest

from application.tables.models import Table


class testTableModel(unittest.TestCase):
    def test_constructor_without_load(self):
        t = Table('test', load_from_name=False)
        self.assertEqual(t.max, 0)

    def test_constructor(self):
        t = Table('test')
        print(t)
        self.assertEqual(t.max, 3)

    def test_table_adding_options(self):
        t = Table('test', load_from_name=False)
        t.add_option(1, 2, 'result1', leads_to=None, identifier='first0')
        t.add_option(3, 3, 'result2', leads_to=None, identifier='first1')

        self.assertEqual(t.get_result(index=1), 'result1')
        self.assertEqual(t.get_result(index=2), 'result1')
        self.assertEqual(t.get_result(index=3), 'result2')

    def test_table_random_result(self):
        t = Table('test', load_from_name=False)
        t.add_option(1, 1, 'result', leads_to=None, identifier='first')
        result = t.random_result()
        self.assertEqual(result, 'result')

    def test_chaining_tables(self):
        t1 = Table('test', load_from_name=True)
        chain = t1.get_result_chain_string(1, 1, 1)
        self.assertEqual(str(chain), 'test:test01|test02:test0201')

    def test_chaining_decoding(self):
        t1 = Table('test')
        chain = t1.get_result_chain_string(1, 1)
        decoded = t1.decode_table_chain_string(chain)
        print(decoded)
        self.assertTrue(True)

    def test_random_option(self):
        t1 = Table('test')
        random_chain, array = t1.get_random_chain_string(first_index=1)
        print(array)
        self.assertTrue(True)

    def test_result_string_chain(self):
        t1 = Table('test')
