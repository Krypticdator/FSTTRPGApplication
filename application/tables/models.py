from __future__ import print_function

from random import randint

import utilities
from db import DBManager


class TableOption(object):
    def __init__(self, fr, to, re, identifier, leads_to):
        self.fr = fr
        self.to = to
        self.re = re
        self.leads_to = leads_to
        self.identifier = identifier


class Table(object):
    def __init__(self, name, load_from_name=True):
        super(Table, self).__init__()
        self.name = name
        self.options = {}
        self.max = 0

        if load_from_name:
            self.load(name)
        self.calc_max()

    def load(self, name):
        db_mgr = DBManager()
        table = None
        if db_mgr.fuzion_tables.count_options(name) > 0:
            table = db_mgr.fuzion_tables.get_table(name)
        else:
            table = utilities.get_aws_table(name)
            utilities.save_table_to_db(table)
            table = db_mgr.fuzion_tables.get_table(name)
        if table is not None:
            for row in table:
                self.add_option(row.fr, row.to, row.re, leads_to=row.leads_to_table, identifier=row.identifier)

    def add_option(self, fr, to, re, leads_to=None, identifier=None):
        table_option = TableOption(fr=fr, to=to, re=re, leads_to=leads_to, identifier=identifier)
        if fr != to:
            for i in range(fr, to + 1):
                self.options[i] = table_option
        else:
            self.options[fr] = table_option
        self.calc_max()

    def extract_option_from_json(self, option):
        fr = int(option['fr'])
        to = int(option['to'])
        re = str(option['result'])
        self.add_option(fr, to, re)

    def results(self):
        results = []
        for key, value in self.options.iteritems():
            if value.re in results:
                pass
            else:
                results.append(value.re)
        results.sort()
        return results

    def random_result(self):
        r = randint(1, self.max)
        option = self.options[r].re

        return option

    def random_option(self):
        r = randint(1, self.max)
        option = self.options[r]
        return (option, r)

    def get_result_chain_string(self, starting_index, *args):
        option = self.options[starting_index]
        chain_str = self.name + ":" + option.identifier
        leads_to = option.leads_to
        for arg in args:
            if leads_to is None:
                break
            table = Table(leads_to)
            try:
                option = table.get_option(index=arg)
                leads_to = option.leads_to
                chain_str = chain_str + "|" + table.name + ":" + option.identifier
            except KeyError as e:
                print(str(e))
                break

        return chain_str

    def get_random_chain_string(self, first_index):
        number_array = []
        number_array.append(first_index)
        option = self.options[first_index]
        chain_str = self.name + ":" + option.identifier
        leads_to = option.leads_to
        while leads_to is not None:
            table = Table(leads_to)
            option, r = table.random_option()
            number_array.append(r)
            leads_to = option.leads_to
            chain_str = chain_str + "|" + table.name + ":" + option.identifier
        return (chain_str, number_array)

    def decode_table_chain_string(self, chain):
        chain = str(chain)
        split_by_table = chain.split('|')
        decoded = []
        num_array = []
        for pair in split_by_table:
            values = pair.split(':')
            t_name = values[0]
            identifier = values[1]
            table = Table(t_name)
            option = table.get_option(identifier=identifier)
            num_array.append(option.fr)
            pack = {'table': t_name, 'option': option}
            decoded.append(pack)
        return (decoded, num_array)

    def decode_chain_string_to_results_string(self, chain):
        decoded_chain, array = self.decode_table_chain_string(chain)
        array_of_results = []
        for table in decoded_chain:
            option = table['option']
            array_of_results.append(option.re + " ")

        string_of_results = ''.join(array_of_results)
        return string_of_results

    def multiple_randoms(self, min, max):
        times = randint(min, max)
        # print('times: ' + str(times))
        results = []
        while len(results) < times:
            r = self.random_result()
            if r in results:
                pass
            else:
                results.append(r)
        return results

    def get_result(self, index):
        return self.options[index].re

    def get_option(self, index=None, identifier=None):
        if identifier:
            for key, value in self.options.iteritems():
                if value.identifier == identifier:
                    return value
        elif index:
            return self.options[index]

    def calc_max(self):
        m = self.max
        for key, value in self.options.iteritems():
            if key > m:
                m = key
        self.max = m

    def __repr__(self):
        printable = ""
        for key, value in self.options.iteritems():
            printable = printable + str(value.fr) + "-" + str(value.to) + " re: " + str(value.re) + "\n"
        return printable


if __name__ == '__main__':
    pass
