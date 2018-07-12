from bs4 import BeautifulSoup

from rod import Rod
from ring import Ring

input_file_path = 'C:\\Users\\owen.morgan-jones\\Dropbox\\5th Edition\\XML Files\\Core.xml'
output_file_path = 'C:\\Users\\owen.morgan-jones\\Desktop\\cards.json'


def _parse_rods(cards, core_data):
    all_rod_type_nodes = core_data.compendium.findAll("type", string="RD")
    all_rod_nodes = list([])
    for rod_type_node in all_rod_type_nodes:
        all_rod_nodes.append(rod_type_node.parent)
    rods = list([])
    for rod_node in all_rod_nodes:
        rod = Rod.from_xml(rod_node)
        rods.append(rod)
    for rod in rods:
        cards.append(rod.to_rpg_card())
        
def _parse_rings(cards, core_data):
    all_ring_type_nodes = core_data.compendium.findAll("type", string="RG")
    all_ring_nodes = list([])
    for ring_type_node in all_ring_type_nodes:
        all_ring_nodes.append(ring_type_node.parent)
    rings = list([])
    for ring_node in all_ring_nodes:
        ring = Ring.from_xml(ring_node)
        rings.append(ring)
    for ring in rings:
        cards.append(ring.to_rpg_card())

with open(input_file_path) as file:
    core_data = BeautifulSoup(file, "xml")

    cards = list([])

    _parse_rods(cards, core_data)
    _parse_rings(cards, core_data)

    output = "["
    for card in cards:
        output += card.to_json() + ","

    output = output[:-1]
    output += "]"

    with open(output_file_path, 'w') as output_file:
        output_file.write(output)