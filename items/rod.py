from bs4 import Tag

from items.base_item import base_item

class Rod(base_item):

    @property
    def default_color(self) -> str: return "DimGrey"

    @property
    def default_icon(self) -> str: return "bo"

    def _get_subtitle(self, xml: Tag):
        subtitle = 'Rod, '
        if xml.detail is not None:
            subtitle += xml.detail.text + ', '
        if xml.weight is not None:
            subtitle += xml.weight.text + 'lb'
        return  subtitle

    @staticmethod
    def from_xml(xml: Tag):
        data = Rod._get_common_data(Rod, xml)
        return Rod(data['title'], data['subtitle'], data['descriptions'])
