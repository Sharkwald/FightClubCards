from bs4 import Tag
from rpg_card import RpgCard


class Ring(object):

    default_color = "Orange"
    default_icon = "ring"

    @staticmethod
    def from_xml(xml: Tag):
        title = xml.findChild("name").text # Can't use the name child directly as it returns the parent tag name
        rarity = xml.detail.text
        description = list([])
        for text_node in xml.findAll("text"):
            text = text_node.text.strip()
            if text == '':
                continue
            description.append(text)
        return Ring(title, rarity, description)

    def to_rpg_card(self) -> RpgCard:
        card = RpgCard(self.title, Ring.default_color, Ring.default_icon)
        self.add_subtitle(card)
        self.add_descriptions(card)
        return card

    def add_descriptions(self, card):
        for text in self.description:
            card.add_description(text)

    def add_subtitle(self, card):
        subtitle = 'Ring, ' + self.rarity
        card.add_subtitle(subtitle)

    def __init__(self, title: str, rarity: str, description: list):
        super(Ring, self).__init__()
        self.title = title
        self.rarity = rarity
        self.description = description
