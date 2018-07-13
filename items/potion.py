from bs4 import Tag

from items.base_item import base_item

class Potion(base_item):

    @property
    def default_color(self) -> str: return "Maroon"

    @property
    def default_icon(self) -> str: return "drink-me"

    def _get_subtitle(self, xml: Tag):
        subtitle = 'Potion, '
        if xml.detail is not None:
            subtitle += xml.detail.text + ', '
        if xml.weight is not None:
            subtitle += xml.weight.text + 'lb'
        return  subtitle

    @staticmethod
    def from_xml(xml: Tag):
        data = Potion._get_common_data(Potion, xml)
        return Potion(data['title'], data['subtitle'], data['descriptions'])