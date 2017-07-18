import requests


def save_character_info(role, name, prime_motivation, m_valued_person, m_valued_posession, feels_about_people, inmode,
                        exmode, quirks, phobias, disorders, hair, clothes, affections):
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/characters/modify/all",
                             json={"role": role,
                                   "target": "personality",
                                   "name": name,
                                   "motivation": prime_motivation,
                                   "valued_person": m_valued_person,
                                   "valued_posession": m_valued_posession,
                                   "feels_about_people": feels_about_people,
                                   "inmode": inmode,
                                   "exmode": exmode,
                                   "quirks": quirks,
                                   "phobias": phobias,
                                   "disorders": disorders,
                                   "hair": hair,
                                   "clothes": clothes,
                                   "affections": affections})

    j = response.json()
    message = j['response']
    print(message)
