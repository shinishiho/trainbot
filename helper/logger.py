import logging
import datetime
import json
import configparser

strings = {}
with open('data/strings.json') as f:
    strings = json.load(f)
config = configparser.ConfigParser()
config.read('config.ini')
loglevel = config.getint('UI', 'loglvl')
logger = logging.getLogger('my_logger')
logger.setLevel(loglevel)

class TranslationFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage()
        translation = strings.get(message, message)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record.msg = f"{timestamp} - {translation}"
        return super().format(record)
handler = logging.StreamHandler()
handler.setFormatter(TranslationFormatter())
logger.addHandler(handler)