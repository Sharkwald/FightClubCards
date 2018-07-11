from abc import ABC
from enum import Enum

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

import jsonpickle

class ContentType(Enum):
    SubTitle = 1
    Property = 2
    Description = 3
    Text = 4
    SubSection = 5
    Boxes = 6
    DnDStats = 7
    Bullet = 8
    Picture = 9


class ContentsEntry(object):
    param_sep = " | "
    def __str__(self):
        stringified = str(self.content_type).lower()[len("contenttype."):]
        stringified += ContentsEntry.param_sep
        for param in self.params:
            stringified +=  param
            stringified += ContentsEntry.param_sep
        stringified = stringified[:-len(ContentsEntry.param_sep)]
        return stringified

    def __init__(self, content_type: ContentType, *argv):
        super(ContentsEntry, self).__init__()
        self.content_type = content_type
        self.params = argv


class RpgCard(object):

    def add_subtitle(self, subtitle: str):
        """Adds a subtitle to the card, always as the first entry in the contents list."""
        subtitle_entry = ContentsEntry(ContentType.SubTitle, subtitle)
        self.content_entries.insert(0, subtitle_entry)

    def add_property(self, name: str, value: str):
        """Adds a property to the card, as the last entry in the contents list."""
        property_entry = ContentsEntry(ContentType.Property, name, value)
        self.content_entries.append(property_entry)

    def add_text(self, text: str):
        """Adds a text block to the card, as the last entry in the contents list."""
        if text.startswith("Source: "):
            self.add_property("Source", text[len("Source: "):])
            return
        text_entry = ContentsEntry(ContentType.Text, text)
        self.content_entries.append(text_entry)

    def prep_for_json(self):
        ellipsis_character = "…"
        contents = list([])
        character_count = 0
        character_limit = 500
        for content_entry in self.content_entries:
            if content_entry.content_type == ContentType.Text:
                text = content_entry.params[0]
                new_count = character_count + len(text)
                if new_count < character_limit:
                    character_count = new_count
                    contents.append(str(content_entry))
                else:
                    space_for_new_characters = character_limit - character_count - 1
                    if space_for_new_characters > 0:
                        new_text = text[:space_for_new_characters]
                        new_text = 'text | ' + new_text + ellipsis_character
                        contents.append(new_text)
                        character_count = character_limit
            else:
                contents.append(str(content_entry))

        self.contents = contents

    def to_json(self):
        self.prep_for_json()

        return jsonpickle.encode(self, keys=True)

    def __init__(self, title: str, color: str, icon:str):
        super(RpgCard, self).__init__()
        self.count = 1
        self.title = title
        self.color = color
        self.icon = icon
        self.icon_back = icon
        self.content_entries = list([])
        self.tags = list([])
