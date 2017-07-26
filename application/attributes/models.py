from databases import DBManager


class AttributeLists(object):
    def __init__(self, attribute_type):
        super(AttributeLists, self).__init__()
        db = DBManager()
        self.all_attribute_names = ['none']
        self.descriptions = {}
        self.costs = {}
        for skill in db.attribute_blueprints.get_all_of_type(attribute_type):
            self.all_attribute_names.append(str(skill.name))
            self.descriptions[skill.name] = skill.desc
            self.costs[skill.name] = skill.cost


class Attribute(object):
    def __init__(self, attr_type, name, lvl=0, field=""):
        super(Attribute, self).__init__()
        self.attr_type = attr_type
        self.name = name
        self.lvl = lvl
        self.field = field

    def __eq__(self, other):
        # print('comparing: ' + self.name + ' to: ' + other.name)
        if other is None:
            # print('other is none, returning false')
            return False
        elif self.name != other.name:
            # print('names are not the same, returning false')
            return False
        elif self.attr_type != other.attr_type:
            # print('types are not the same, returning false')
            return False
        elif self.field != other.field:
            print('fields are not the same, returning false')
            return False
        else:
            # print('same, returning true')
            return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if self.field != "":
            return self.attr_type + ": " + self.name + "(" + self.field + ")"
        return self.attr_type + ": " + self.name


class Complication(Attribute):
    def __init__(self, name, frequency=0, intensity=0, importance=0, field=""):
        super(Complication, self).__init__(attr_type='complication', name=name, field=field)
        self.frequency = frequency
        self.intensity = intensity
        self.importance = importance

    def __eq__(self, other):
        if other is None:
            return False
        elif other.name != self.name:
            return False
        elif other.attr_type != self.attr_type:
            return False
        elif other.field != self.field:
            return False
        else:
            return True


class Perk(Attribute):
    def __init__(self, name, lvl, field, target_person_name):
        super(Perk, self).__init__(attr_type='perk', name=name, lvl=lvl, field=field)
        self.target_person_name = target_person_name

    def __eq__(self, other):
        if other is None:
            return False
        elif other.name != self.name:
            return False
        elif other.attr_type != self.attr_type:
            return False
        elif other.target_person_name != self.target_person_name:
            return False
        elif other.field != self.field:
            return False
        else:
            return True


class AttributeManager(object):
    def __init__(self):
        super(AttributeManager, self).__init__()
        self.attributes = []

    def add_attribute(self, attr_type, attr_name, lvl=0, field=""):
        self.attributes.append(Attribute(attr_type, attr_name, lvl, field))
        print(self.attributes)

    def get_attribute(self, attr_type, attr_name, field, use_field_in_search=True):
        for i in range(0, len(self.attributes)):
            a = self.attributes[i]
            if a.name == attr_name and a.attr_type == attr_type:
                if use_field_in_search:
                    if a.field == field:
                        return a
                else:
                    return a

    def already_exists(self, attr_type, attr_name, field):
        attr = Attribute(attr_type=attr_type, name=attr_name, field=field)
        if attr in self.attributes:
            return True
        else:
            return False

    def modify_lvl(self, attr_type, attr_name, field, lvl):
        a = self.get_attribute(attr_type, attr_name, field)
        if a:
            a.lvl = lvl

    def modify_field(self, attr_type, attr_name, field):
        a = self.get_attribute(attr_type, attr_name, field, use_field_in_search=False)
        if a:
            a.field = field
        else:
            print('didnt find attribute for field modification')

    def add_if_new(self, attr_type, attr_name, lvl, field):
        if self.already_exists(attr_type, attr_name, field):
            pass
        else:
            self.add_attribute(attr_type, attr_name, lvl, field)

    def remove(self, attr_type, attr_name):
        index_to_remove = None
        for i in range(0, len(self.attributes)):
            attr = self.attributes[i]

            if attr_name == attr.name and attr.attr_type == attr_type:
                index_to_remove = i
                break
        if index_to_remove is not None:
            del self.attributes[index_to_remove]

    def get_names_array(self):
        array = []
        for attr in self.attributes:
            array.append(attr.name)
        return array

    def remove_if_not_in_array(self, array, attr_type):
        names_array = self.get_names_array()
        for name in names_array:
            if name not in array:
                self.remove(attr_type, name)

    def save(self, character_name, character_role):
        db_mgr = DBManager()
        for attribute in self.attributes:
            print(attribute)
            if attribute.attr_type == 'skill':
                db_mgr.skills.add_or_modify_skill(character_name=character_name, character_role=character_role,
                                                  skill_name=attribute.name, chipped=False, ip=0, lvl=attribute.lvl,
                                                  field=attribute.field)
            elif attribute.attr_type == 'talent':
                db_mgr.attributes.add_or_modify(attribute_type='talent', blueprint_name=attribute.name,
                                                actor_name=character_name, actor_role=character_role,
                                                field=attribute.field, lvl=attribute.lvl)


