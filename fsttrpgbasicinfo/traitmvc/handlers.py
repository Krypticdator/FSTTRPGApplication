from traitsui.api import Handler, Action

from fsttrpgbasicinfo.utilities import upload_character_to_aws


class BasicInfoHandler(Handler):
    def do_upload(self, UIInfo):
        upload_character_to_aws(name=self.basic_info.character_name.name.name,
                                role=self.basic_info.character_name.role,
                                gender=self.basic_info.gender,
                                country=self.basic_info.country, birthday=self.basic_info.birthday,
                                age=self.basic_info.age, alias=self.basic_info.alias)

    def do_save(self, UIInfo):
        UIInfo.object.basic_info.save()

    def do_load(self, UIInfo):
        UIInfo.object.basic_info.load()

    def do_random_alias(self, UIInfo):
        # UIInfo.object.basic_info._random_alias_fired()
        UIInfo.object.basic_info.random_alias()

    def do_random_name(self, UIInfo):
        # UIInfo.object.basic_info._random_name_fired()
        UIInfo.object.basic_info.random_name()

    def do_random_age(self, UIInfo):
        # UIInfo.object.basic_info._random_age_fired()
        UIInfo.object.basic_info.random_age()

    def do_random_birthday(self, UIInfo):
        # UIInfo.object.basic_info._random_birthday_fired()
        UIInfo.object.basic_info.random_dob()

    def do_random_all(self, UIInfo):
        # UIInfo.object.basic_info._random_all_fired()
        UIInfo.object.basic_info.random_all()


action_upload = Action(name="Upload", action="do_upload")
action_save = Action(name="Save", action='do_save')
action_load = Action(name="Load", action='do_load')
action_random_name = Action(name="Random name", action="do_random_name")
action_random_alias = Action(name="Random alias", action="do_random_alias")
action_random_age = Action(name="Random age", action="do_random_age")
action_random_birthday = Action(name="Random birthday", action="do_random_birthday")
action_random_all = Action(name="Random all", action="do_random_all")
