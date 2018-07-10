import os

from bs4 import BeautifulSoup

file_path = '.\data\Core.xml'

with open(file_path) as file:
    core_data = BeautifulSoup(file, "xml")

    item_list = core_data.compendium.findAll("item")
    types_list = list([])
    for item in item_list:
        types_list.append(item.type)
    types_set = set(types_list)

    for type in types_set:
        print(type)

