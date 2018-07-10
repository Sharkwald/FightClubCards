
item_types = list([{'key': '$', 'desc': 'Currency'},
                   {'key': 'A', 'desc': 'Ammunition'},
                   {'key': 'G', 'desc': 'General'},
                   {'key': 'HA', 'desc': 'Heavy armor'},
                   {'key': 'LA', 'desc': 'Light armor'},
                   {'key': 'M', 'desc': 'Melee weapon'},
                   {'key': 'MA', 'desc': 'Medium armor'},
                   {'key': 'P', 'desc': 'Potion'},
                   {'key': 'R', 'desc': 'Ranged weapon'},
                   {'key': 'RD', 'desc': 'Rod'},
                   {'key': 'RG', 'desc': 'Ring'},
                   {'key': 'S', 'desc': 'Shield'},
                   {'key': 'SC', 'desc': 'Staff'},
                   {'key': 'ST', 'desc': 'Scroll'},
                   {'key': 'W', 'desc': 'Wondrous item'},
                   {'key': 'WD', 'desc': 'Wand'}
                  ])


weapon_properties = list(['ammunition','finesse','heavy','light','loading','range','reach','special','thrown','two-handed','versatile'])

import json

class RpgCard(object):

    def add_subtitle(self, subtitle: str):
        """Adds a subtitle to the card, always as the first entry in the contents list."""
        formatted_subtitle = "subtitle | " + subtitle
        self.contents.insert(0, formatted_subtitle)

    def add_property(self, name: str, value: str):
        """Adds a property to the card, as the last entry in the contents list."""
        formatted_property = "property | " + name + " | " + value
        self.contents.append(formatted_property)

    def add_text(self, text: str):
        """Adds a text block to the card, as the last entry in the contents list."""
        if text.startswith("Source: "):
            self.add_property("Source", text[len("Source: "):])
            return
        formatted_text = "text | " + text
        self.contents.append(formatted_text)

    def to_json(self):
        return json.dumps(self.__dict__)

    def __init__(self, title: str, color: str, icon:str):
        super(RpgCard, self).__init__()
        self.count = 1
        self.title = title
        self.color = color
        self.icon = icon
        self.icon_back = icon
        self.contents = list([])
        self.tags = list([])
