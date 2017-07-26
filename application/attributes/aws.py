import requests


def import_attributes_of_type(attribute_type):
    print('retrieving blueprints for ' + attribute_type)
    url = 'https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/skillblueprints/get'
    response = requests.post(url=url, json={'type': attribute_type})
    j = response.json()
    attributes = j['response']
    return attributes
