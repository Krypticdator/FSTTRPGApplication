import os
import unittest

import fsttrpgbasicinfo.utilities
from fsttrpgbasicinfo.databases import DBManager
from fsttrpgbasicinfo.models import Names, BasicInfo as ModelBasicInfo
from fsttrpgbasicinfo.traitmvc.models import BasicInfo


class TestModel(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove('names.db')
            os.remove('actors.db')
        except Exception as e:
            print('failed to delete: ' + str(e))

    def test_load_names_aws_true_no_doubles(self):
        '''Names table should not store double values of same name'''
        names = Names('test', True)
        names.load_names('test', True)
        len_of_test_country = len(names.female_names) + len(names.male_names) + len(names.last_names)
        self.assertEqual(len_of_test_country, 3)
        db = DBManager()
        db.names_table.delete_country('test')

    def test_random_name(self):
        names = Names('test', True)
        random = names.random_name('male')
        self.assertEqual(random, 'test01 test03')

    def test_save_and_load(self):
        bi = ModelBasicInfo(name='Toni Nurmi', gender='male', dob='11.1', age=27, country='us', alias='mad doc')
        bi.save('Toni Nurmi', role='pc')
        bi.load('Toni Nurmi', role='pc')
        self.assertEqual(bi.name, 'Toni Nurmi')
        self.assertEqual(bi.gender, 'male')
        self.assertEqual(bi.dob, '11.1')
        self.assertEqual(bi.age, 27)
        self.assertEqual(bi.alias, 'mad doc')


class TestUtilities(unittest.TestCase):
    def tearDown(self):
        try:
            os.remove('names.db')
            os.remove('actors.db')
        except Exception as e:
            print('failed to delete: ' + str(e))

    def test_upload(self):
        response = fsttrpgbasicinfo.utilities.upload_character_to_aws(name='test', role='test', gender='male',
                                                                      country='us',
                                                                      birthday='11.1', age=18, alias="test")
        self.assertEqual(response['response'], 'success')

    def test_get_aws_names(self):
        response = fsttrpgbasicinfo.utilities.get_aws_names_group('test')
        self.assertEqual(len(response), 3)


class TestTraits(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove('names.db')
            os.remove('actors.db')
        except Exception as e:
            print('failed to delete: ' + str(e))

    def test_basic_info(self):
        basic = BasicInfo()
        self.assertTrue(True)

    def test_basic_info_save(self):
        basic = BasicInfo()
        basic.save()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
