from bs4 import BeautifulSoup

from items.potion import Potion
from items.ring import Ring
from items.rod import Rod
from items.sheild import Shield

input_file_path = 'C:\\Users\\owen.morgan-jones\\Dropbox\\5th Edition\\XML Files\\Core.xml'
output_file_path = 'C:\\Users\\owen.morgan-jones\\Desktop\\cards.json'


def _parse_items(cards, core_data):

    item_creators = list([
       {'key': '$', 'desc': 'Currency'},
       {'key': 'A', 'desc': 'Ammunition'},
       {'key': 'G', 'desc': 'General'},
       {'key': 'HA', 'desc': 'Heavy armor'},
       {'key': 'LA', 'desc': 'Light armor'},
       {'key': 'M', 'desc': 'Melee weapon'},
       {'key': 'MA', 'desc': 'Medium armor'},
       {'key': 'P', 'desc': 'Potion', "ctor": Potion.from_xml},
       {'key': 'R', 'desc': 'Ranged weapon'},
       {'key': 'RD', 'desc': 'Rod', 'ctor': Rod.from_xml},
       {'key': 'RG', 'desc': 'Ring', 'ctor': Ring.from_xml},
       {'key': 'S', 'desc': 'Shield', 'ctor': Shield.from_xml},
       {'key': 'ST', 'desc': 'Staff'},
       {'key': 'SC', 'desc': 'Scroll'},
       {'key': 'W', 'desc': 'Wondrous item'},
       {'key': 'WD', 'desc': 'Wand'}
    ])

    all_item_nodes = core_data.compendium.findAll("item")
    for item_node in all_item_nodes:
        item_type = item_node.type.text
        for item_creator in item_creators:
            if item_creator['key'] == item_type and item_creator.__contains__('ctor'):
                item = item_creator['ctor'].__call__(item_node)
                cards.append(item.to_rpg_card())

with open(input_file_path) as file:
    core_data = BeautifulSoup(file, "xml")

    cards = list([])

    _parse_items(cards, core_data)

    output = "["
    for card in cards:
        output += card.to_json() + ","

    output = output[:-1]
    output += "]"

    with open(output_file_path, 'w') as output_file:
        output_file.write(output)