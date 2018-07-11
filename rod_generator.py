from bs4 import BeautifulSoup

from rod import Rod

file_path = 'C:\\Users\\owen.morgan-jones\\Dropbox\\5th Edition\\XML Files\\Core.xml'

with open(file_path) as file:
    core_data = BeautifulSoup(file, "xml")

    all_rod_type_nodes = core_data.compendium.findAll("type", string="RD")
    all_rod_nodes = list([])
    for rod_type_node in all_rod_type_nodes:
        all_rod_nodes.append(rod_type_node.parent)

    rods = list([])

    for rod_node in all_rod_nodes:
        rod = Rod.from_xml(rod_node)
        rods.append(rod)

    cards = list([])

    for rod in rods:
        cards.append(rod.to_rpg_card())

    output = "["
    for card in cards:
        output += card.to_json() + ","

    output = output[:-1]
    output += "]"

    print(output)