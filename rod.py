from bs4 import Tag
from rpg_card import RpgCard


class Rod(object):

    default_color = "Grey"
    default_icon = "bo"

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
        return Rod(title, rarity, weight, description)

    def to_rpg_card(self) -> RpgCard:
        card = RpgCard(self.title, Rod.default_color, Rod.default_icon)
        card.add_subtitle(self.rarity + ", " + self.weight + "lb")
        for text in self.description:
            card.add_text(text)
        return card

    def __init__(self, title: str, rarity: str, weight: str, description: list):
        super(Rod, self).__init__()
        self.title = title
        self.rarity = rarity
        self.weight = weight
        self.description = description
