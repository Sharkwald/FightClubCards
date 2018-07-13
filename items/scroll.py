from bs4 import Tag

from items.base_item import base_item


class Scroll(base_item):

    @property
    def default_color(self) -> str: return "SaddleBrown"

    @property
    def default_icon(self) -> str: return "tied-scroll"

    def _get_subtitle(self, xml: Tag):
        return 'Scroll, ' + xml.detail.text

    @staticmethod
    def from_xml(xml: Tag):
        data = Scroll._get_common_data(Scroll, xml)
        return Scroll(data['title'], data['subtitle'], data['descriptions'])