class ComplicationManager(AttributeManager):
    def __init__(self):
        super(ComplicationManager, self).__init__()

    def add_complication(self, attr_name, frequency, intensity, importance, field=""):
        self.attributes.append(Complication(name=attr_name, frequency=frequency, intensity=intensity,
                                            importance=importance, field=field))

    def modify(self, name, field, intensity=None, frequency=None, importance=None):
        c = self.get_attribute(attr_type='complication', attr_name=name, field=field)
        if c:
            if intensity is not None:
                c.intensity = intensity
            if frequency is not None:
                c.frequency = frequency
            if importance is not None:
                c.importance = importance

    def already_exists(self, attr_name, field):
        attr = Complication(attr_name, field=field)
        if attr in self.attributes:
            return True
        else:
            return False

    def add_if_new(self, attr_name, field, frequency, intensity, importance):
        if self.already_exists(attr_name, field):
            pass
        else:
            self.add_complication(attr_name=attr_name, frequency=frequency, intensity=intensity, importance=importance,
                                  field=field)

    def save(self, character_name, character_role):
        db_mgr = DBManager()

        for attribute in self.attributes:
            num_freq = 0
            num_inte = 0
            num_impo = 0

            if attribute.frequency == 'infrequently':
                num_freq = 5
            elif attribute.frequency == 'frequently':
                num_freq = 10
            else:
                num_freq = 15

            if attribute.intensity == 'mild':
                num_inte = 5
            elif attribute.intensity == 'strong':
                num_inte = 10
            elif attribute.intensity == 'severe':
                num_inte = 15
            else:
                num_inte = 20

            if attribute.importance == 'minor':
                num_impo = 5
            elif attribute.importance == 'major':
                num_impo = 2
            else:
                num_impo = 1

            db_mgr.complications.add_or_modify(actor_name=character_name, actor_role=character_role,
                                               blueprint_name=attribute.name, frequency=num_freq,
                                               intensity=num_inte, importance=num_impo)


class PerkManager(AttributeManager):
    def __init__(self):
        super(PerkManager, self).__init__()

    def add_attribute(self, attr_name, lvl=0, field="", attr_type='perk', target_person=""):
        self.attributes.append(Perk(name=attr_name, lvl=lvl, field=field, target_person_name=target_person))

    def already_exists(self, attr_name, field, target_person):
        attr = Perk(name=attr_name, field=field, target_person_name=target_person, lvl=1)
        if attr in self.attributes:
            return True
        else:
            return False

    def add_if_new(self, attr_name, field, lvl, target_person):
        if self.already_exists(attr_name, field, target_person):
            pass
        else:
            self.add_attribute(attr_name=attr_name, field=field, lvl=lvl, target_person=target_person)

    def clear(self):
        del self.attributes[:]


class SkillManager(object):
    def add_everyman_skills(self):
        self.add_skill('awarness / notice')
        self.add_skill('education & gen know')
        self.add_skill('persuasion & fast talk')
        self.add_skill('athletics')
        self.add_skill('teaching')
        self.add_skill('brawling / hand to hand')
        self.add_skill('dodge & escape')


if __name__ == '__main__':
    am = AttributeManager()
    am.add_attribute('skill', 'handgun', 1, None)
    print(am.attributes)
    am.remove('skill', 'handgun')
    print(am.attributes)
