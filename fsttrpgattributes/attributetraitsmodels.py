from traits.api import HasTraits, Any, Range, String, Enum, List, Instance, Button, Method
from traitsui.api import View, HGroup, Item, CheckListEditor, VGroup, ListEditor

from databases import DBManager
from fsttrpgbasicinfo.traitmvc.models import CharacterName
from fsttrpgbasicinfo.traitmvc.views import BasicInfo
from models import AttributeLists, AttributeManager, PerkManager, ComplicationManager

all_skills_list = AttributeLists('skill')
all_talents_list = AttributeLists('talent')
all_complications_list = AttributeLists('complication')
all_perks_list = AttributeLists('perk')

skill_mgr = AttributeManager()
talent_mgr = AttributeManager()
perk_mgr = PerkManager()
comp_mgr = ComplicationManager()


class Attribute(HasTraits):
    name = Any()
    lvl = Range(1, 10, mode='spinner')
    field = String()

    view = View(
        HGroup(
            Item('name'),
            Item('field'),
            Item('lvl')
        )
    )


class Talent(Attribute):
    name = Enum(all_talents_list.all_attribute_names)

    def _lvl_changed(self):
        talent_mgr.modify_lvl(attr_type='talent', attr_name=self.name, field=self.field, lvl=self.lvl)

    def _field_changed(self):
        talent_mgr.modify_field(attr_type='talent', attr_name=self.name, field=self.field)


class Skill(Attribute):
    name = Enum(all_skills_list.all_attribute_names)

    def _lvl_changed(self):
        skill_mgr.modify_lvl(attr_type='skill', attr_name=self.name, field=self.field, lvl=self.lvl)

    def _field_changed(self):
        skill_mgr.modify_field(attr_type='skill', attr_name=self.name, field=self.field)


class Complication(Attribute):
    name = Enum(all_complications_list.all_attribute_names)
    frequency = Enum('infrequently', 'frequently', 'constantly')
    intensity = Enum('mild', 'strong', 'severe', 'extreme')
    importance = Enum('minor', 'major', 'extreme')

    def _frequency_changed(self):
        comp_mgr.modify(self.name, self.field, frequency=self.frequency)

    def _intensity_changed(self):
        comp_mgr.modify(self.name, self.field, intensity=self.intensity)

    def _importance_changed(self):
        comp_mgr.modify(self.name, self.field, importance=self.importance)

    def _field_changed(self):
        comp_mgr.modify_field('complication', self.name, self.field)

    view = View(
        HGroup(
            Item('name'),
            Item('frequency'),
            Item('intensity'),
            Item('importance'),
            Item('field')
        )
    )


class CustomBasicInfo(BasicInfo):
    perk = Instance(Attribute)

    def _character_name_default(self):
        return CharacterName(name_change_handler=self.name_changed)

    def name_changed(self):
        self.perk.person = self.character_name.get_name()


class Perk(Attribute):
    name = Enum(all_perks_list.all_attribute_names)
    person = String()
    roll_person = Button()
    configure_person = Instance(CustomBasicInfo, ())

    def _configure_person_default(self):
        return CustomBasicInfo(perk=self)

    def _roll_person_fired(self):
        self.configure_person._random_all_fired()

    view = View(
        HGroup(
            Item('name'),
            Item('lvl'),
            Item('field'),
            Item('person'),
            Item('roll_person', show_label=False),
            Item('configure_person', show_label=False)
        )
    )


class SkillsCheckBoxEditor(HasTraits):
    all_skills = List(editor=CheckListEditor(values=all_skills_list.all_attribute_names, cols=6))
    change_listener = Method()

    def _all_skills_changed(self):
        self.change_listener()

    view = View(
        Item('all_skills', style='custom', show_label=False)
    )


class TalentCheckBoxEditor(HasTraits):
    all_talents = List(editor=CheckListEditor(values=all_talents_list.all_attribute_names, cols=2))
    change_listener = Method()

    def _all_talents_changed(self):
        self.change_listener()

    view = View(
        Item('all_talents', style='custom', show_label=False)
    )


