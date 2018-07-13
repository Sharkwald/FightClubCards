from bs4 import Tag

from items.base_item import base_item


class Ring(base_item):

    @property
    def default_color(self) -> str: return "Orange"

    @property
    def default_icon(self) -> str: return "ring"

    def _get_subtitle(self, xml: Tag):
        return 'Ring, ' + xml.detail.text

    @staticmethod
    def from_xml(xml: Tag):
        data = Ring._get_common_data(Ring, xml)
        return Ring(data['title'], data['subtitle'], data['descriptions'])
