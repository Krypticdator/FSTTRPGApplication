import requests


def get_aws_character_list(group):
    print('fetching group: ' + group)
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/characters/get/list",
                             json={"role": group})
    try:
        j = response.json()

        names = j['response']
        return names
    except Exception as e:
        print('converting response to json failed')
        print(str(e))
        return None
