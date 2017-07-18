from __future__ import print_function

from random import randint

import requests


def upload_to_aws(role, name, packed_stats):
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/characters/modify/all",
                             json={"stats": packed_stats,
                                   "name": name,
                                   "role": role,
                                   "target": "primary_stats"})
    j = response.json()
    message = j['response']
    print(message)


def randomize(max_points=-1, min_points=-1, limit_tens=-1, limit_ones=0):
    array = []

    for i in range(0, 10):
        array.append(randint(1, 10))
    print(array)
    if limit_tens > -1 and limit_ones > -1:
        while array.count(10) > limit_tens or array.count(1) > limit_ones:
            ten_count = array.count(10)
            one_count = array.count(1)
            index_to_rethrow = -1
            if ten_count > limit_tens:
                index_to_rethrow = array.index(10)
            elif one_count > limit_ones:
                index_to_rethrow = array.index(1)
            if index_to_rethrow != -1:
                print('rethrowing value: ' + str(array[index_to_rethrow]))
                array[index_to_rethrow] = randint(1, 10)

    elif limit_tens > -1 and limit_ones == -1:
        while array.count(10) > limit_tens:
            ten_index = array.index((10))
            array[ten_index] = randint(1, 10)
    else:
        while array.count(1) > limit_ones:
            one_index = array.index((1))
            array[one_index] = randint(1, 10)

    if max_points > -1:
        trim_count = 0
        while sum(array) > max_points:
            highest = max(array)
            index_of_max = array.index(highest)
            array[index_of_max] -= 1
            trim_count += 1
        print('trimmed ' + str(trim_count) + ' points')

    if min_points > -1:
        trim_count = 0
        while sum(array) < min_points:
            lowest = min(array)
            index_of_min = array.index(lowest)
            array[index_of_min] += 1
            trim_count += 1
        print('added ' + str(trim_count) + ' points')

    print(array)

    return array
