import utilities
from application.tables.models import Table
from database import DBManager


class TableValue(object):
    def __init__(self, source_table_name, random_method='single', random_min=1, random_max=1):
        super(TableValue, self).__init__()

        self.source_table = Table(source_table_name)
        if random_method == 'single':
            self.value = self.source_table.results()[0]
        else:
            self.value = None
        print(self.value)
        self.random_method = random_method
        self.random_min = random_min
        self.random_max = random_max

    def get_random(self, return_as_option=False):
        if self.random_method is 'multiple':
            self.value = self.source_table.multiple_randoms(min=self.random_min, max=self.random_max)
        else:
            if return_as_option:
                self.value = self.source_table.random_option()
            else:
                self.value = self.source_table.random_result()
        return self.value


class Personality(object):
    def __init__(self):
        super(Personality, self).__init__()
        self.prime_motivation = TableValue(source_table_name='prime_motivations')
        self.most_valued_person = TableValue(source_table_name='valued_person')
        self.most_valued_posession = TableValue(source_table_name='valued_posession')
        self.how_feels_about_most_people = TableValue(source_table_name='valued_people')
        self.inmode = TableValue(source_table_name='inmodes')
        self.exmode = TableValue(source_table_name='exmodes')
        self.quirks = TableValue(source_table_name='quirks', random_method='multiple', random_min=1, random_max=3)
        self.disorders = TableValue(source_table_name='disorders', random_method='multiple')
        self.disorders.value = ['None']
        self.phobias = TableValue(source_table_name='phobias', random_method='multiple')
        self.hairstyle = TableValue(source_table_name='hair', random_method='multiple')
        self.clothes = TableValue(source_table_name='clothes', random_method='multiple')
        self.affections = TableValue(source_table_name='affections', random_method='multiple')
        self.all_fields_array = [self.prime_motivation, self.most_valued_person, self.most_valued_posession,
                                 self.how_feels_about_most_people, self.inmode, self.exmode, self.quirks,
                                 self.phobias, self.hairstyle, self.clothes, self.affections]

    def assign_random_to_field(self, field_name):
        try:
            field = self.__getattribute__(field_name)
            return field.get_random()
        except KeyError:
            print('no such field')

    def random_all(self):
        for field in self.all_fields_array:
            field.get_random()

    def save(self, role, actor_name, upload_to_aws=False):
        # print('Personality model class save')
        pm = self.prime_motivation.value
        mvper = self.most_valued_person.value
        mvpos = self.most_valued_posession.value
        fap = self.how_feels_about_most_people.value
        inm = self.inmode.value
        exm = self.exmode.value
        qui = self.quirks.value
        pho = self.phobias.value
        dis = self.disorders.value
        hai = self.hairstyle.value
        clo = self.clothes.value
        aff = self.affections.value

        arr = [pm, mvper, mvpos, fap, inm, exm, qui, pho, dis, hai, clo, aff]

        for cell in arr:
            if cell is None:
                return "one of the personality fields was empty, save failed"

        db_mgr = DBManager()
        db_mgr.personalities_table.add(actor_role=role, actor_name=actor_name, prime_motivation=pm,
                                       most_valued_person=mvper, most_valued_pos=mvpos, feels_about_people=fap,
                                       inmode=inm, exmode=exm, quirks=qui, phobias=pho, disorders=dis, hairs=hai,
                                       clothing=clo, affections=aff)

        if upload_to_aws:
            utilities.save_character_info(role=role, name=actor_name, prime_motivation=pm, m_valued_person=mvper,
                                          m_valued_posession=mvpos, feels_about_people=fap, inmode=inm, exmode=exm,
                                          quirks=qui, phobias=pho, disorders=dis, hair=hai, clothes=clo, affections=aff)
        return 'save successful'

    def load(self, role, name):
        db_mgr = DBManager()
        query = db_mgr.personalities_table.get_personality_of(actor_role=role, actor_name=name)
        traits = query['traits']
        per = query['personality']
        self.prime_motivation.value = per.prime_motivation
        self.most_valued_person.value = per.most_valued_person
        self.most_valued_posession.value = per.most_valued_posession
        self.how_feels_about_most_people.value = per.feels_about_people
        self.inmode.value = per.inmode
        self.exmode.value = per.exmode

        quirks = []
        phobias = []
        disorders = []
        hairs = []
        clothes = []
        affections = []
        for trait in traits:
            if trait.trait_type == 'quirk':
                quirks.append(trait.trait_name)
            elif trait.trait_type == 'phobia':
                phobias.append(trait.trait_name)
            elif trait.trait_type == 'disorder':
                disorders.append(trait.trait_name)
            elif trait.trait_type == 'hair':
                hairs.append(trait.trait_name)
            elif trait.trait_type == 'clothes':
                clothes.append(trait.trait_name)
            elif trait.trait_type == 'affection':
                affections.append(trait.trait_name)
        self.quirks.value = quirks
        self.phobias.value = phobias
        self.disorders.value = disorders
        self.hairstyle.value = hairs
        self.clothes.value = clothes
        self.affections.value = affections


if __name__ == '__main__':
    p = Personality()
    p.assign_random_to_field('prime_motivation')
    print(p.prime_motivation.value)
