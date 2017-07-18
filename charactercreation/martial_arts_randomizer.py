from fsttrpgtables.models import Table

martial_arts_table = Table('martial_arts', load_from_name=False)

martial_arts_table.add_option(fr=1, to=1, re='karate', leads_to=None, identifier='01')
martial_arts_table.add_option(fr=2, to=2, re='boxing', leads_to=None, identifier='judo02')
martial_arts_table.add_option(fr=3, to=3, re='thai boxing', leads_to=None, identifier='judo03')
martial_arts_table.add_option(fr=4, to=4, re='chol li fut', leads_to=None, identifier='judo04')
martial_arts_table.add_option(fr=5, to=5, re='aikido', leads_to=None, identifier='judo05')
martial_arts_table.add_option(fr=6, to=6, re='animal kunfu', leads_to=None, identifier='judo06')
martial_arts_table.add_option(fr=7, to=7, re='tae kwon do', leads_to=None, identifier='judo07')
martial_arts_table.add_option(fr=8, to=8, re='savate', leads_to=None, identifier='judo08')
martial_arts_table.add_option(fr=9, to=9, re='wrestling', leads_to=None, identifier='judo09')
martial_arts_table.add_option(fr=10, to=10, re='capoera', leads_to=None, identifier='judo10')

x = 'y'
while x != 'x':
    x = input()
    print(martial_arts_table.random_result())

'''Style and  Difficulty Lvl.
Karate (2) Judo (1)
Boxing  (1)
Thai Boxing  (4)
Chol Ll Fut (3) Aikido (3)
Animal  Kung Fu (3) Tae Kwon Do (4)
Savate (2) Wrestling ( 1)
Capeolra  (3)'''