class PerkCheckBoxEditor(HasTraits):
    all_perks = List(editor=CheckListEditor(values=all_perks_list.all_attribute_names, cols=2))
    change_listener = Method()

    def _all_perks_changed(self):
        self.change_listener()

    view = View(
        Item('all_perks', style='custom', show_label=False)
    )


class ComplicationCheckBoxEditor(HasTraits):
    all_complications = List(editor=CheckListEditor(values=all_complications_list.all_attribute_names, cols=4))
    change_listener = Method()

    def _all_complications_changed(self):
        self.change_listener()

    view = View(
        Item('all_complications', style='custom', show_label=False)
    )


class SkillsList(HasTraits):
    equipped_skills = List(Instance(Skill, ()))

    view = View(
        Item('equipped_skills', show_label=False, editor=ListEditor(style='custom'), resizable=False)
    )

    def update(self):
        self.equipped_skills = []
        for attribute in skill_mgr.attributes:
            self.equipped_skills.append(Skill(name=attribute.name, lvl=attribute.lvl, field=attribute.field))

    def _equipped_skills_changed(self, name, old, new):
        # print("_skills_changed: %s %s %s" % (name, str(old), str(new)))
        # print(str(new))
        pass

    def _equipped_skills_items_changed(self, name, old, new):
        # print("_skills_items_changed: %s %s %s" % (name, str(old), str(new)))
        # print('skill items changed')
        pass


class TalentsList(HasTraits):
    equipped_talents = List(Instance(Talent, ()))
    view = View(
        Item('equipped_talents', show_label=False, editor=ListEditor(style='custom'), resizable=False)
    )

    def update(self):
        self.equipped_talents = []
        for attribute in talent_mgr.attributes:
            self.equipped_talents.append(Talent(name=attribute.name, lvl=attribute.lvl, field=attribute.field))


class PerkList(HasTraits):
    equipped_perks = List(Instance(Perk, ()))
    view = View(
        Item('equipped_perks', show_label=False, editor=ListEditor(style='custom'), resizable=False)
    )

    def add(self, name, lvl=1, field="", person=""):
        self.equipped_perks.append(Perk(name=name, lvl=lvl, field=field, person=person))

    def update(self):
        self.equipped_perks = []
        for attribute in perk_mgr.attributes:
            self.equipped_perks.append(Perk(name=attribute.name, lvl=attribute.lvl, field=attribute.field,
                                            person=attribute.target_person_name))

    def save(self, actor_role, actor_name):
        db_mgr = DBManager()
        for perk in self.equipped_perks:
            if perk.person != "":
                perk.configure_person.save()
                db_mgr.perks.add_or_modify_perk(actor_role=actor_role, actor_name=actor_name, blueprint_name=perk.name,
                                                lvl=perk.lvl, field=perk.field,
                                                target_name=perk.configure_person.character_name.get_name(),
                                                target_role=perk.configure_person.character_name.role)
            else:
                db_mgr.perks.add_or_modify_perk(actor_role=actor_role, actor_name=actor_name, blueprint_name=perk.name,
                                                lvl=perk.lvl, field=perk.field)


class PerkListActiveEditMode(PerkList):
    def _equipped_perks_changed(self):
        perk_mgr.clear()
        for perk in self.equipped_perks:
            perk_mgr.add_attribute(attr_name=perk.name, lvl=perk.lvl, field=perk.field, target_person=perk.person)


class ComplicationList(HasTraits):
    equipped_complications = List(Instance(Complication, ()))
    view = View(
        Item('equipped_complications', show_label=False, editor=ListEditor(style='custom'), resizable=False)
    )

    def update(self):
        self.equipped_complications = []
        for complication in comp_mgr.attributes:
            self.equipped_complications.append(Complication(name=complication.name, field=complication.field,
                                                            frequency=complication.frequency,
                                                            intensity=complication.intensity,
                                                            importance=complication.importance))


