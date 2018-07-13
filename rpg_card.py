import re

import jsonpickle

from enum import Enum



weapon_properties = list(['ammunition', 'finesse', 'heavy', 'light', 'loading', 'range', 'reach' ,'special', 'thrown',
                          'two-handed', 'versatile'])

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
            stringified += str(param)
            stringified += ContentsEntry.param_sep
        stringified = stringified[:-len(ContentsEntry.param_sep)]
        return stringified

    def __init__(self, content_type: ContentType, *argv):
        super(ContentsEntry, self).__init__()
        self.content_type = content_type
        self.params = argv


class RpgCard(object):

    subtitle_length_limit = 35
    source_entry_prefix = "Source: "
    charges_regex = re.compile('.*has ([\d]+) charges.*')

    def add_subtitle(self, subtitle: str):
        """Appends a subtitle to the card"""
        if len(subtitle) <= RpgCard.subtitle_length_limit:
            self._add_subtitle_entry(subtitle)
            return
        else:
            self._add_multiple_subtitles(subtitle)

    def add_property(self, name: str, value: str):
        """Appends a property to the card"""
        property_entry = ContentsEntry(ContentType.Property, name, value)
        self.content_entries.append(property_entry)

    def add_description(self, text: str):
        """Appends a description block to the card"""
        if self._is_source_entry(text):
            self._add_source_entry(text)
        elif self._is_charges_entry(text):
            self._add_boxes_entry(text)
        else:
            text_entry = ContentsEntry(ContentType.Text, text)
            self.content_entries.append(text_entry)

    def _add_multiple_subtitles(self, subtitle):
        subtitle_split = subtitle.split(' ')
        subtitle = ''
        subtitle_length = 0
        split_counter = 0
        while subtitle_length <= RpgCard.subtitle_length_limit and split_counter < len(subtitle_split):
            subtitle += subtitle_split[split_counter] + ' '
            subtitle_length = len(subtitle)
            next = split_counter + 1
            if next >= len(subtitle_split):
                subtitle = subtitle.strip()
                self._add_subtitle_entry(subtitle)
            else:
                next_subtitle_length = len(subtitle + ' ' + subtitle_split[next])
                if next_subtitle_length > RpgCard.subtitle_length_limit:
                    subtitle = subtitle.strip()
                    self._add_subtitle_entry(subtitle)
                    subtitle = ''
            split_counter = next

    def _add_subtitle_entry(self, subtitle: str):
        subtitle_entry = ContentsEntry(ContentType.SubTitle, subtitle)
        self.content_entries.append(subtitle_entry)

    def _is_source_entry(self, text: str):
        return text.startswith(RpgCard.source_entry_prefix)

    def _add_source_entry(self, text: str):
        self.add_property("Source", text[len(RpgCard.source_entry_prefix):])

    def _is_charges_entry(self, text: str):
        return RpgCard.charges_regex.match(text)

    def _add_boxes_entry(self, text: str):
        charge_match = RpgCard.charges_regex.match(text)
        charges = charge_match.group(1)
        size = 1
        self.content_entries.append(ContentsEntry(ContentType.Boxes, charges, size))
        self.content_entries.append(ContentsEntry(ContentType.Text, text))

    def _prep_for_json(self):
        ellipsis_character = "…"
        contents = list([])
        character_count = 0
        character_limit = 475
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
        self._prep_for_json()
        return jsonpickle.encode(self, keys=True)

    def __init__(self, title: str, color: str, icon: str):
        super(RpgCard, self).__init__()
        self.count = 1
        self.title = title
        self.color = color
        self.icon = icon
        self.icon_back = icon
        self.content_entries = list([])
        self.contents = list([])
        self.tags = list([])
