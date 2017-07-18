from traits.api import HasTraits, Any, Range, String, Enum, List, Instance, Button, Float
from traitsui.api import View, HGroup, Item, ListEditor, VGroup

from application.attributes.databases import DBManager
from application.attributes.models import AttributeLists
from application.basicinfo.models import Names
from application.basicinfo.traitmvc.models import BasicInfo

ALL_SKILLS_LIST = AttributeLists('skill')
ALL_TALENTS_LIST = AttributeLists('talent')
ALL_COMPLICATIONS_LIST = AttributeLists('complication')
ALL_PERKS_LIST = AttributeLists('perk')
NAMES = Names('us', check_aws=False)

FREQUENCY_NUMBER_VALUES = {'infrequently': 5, 'frequently': 10, 'constantly': 15}
FREQUENCY_TEXT_VALUES = {5: 'infrequently', 10: 'frequently', 15: 'constantly'}

INTENSITY_NUMBER_VALUES = {'mild': 5, 'strong': 10, 'severe': 15, 'extreme': 20}
INTENSITY_TEXT_VALUES = {5: 'mild', 10: 'strong', 15: 'severe', 20: 'extreme'}

IMPORTANCE_NUMBER_VALUES = {'minor': 5, 'major': 2, 'extreme': 1}
IMPORTANCE_TEXT_VALUES = {5: 'minor', 2: 'major', 1: 'extreme'}

EVERYMAN_SKILLS = ['awarness / notice',
                   'education & gen know',
                   'persuasion & fast talk',
                   'athletics',
                   'teaching',
                   'brawling / hand to hand',
                   'dodge & escape']


class Attribute(HasTraits):
    name = Any()
    lvl = Range(1, 10, mode='spinner')
    field = String()
    attribute_type = String('attribute')
    cost = Float()

    def recalculate_cost(self):
        if self.name == 'none':
            return
        attr_type = self.attribute_type
        cost = 0
        if attr_type == 'talent':
            cost = ALL_TALENTS_LIST.costs[self.name]
        elif attr_type == 'perk':
            cost = ALL_PERKS_LIST.costs[self.name]
            print('perk cost: ' + str(cost))
        elif attr_type == 'skill':
            cost = ALL_SKILLS_LIST.costs[self.name]
        self.cost = cost * self.lvl

    def _name_changed(self):
        self.recalculate_cost()

    def _lvl_changed(self):
        self.recalculate_cost()

    def save(self, actor_name, actor_role):
        if self.name == 'none':
            return
        db_mgr = DBManager()
        db_mgr.attributes.add_or_modify(attribute_type=self.attribute_type, blueprint_name=self.name,
                                        actor_name=actor_name, actor_role=actor_role, lvl=self.lvl, field=self.field)

    view = View(
        HGroup(
            Item('name'),
            Item('field'),
            Item('lvl')
        )
    )


class Talent(Attribute):
    name = Enum(ALL_TALENTS_LIST.all_attribute_names)

    attribute_type = 'talent'


class Skill(Attribute):
    name = Enum(ALL_SKILLS_LIST.all_attribute_names)

    attribute_type = 'skill'

    def save(self, actor_name, actor_role):
        if self.name == 'none':
            return
        db_mgr = DBManager()
        db_mgr.skills.add_or_modify_skill(character_name=actor_name, character_role=actor_role, skill_name=self.name,
                                          chipped=False, ip=0, lvl=self.lvl, field=self.field)


class Complication(Attribute):
    name = Enum(ALL_COMPLICATIONS_LIST.all_attribute_names)
    frequency = Enum('infrequently', 'frequently', 'constantly')
    intensity = Enum('mild', 'strong', 'severe', 'extreme')
    importance = Enum('minor', 'major', 'extreme')

    attribute_type = 'complication'

    def _frequency_changed(self):
        self.calculate_cost()

    def _intensity_changed(self):
        self.calculate_cost()

    def _importance_changed(self):
        self.calculate_cost()

    def calculate_cost(self):
        frequency = FREQUENCY_NUMBER_VALUES[self.frequency]
        importance = IMPORTANCE_NUMBER_VALUES[self.importance]
        intensity = INTENSITY_NUMBER_VALUES[self.intensity]

        self._lvl_changed()
        self.cost = ((frequency + intensity) / importance) * -1

    def save(self, actor_name, actor_role):
        if self.name == 'none':
            return
        frequency = FREQUENCY_NUMBER_VALUES[self.frequency]
        importance = IMPORTANCE_NUMBER_VALUES[self.importance]
        intensity = INTENSITY_NUMBER_VALUES[self.intensity]
        db_mgr = DBManager()
        db_mgr.complications.add_or_modify(actor_name=actor_name, actor_role=actor_role, blueprint_name=self.name,
                                           intensity=intensity, frequency=frequency, importance=importance)

    view = View(
        HGroup(
            Item('name'),
            VGroup(
                Item('frequency'),
                Item('intensity'),
                Item('importance'),
            ),
            VGroup(
                Item('field'),
                Item('cost', style='readonly')
            )
        )
    )