class SkillWindow(HasTraits):
    skills = Instance(SkillsCheckBoxEditor, ())
    equipped = Instance(SkillsList, ())

    def _skills_default(self):
        return SkillsCheckBoxEditor(change_listener=self.checkbox_selection_changed)

    def checkbox_selection_changed(self):
        for skill in self.skills.all_skills:
            skill_mgr.add_if_new(attr_type='skill', attr_name=skill, lvl=1, field="")
        skill_mgr.remove_if_not_in_array(self.skills.all_skills, attr_type='skill')
        self.equipped.update()

    view = View(
        Item('skills', style='custom'),
        Item('equipped')
    )


class TalentWindow(HasTraits):
    talents = Instance(TalentCheckBoxEditor, ())
    equipped = Instance(TalentsList, ())

    def _talents_default(self):
        return TalentCheckBoxEditor(change_listener=self.checkbox_selection_changed)

    def checkbox_selection_changed(self):
        for talent in self.talents.all_talents:
            talent_mgr.add_if_new(attr_type='talent', attr_name=talent, lvl=1, field="")
        talent_mgr.remove_if_not_in_array(self.talents.all_talents, attr_type='talent')
        self.equipped.update()

    view = View(
        Item('talents', style='custom'),
        Item('equipped')
    )


class PerkWindow(HasTraits):
    # perks = Instance(PerkCheckBoxEditor, ())
    equipped = Instance(PerkListActiveEditMode, ())

    '''
    def _perks_default(self):
        return PerkCheckBoxEditor(change_listener=self.checkbox_selection_changed)
    '''
    '''
    def checkbox_selection_changed(self):
        for perk in self.perks.all_perks:
            perk_mgr.add_if_new(attr_name=perk, field="", lvl=1, target_person="")
        perk_mgr.remove_if_not_in_array(self.perks.all_perks, attr_type='perk')
        self.equipped.update()
    '''
    view = View(
        # Item('perks', style='custom'),
        Item('equipped')
    )


class ComplicationWindow(HasTraits):
    complications = Instance(ComplicationCheckBoxEditor, ())
    equipped = Instance(ComplicationList, ())

    def _complications_default(self):
        return ComplicationCheckBoxEditor(change_listener=self.checkbox_selection_changed)

    def checkbox_selection_changed(self):
        for complication in self.complications.all_complications:
            comp_mgr.add_if_new(attr_name=complication, frequency='infrequently', importance='minor', intensity='mild',
                                field="")
        comp_mgr.remove_if_not_in_array(self.complications.all_complications, attr_type='complication')
        self.equipped.update()

    view = View(
        Item('complications', style='custom'),
        Item('equipped')
    )


class CareerPackageMaker(HasTraits):
    career_pack_name = String()
    skills = Instance(SkillsCheckBoxEditor, ())
    talents = Instance(TalentCheckBoxEditor, ())
    perks = Instance(PerkCheckBoxEditor, ())
    save_pack = Button()

    view = View(
        VGroup(
            Item('career_pack_name'),
            Item('skills'),
            Item('talents'),
            Item('perks'),
            Item('save_pack', show_label=False)
        )
    )

    def _save_pack_fired(self):
        db_mgr = DBManager()
        for skill in self.skills.all_skills:
            db_mgr.career_packs.add(career_name=self.career_pack_name, attr_type='skill', attr_name=skill)
        for talent in self.talents.all_talents:
            db_mgr.career_packs.add(career_name=self.career_pack_name, attr_type='talent', attr_name=talent)
        for perk in self.perks.all_perks:
            db_mgr.career_packs.add(career_name=self.career_pack_name, attr_type='perk', attr_name=perk)


if __name__ == '__main__':
    # tw = TalentWindow()
    # tw.configure_traits()
    cp = CareerPackageMaker()
    cp.configure_traits()
    # pw = PerkWindow()
    # pw.configure_traits()
