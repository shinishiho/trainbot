import logging
import datetime
from helper import load_strings, load_config

strings = load_strings()
config = load_config()
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