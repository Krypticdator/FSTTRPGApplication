from traits.api import HasTraits, Int, Enum, Button, Instance, Range
from traitsui.api import View, Item

from attributetraitsmodels import SkillWindow, TalentWindow, ComplicationWindow, PerkWindow, skill_mgr, talent_mgr, \
    comp_mgr
from databases import DBManager
from fsttrpgcharloader.traitsmodels import CharacterName

database_manager = DBManager()


class AttributeRandomizer(HasTraits):
    skill_min_lvl = Range(1, 10, mode='spinner', value=2)
    skill_max_lvl = Range(1, 10, mode='spinner', value=9)
    number_of_changes_to_get_talent = Int(1)
    percentage_to_get_talent = Range(1, 100, mode='spinner', value=20)
    number_of_contacts_max = Int(3)
    number_of_contacts_min = Int(1)
    number_of_favors_max = Int(3)
    number_of_favors_min = Int(1)
    change_to_get_renown = Range(1, 100, mode='spinner', value=10)
    change_to_get_streetdeal = Range(1, 100, mode='spinner', value=10)
    number_of_random_skills = Int(3)
    skill_points_max = Int(-1)


class CharacterAttributes(HasTraits):
    # TODO - Load careers dynamically
    career = Enum('none', 'solo', 'corporate', 'media', 'nomad', 'techie', 'cop', 'rockerboy', 'tech', 'med tech',
                  'fixer')
    # configure_randomizer = Instance(AttributeRandomizer, ())
    # career = Enum(database_manager.career_packs.get_pack_names())
    option_points_allocated = Int()
    generate_career_package = Button()
    choose_skills = Instance(SkillWindow, ())
    choose_talents = Instance(TalentWindow, ())
    choose_perks = Instance(PerkWindow, ())
    choose_complications = Instance(ComplicationWindow, ())

    def _generate_career_package_fired(self):
        db_mgr = DBManager()
        attributes = db_mgr.career_packs.get_pack_skills(self.career)

        for attribute in attributes:
            attribute_type = attribute.attribute_blueprint.attribute_type
            if attribute_type == 'skill':
                self.choose_skills.skills.all_skills.append(attribute.attribute_blueprint.name)
                self.choose_skills.checkbox_selection_changed()
            elif attribute_type == 'talent':
                self.choose_talents.talents.all_talents.append(attribute.attribute_blueprint.name)
                self.choose_talents.checkbox_selection_changed()
            elif attribute_type == 'perk':
                self.choose_perks.equipped.add(attribute.attribute_blueprint.name)

    view = View(
        # Item('configure_randomizer'),
        Item('career'),
        Item('option_points_allocated', style='readonly'),
        Item('generate_career_package', show_label=False),
        Item('choose_skills'),
        Item('choose_talents'),
        Item('choose_perks'),
        Item('choose_complications')
    )


class Standalone(HasTraits):
    character_name = Instance(CharacterName, ())
    attributes = Instance(CharacterAttributes, ())
    save = Button()

    def _save_fired(self):
        skill_mgr.save(character_name=self.character_name.get_name(), character_role=self.character_name.role)
        talent_mgr.save(character_name=self.character_name.get_name(), character_role=self.character_name.role)
        comp_mgr.save(character_name=self.character_name.get_name(), character_role=self.character_name.role)
        self.attributes.choose_perks.equipped.save(self.character_name.role, self.character_name.get_name())

    def _character_name_default(self):
        return CharacterName(name_change_handler=self.load_character_skills)

    def load_character_skills(self):
        pass

    view = View(
        Item('character_name', style='custom', show_label=False),
        Item('attributes', show_label=False, style='custom'),
        Item('save', show_label=False)
    )


if __name__ == '__main__':
    s = Standalone()
    s.configure_traits()
