import re

from fsttrpgtables.models import Table

LIFEPATH_SHORTCUTS_TABLE = Table('lifepath_shortcuts')
TABLE_EVENT_MENU = Table('event_menu')
TABLE_ENEMY_CAUSES = Table('enemy_cause')
TABLE_ENEMY_TYPE = Table('enemy_who')
TABLE_ENEMY_HATE = Table('enemy_hate')
TABLE_ENEMY_DO = Table('enemy_do')
TABLE_ENEMY_RESOURCES = Table('enemy_resources')
TABLE_FRIENDS = Table('friend_relationships')
TABLE_LOVE_TRAGIC = Table('love_tragic')
TABLE_LOVE_MUTUAL_FEELINGS = Table('love_mutual')
TABLE_LOVE_PROBLEMS = Table('love_problems')
TABLE_SIBLING_RELATION = Table('family_sibling_relation')
POWERFUL_CONNECTION_PATTERN = re.compile('1\.1\.1\.\d')

TABLE_CHILDHOOD_ENVIROMENT = Table('childhood_enviroment')
TABLE_CHILDHOOD_EVENT = Table('childhood_event')
TABLE_PARENTS_ARE = Table('family_is')
TABLE_PARENT_RANK = Table('family_rank')
TABLE_PARENT_EVENT = Table('parent_event')
TABLE_PARENT_PROBLEMS = Table('family_problems')
TABLE_FAMILY_STATUS = Table('family_status')
TABLE_FAMILY_TRAGEDY = Table('family_tragedy')
TABLE_FAMILY_CONTACT = Table('family_contact')

PARENT_PROBLEMS_ARRAY = ['none']
FAMILY_TRAGEDY_ARRAY = ['none']

for result in TABLE_PARENT_PROBLEMS.results():
    PARENT_PROBLEMS_ARRAY.append(result)

for result in TABLE_FAMILY_TRAGEDY.results():
    FAMILY_TRAGEDY_ARRAY.append(result)

BETRAYEL_PATTERN_1 = re.compile('1\.2\.4\.1\.\d')

# Big Problems, Big Wins DISASTER STRIKES Betrayal  you were betrayed by a close friend in either romance or
# career (you choose).
BETRAYEL_PATTERN_2 = re.compile('1\.2\.4\.3\.\d')

# Big Problems, Big Wins DISASTER STRIKES Lover, friend or relative killed  They died accidentally.
FRND_KILLED_PATTERN_1 = re.compile('1\.2\.6\.1\.\d')

# Big Problems, Big Wins DISASTER STRIKES Lover, friend or relative killed  They were murdered by unknown
# parties.
FRND_KILLED_PATTERN_2 = re.compile('1\.2\.6\.2\.\d')

# Big Problems, Big Wins DISASTER STRIKES Lover, friend or relative killed  They were murdered and you know who
# did it. You just need the proof.
FRND_KILLED_PATTERN_3 = re.compile('1\.2\.6\.3\.(\d+)')

FRIEND_PATTERN = re.compile('2\.1\.(\d+)')

# 2.2.1.1.1.1.1
# 2.2.10.5.2.3.3
# 2.2.2.10.3.4.5
ENEMY_PATTERN = re.compile('2\.2\.(\d+)\.(\d+)\.\d\.\d\.\d')
PATTERN_ENEMY_FRIEND = re.compile('2\.2\.1\.(\d+)\.\d\.\d\.\d')
PATTERN_ENEMY_EX_LOVER = re.compile('2\.2\.2\.(\d+)\.\d\.\d\.\d')
PATTERN_ENEMY_RELATIVE = re.compile('2\.2\.3\.(\d+)\.\d\.\d\.\d')

# 3.2.1.1
PATTERN_TRAGIC_LOVE = re.compile('3\.2\.\d\.\d')
PATTERN_TRAGIC_LOVE_LOVER_DIED = re.compile('3\.2\.(1|7|8)\.\d')
PATTERN_TRAGIC_LOVE_LOVER_VANISHED = re.compile('3\.2\.2\.\d')

# 3.3.1
PATTERN_LOVE_WITH_PROBLEMS = re.compile('3\.3\.\d')

ROMANCE_COMPLICATED_PATTERN = re.compile('3\.5\.\d')

PATTERN_RANDOM_PATH = re.compile('r:\d:\d+')
MANY_RELATIONS_SEARCH_PATTERN = re.compile('([a-z]+):([a-z]+):?([a-z]+)?:?([a-z]+)?:?([a-z]+)?:?([a-z]+)?')
