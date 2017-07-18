# -*- coding: latin-1 -*-
from __future__ import print_function

import requests

from db import DBManager


def get_aws_table(name):
    print('fetching table: ' + name)
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/tables/get",
                             json={"table": name})
    j = response.json()
    print(j)
    table = j['response']
    return table


def get_all_aws_tablenames():
    print('fetching all tables..')
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/tables/getall")
    j = response.json()
    tables = j['response']
    names_array = []
    for row in tables:
        stringform = str(row['table_name'])
        if stringform in names_array:
            pass
        else:
            names_array.append(stringform)
    names_array.sort()
    return names_array


def save_table_to_db(table):
    db_mgr = DBManager()
    array = []
    for row in table:
        fr = int(row['fr'])
        to = int(row['to'])
        re = row['result']
        if isinstance(re, unicode):
            # re.replace(u"\u2018", "'").replace(u"\u2019", "'")
            re = str(re.encode(encoding='utf-8', errors='replace'))

        print('type of re in db saving is: ' + str(type(re)))
        re = re.lower()
        ide = row['identifier']

        if isinstance(ide, unicode):
            ide = str(ide.encode(encoding='utf-8', errors='replace'))
        leads_to = None
        try:
            leads_to = row['leads_to']
        except KeyError:
            pass
        array.append({'identifier': ide, 'fr': fr, 'to': to, 're': re, 'table': row['table_name'],
                      'leads_to_table': leads_to})

    db_mgr.fuzion_tables.add_many((array))


def export_to_aws(name, identifier, fr, to, re, leads_to):
    url = 'https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/tables/add'
    re = str.lower(re)
    print('exporting table: ' + str(name) + ' option: ' + str(identifier))
    if leads_to == "":
        leads_to = None
    response = requests.post(url=url, json={'name': name,
                                            'id': identifier,
                                            'fr': fr,
                                            'to': to,
                                            're': re,
                                            'leads_to': leads_to})
    try:
        response_json = response.json()
        load = response_json['response']
        error = load['error']
        if error is not None:
            print('error')
    except ValueError as e:
        print(str(e))
