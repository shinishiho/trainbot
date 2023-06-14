import configparser
import subprocess
import sys
sys.path.append('./')
from resource.logger import logger

def check_adb():
    try:
        output = subprocess.check_output(['adb', 'version'])
    except:
        logger.critical("ADB_MISSING")
        return False
    if output.decode('utf-8').find('Android Debug Bridge') == -1:
        logger.critical("ADB_MISSING")
        return False
    logger.info("ADB_FOUND")
    return True

def connect():
    config = configparser.ConfigParser()
    config.read('config.ini')
    addr = config.get('Connection', 'address')
    port = config.get('Connection', 'port')
    output = subprocess.check_output(['adb', 'connect', addr + ':' + port])
    if output.decode('utf-8').find('connected') == -1:
        logger.critical("CONNECTION_ERROR")
    else:
        logger.info("CONNECTION_SUCCESS")
        startup()

def startup():
    output = subprocess.check_output(['adb', 'shell', 'monkey', '-p', 'air.com.pixelfederation.TrainStationGame', '-c', 'android.intent.category.LAUNCHER', '1'])
    if output.decode('utf-8').find('Error') != -1:
        print('Failed to start app')
        logger.critical("STARTUP_ERROR")
    logger.info("STARTUP_SUCCESS")
    
if __name__ == '__main__':
    if check_adb():
        connect()