from abc import ABC, abstractmethod

from bs4 import Tag

from rpg_card import RpgCard


class base_item(ABC):

    @property
    @abstractmethod
    def default_color(self) -> str:
        pass

    @property
    @abstractmethod
    def default_icon(self) -> str:
        pass

    @staticmethod
    def _get_title(xml: Tag) -> str:
        return xml.findChild("name").text  # Can't use the name child directly as it returns the parent tag name

    @abstractmethod
    def _get_subtitle(self, xml) -> str:
        pass

    @staticmethod
    def _get_descriptions(xml):
        descriptions = list([])
        for text_node in xml.findAll("text"):
            text = text_node.text.strip()
            if text == '':
                continue
            descriptions.append(text)
        return descriptions

    @staticmethod
    def _get_common_data(self, xml):
        title = self._get_title(xml)
        subtitle = self._get_subtitle(self, xml)
        descriptions = self._get_descriptions(xml)
        return {'title': title, 'subtitle': subtitle, 'descriptions': descriptions}

    def __init__(self, title: str, subtitle: str, descriptions: list):
        super(base_item, self).__init__()
        self.title = title
        self.subtitle = subtitle
        self.descriptions = descriptions

    def to_rpg_card(self) -> RpgCard:
        card = RpgCard(self.title, self.default_color, self.default_icon)
        self.add_subtitle(card)
        self.add_descriptions(card)
        return card

    def add_descriptions(self, card):
        for text in self.descriptions:
            card.add_description(text)

    def add_subtitle(self, card):
        card.add_subtitle(self.subtitle)