import os
import unittest

from fsttrpgpersonality.traitsmodels import PersonalityRandomizer, Personality, personality

'''class TestCheckListEditorClasses(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove('fuziontables.db')
        except WindowsError as e:
            print('failed to delete: ' + str(e))

    def test_initialization(self):
        d = Disorders()
        p = Phobias()
        q = Quirks()
        c = Clothes()
        h = Hair()
        a = Affections()
        self.assertTrue(True)'''


class TestPersonalityTraitModel(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove('fuziontables.db')
        except WindowsError as e:
            print('failed to delete: ' + str(e))

    def test_initialization(self):
        p = Personality()
        self.assertTrue(True)

    def test_saving(self):
        pr = PersonalityRandomizer()
        pr._random_all_fired()
        pr.personality.prime_motivation = 'Love'
        message = personality.save('NPC', 'testactor')
        print(message)
        personality.load('NPC', 'testactor')
        self.assertEqual(personality.prime_motivation.value, 'Love')