class Perk(Attribute):
    name = Enum(ALL_PERKS_LIST.all_attribute_names)
    person_name = String()
    attribute_type = 'perk'
    person_basic_info = BasicInfo()

    def _name_changed(self):
        if self.name == 'contact' or self.name == 'favor':
            if self.person_basic_info.character_name.get_name() == "":
                self.person_basic_info.random_all()
        self.person_name = self.person_basic_info.character_name.get_name()

    def save(self, actor_name, actor_role):
        if self.name == 'none':
            return
        db_mgr = DBManager()
        if self.name == 'contact' or self.name == 'favor':
            self.person_basic_info.save()
            t_name = self.person_basic_info.character_name.get_name()
            t_role = self.person_basic_info.character_name.role
            db_mgr.perks.add_or_modify_perk(actor_role=actor_role, actor_name=actor_name, blueprint_name=self.name,
                                            lvl=self.lvl, field=self.field, target_role=t_role, target_name=t_name)
        else:
            db_mgr.perks.add_or_modify_perk(actor_role=actor_role, actor_name=actor_name, blueprint_name=self.name,
                                            lvl=self.lvl, field=self.field)

    view = View(
        VGroup(
            HGroup(
                Item('name'),
                Item('lvl'),
                Item('field'),

            ),
            HGroup(
                Item('person_name', style='readonly'),
                Item('cost', style='readonly')
            )
        )
    )


class AttributeList(HasTraits):
    attributes = List(Instance(Attribute, ()))
    character_points_spend = Float()
    attribute_name = String()
    recalculate = Button()

    def _attributes_changed(self):
        pass

    def _recalculate_fired(self):
        total_points = 0
        for attribute in self.attributes:
            total_points += attribute.cost
        self.character_points_spend = total_points

    def save(self, actor_name, actor_role):
        for attribute in self.attributes:
            attribute.save(actor_name, actor_role)

    view = View(
        VGroup(
            HGroup(
                Item('character_points_spend', style='readonly'),
                Item('recalculate', show_label=False)
            ),

            Item('attributes', show_label=False, editor=ListEditor(style='custom')),
            # show_border=True
        )
    )


class TalentList(AttributeList):
    attributes = List(Instance(Talent, ()))

    def load(self, actor_name, actor_role):
        self.attributes = []
        db_mgr = DBManager()
        array = db_mgr.attributes.load_attributes_of(actor_role=actor_role, actor_name=actor_name,
                                                     attribute_type='talent')
        for t in array:
            talent = Talent(name=t.name, lvl=t.lvl, field=t.field)
            self.attributes.append(talent)

    def _attributes_default(self):
        return [Talent()]


class SkillList(AttributeList):
    attributes = List(Instance(Skill, ()))

    def _attributes_default(self):
        eskills = []
        for skill in EVERYMAN_SKILLS:
            eskills.append(Skill(name=skill, lvl=2))
        return eskills

    def load(self, actor_name, actor_role):
        self.attributes = []
        db_mgr = DBManager()
        skills = db_mgr.skills.load_skills_of(actor_role=actor_role, actor_name=actor_name)
        for s in skills:
            skill = Skill(name=s.name, lvl=s.lvl, field=s.field)
            self.attributes.append(skill)


class ComplicationList(AttributeList):
    attributes = List(Instance(Complication, ()))

    def _attributes_default(self):
        return [Complication()]

    def load(self, actor_name, actor_role):
        db_mgr = DBManager()
        self.attributes = []
        db_complications = db_mgr.complications.load_complications_of(actor_name=actor_name, actor_role=actor_role)
        for c in db_complications:
            intensity = INTENSITY_TEXT_VALUES[c.intensity]
            frequency = FREQUENCY_TEXT_VALUES[c.frequency]
            importance = IMPORTANCE_TEXT_VALUES[c.importance]
            complication = Complication(name=c.name, intensity=intensity, frequency=frequency, importance=importance)
            complication.calculate_cost()
            self.attributes.append(complication)


class PerkList(AttributeList):
    attributes = List(Instance(Perk, ()))

    def load(self, actor_name, actor_role):
        db_mgr = DBManager()
        self.attributes = []
        db_perks = db_mgr.perks.get_perks_of_actor(actor_role=actor_role, actor_name=actor_name)

        for p in db_perks:
            name = p.name
            field = p.field
            lvl = p.lvl
            if p.target_name is not None:
                bi = BasicInfo()
                bi.character_name.set_name(p.target_name)
                bi.character_name.role = p.target_role
                bi.load()
                self.attributes.append(Perk(name=name, field=field, lvl=lvl, person_basic_info=bi))
            else:
                self.attributes.append(Perk(name=name, field=field, lvl=lvl))

    def _attributes_default(self):
        return [Perk()]


if __name__ == '__main__':
    tl = TalentList()
    tl.configure_traits()
