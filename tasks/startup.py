import subprocess
import time
from helper import logger, check_pixel, take_screenshot, load_coords, load_config, save_config, swipe
config = load_config()

def start():
    try:
        output = subprocess.check_output(['adb', 'version'])
    except:
        logger.critical("ADB_MISSING")
    if output.decode('utf-8').find('Android Debug Bridge') == -1:
        logger.critical("ADB_MISSING")
    else:
        logger.info("ADB_FOUND")
        connect()

def connect():
    addr = config.get('Emulator', 'address')
    port = config.get('Emulator', 'port')
    output = subprocess.check_output(['adb', 'connect', addr + ':' + port])
    if output.decode('utf-8').find('connected') == -1:
        logger.critical("CONNECTION_ERROR")
    else:
        logger.info("CONNECTION_SUCCESS")
        runapp(addr, port)

def runapp(addr, port):
    output = subprocess.check_output(['adb', '-s', addr + ':' + port, 'shell', 'am', 'start', '-n', 'air.com.pixelfederation.TrainStationGame/com.google.firebase.MessagingUnityPlayerActivity'])
    if output.decode('utf-8').find('Error') != -1:
        print('Failed to start app')
        logger.critical("STARTUP_ERROR")
    else:
        logger.info("STARTUP_SUCCESS")
    
def complete():
    coords = load_coords()
    i = 0
    while True:
        if i > 5:
            logger.critical("STARTUP_TIMEOUT")
            exit()
        screenshot = take_screenshot()
        if check_pixel(screenshot, coords["StartupComplete"]["x"], coords["StartupComplete"]["y"], coords["StartupComplete"]["color"], 0.95):
            swipe(1000, 500, 500, 500)
            config['Emulator']['width'] = str(screenshot.width)
            config['Emulator']['height'] = str(screenshot.height)
            save_config(config)
            logger.info("STARTUP_COMPLETE")
            break
        i += 1
        time.sleep(5)