import re

from bs4 import Tag

from items.base_item import base_item
from rpg_card import RpgCard


def _parse_bonus_armor(xml) -> str:
    bonus = ''
    regex = re.compile('.*you have a \+([\d]+) bonus to AC.*')
    for text_node in xml.findAll("text"):
        text = text_node.text.strip()
        if regex.match(text):
            bonus_text_match = regex.match(text)
            bonus = bonus_text_match.group(1)
            break
    return bonus


class Shield(base_item):

    @property
    def default_color(self) -> str: return "DimGrey"

    @property
    def default_icon(self) -> str: return "checked-shield"

    def _get_subtitle(self, xml: Tag):
        rarity = xml.detail.text if xml.detail != None else ''
        weight = xml.weight.text
        subtitle = 'Shield, '
        if rarity != '':
            subtitle += rarity + ', '
        subtitle += weight + 'lb'
        return subtitle

    @staticmethod
    def from_xml(xml: Tag):
        data = Shield._get_common_data(Shield, xml)
        base_armor = xml.ac.text
        bonus_armor = _parse_bonus_armor(xml)
        return Shield(data['title'], data['subtitle'], data['descriptions'], base_armor, bonus_armor)

    def to_rpg_card(self) -> RpgCard:
        card = super().to_rpg_card()
        card.add_bonus("AC", self.base_armor)
        if self.bonus_armor != '':
            card.add_bonus("Bonus AC", "+" + self.bonus_armor)
        return card

    def __init__(self, title: str, subtitle: str, descriptions: list, base_armor: str, bonus_armor: str):
        super(Shield, self).__init__(title, subtitle, descriptions)
        self.base_armor = base_armor
        self.bonus_armor = bonus_armor
