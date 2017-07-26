from traits.api import HasTraits, String, Instance, Button
from traitsui.api import View, VGroup, Item

import aws
from application.attributes.attributetraitsmodels import SkillsCheckBoxEditor, TalentCheckBoxEditor, PerkCheckBoxEditor
from databases import DBManager


class CareerPackageMaker(HasTraits):
    career_pack_name = String()
    skills = Instance(SkillsCheckBoxEditor, ())
    talents = Instance(TalentCheckBoxEditor, ())
    perks = Instance(PerkCheckBoxEditor, ())
    save_pack = Button()
    upload_pack = Button()

    def change_listener(self):
        pass

    def _skills_default(self):
        return SkillsCheckBoxEditor(change_listener=self.change_listener)

    def _talents_default(self):
        return TalentCheckBoxEditor(change_listener=self.change_listener)

    def _perks_default(self):
        return PerkCheckBoxEditor(change_listener=self.change_listener)

    view = View(
        VGroup(
            Item('career_pack_name'),
            Item('skills'),
            Item('talents'),
            Item('perks'),
            Item('save_pack', show_label=False),
            Item('upload_pack', show_label=False)
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

    def _upload_pack_fired(self):
        career_name = self.career_pack_name
        for skill in self.skills.all_skills:
            aws.upload_pack_member(career_name, attr_type='skill', attr_name=skill)
        for talent in self.talents.all_talents:
            aws.upload_pack_member(career_name, attr_type='talent', attr_name=talent)
        for perk in self.perks.all_perks:
            aws.upload_pack_member(career_name, attr_type='perk', attr_name=perk)


if __name__ == '__main__':
    cp = CareerPackageMaker()
    cp.configure_traits()
