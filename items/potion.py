from bs4 import Tag
from rpg_card import RpgCard


class Potion(object):

    default_color = "Maroon"
    default_icon = "drink-me"

    @staticmethod
    def from_xml(xml: Tag):
        title = xml.findChild("name").text # Can't use the name child directly as it returns the parent tag name
        rarity = xml.detail.text
        weight = xml.weight.text
        description = list([])
        for text_node in xml.findAll("text"):
            text = text_node.text.strip()
            if text == '':
                continue
            description.append(text)
        return Potion(title, rarity, weight, description)

    def to_rpg_card(self) -> RpgCard:
        card = RpgCard(self.title, Potion.default_color, Potion.default_icon)
        self.add_subtitle(card)
        self.add_descriptions(card)
        return card

    def add_descriptions(self, card):
        for text in self.description:
            card.add_description(text)

    def add_subtitle(self, card):
        subtitle = 'Potion, ' + self.rarity + ', ' + self.weight + 'lb'
        card.add_subtitle(subtitle)

    def __init__(self, title: str, rarity: str, weight: str, description: list):
        super(Potion, self).__init__()
        self.title = title
        self.rarity = rarity
        self.weight = weight
        self.description = description
