import json
import configparser
import logging

def load_strings(json_file):
    with open(json_file, 'r') as file:
        strings = json.load(file)
    return strings
strings = load_strings('data/strings.json')

config = configparser.ConfigParser()
config.read('config.ini')
loglevel = config.getint('UI', 'loglvl')
logger = logging.getLogger('my_logger')
logger.setLevel(loglevel)

class TranslationFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage()
        translation = strings.get(message, message)
        record.msg = translation
        return super().format(record)
handler = logging.StreamHandler()
handler.setFormatter(TranslationFormatter())
logger.addHandler(handler)