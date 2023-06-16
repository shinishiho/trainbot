import json
import configparser

def load_coords():
    coords = {}
    with open('data/coords.json') as f:
        coords = json.load(f)
    return coords

def load_strings():
    strings = {}
    with open('data/strings.json') as f:
        strings = json.load(f)
    return strings

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config