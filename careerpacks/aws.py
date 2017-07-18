import requests


def upload_pack_member(pack_name, attr_name, attr_type):
    url = 'https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/careers/add'
    print('sending career: ' + pack_name + ": " + attr_name)
    response = requests.post(url=url, json={'career': pack_name,
                                            'attribute_name': attr_name,
                                            'attribute_type': attr_type})
    j = response.json()
    print(str(j))
