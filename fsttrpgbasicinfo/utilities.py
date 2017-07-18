from __future__ import print_function

from random import randint

import requests


def get_aws_names_group(country):
    print('fetching country: ' + country)
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/names/get/group",
                             json={"country": country})
    j = response.json()

    names = j['response']
    return names


def upload_character_to_aws(name, role, gender, country, birthday, age, alias=None):
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/characters/create",
                             json={"name": str(name),
                                   "role": str(role),
                                   "gender": str(gender),
                                   "country": str(country),
                                   "birthday": str(birthday),
                                   "age": str(age),
                                   "alias": str(alias)})
    print('upload complete')
    return response.json()


def random_birthday():
    month = randint(1, 12)
    day = 0
    if month == 2:
        day = randint(1, 28)
    else:
        day = randint(1, 30)
    birthday = str(day) + "." + str(month)
    return birthday


def max_sql_variables():
    """Get the maximum number of arguments allowed in a query by the current
    sqlite3 implementation. Based on `this question
    `_

    Returns
    -------
    int
        inferred SQLITE_MAX_VARIABLE_NUMBER
    """
    import sqlite3
    db = sqlite3.connect(':memory:')
    cur = db.cursor()
    cur.execute('CREATE TABLE t (test)')
    low, high = 0, 100000
    while (high - 1) > low:
        guess = (high + low) // 2
        query = 'INSERT INTO t VALUES ' + ','.join(['(?)' for _ in
                                                    range(guess)])
        args = [str(i) for i in range(guess)]
        try:
            cur.execute(query, args)
        except sqlite3.OperationalError as e:
            if "too many SQL variables" in str(e):
                high = guess
            else:
                raise
        else:
            low = guess
    cur.close()
    db.close()
    return low
