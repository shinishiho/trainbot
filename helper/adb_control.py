import subprocess
import io
from PIL import Image
import configparser
from helper import logger
import time

def scaled_coords(x, y):
    config = configparser.ConfigParser()
    config.read('config.ini')
    w = config.getint('Emulator', 'width')
    h = config.getint('Emulator', 'height')
    scaled_x = int((x / 1920) * w)
    scaled_y = int((y / 1080) * h)
    return scaled_x, scaled_y

def take_screenshot():
    capture = subprocess.check_output(['adb', 'exec-out', 'screencap', '-p'])
    logger.debug("Executed screenshot command 'adb exec-out screencap -p'")
    image = Image.open(io.BytesIO(capture))
    i = 0
    while not image:
        logger.error("SCREENSHOT_ERROR")
        i += 1
        if i > 10:
            logger.critical("SCREENSHOT_RETRY_EXCEEDED")
            exit()
        capture = subprocess.check_output(['adb', 'exec-out', 'screencap', '-p'])
        logger.debug("Executed screenshot command 'adb exec-out screencap -p'")
        image = Image.open(io.BytesIO(capture))
    logger.debug("SCREENSHOT_OK")
    return image

def click(x, y):
    x, y = scaled_coords(x, y)
    subprocess.check_output(['adb', 'shell', 'input', 'touchscreen', 'tap', str(x), str(y)])
    logger.debug(f"Clicked at coordinates: {str(x)} {str(y)}")
    time.sleep(0.3)
    
def swipe(x1, y1, x2, y2):
    x1, y1 = scaled_coords(x1, y1)
    x2, y2 = scaled_coords(x2, y2)
    subprocess.check_output(['adb', 'shell', 'input', 'touchscreen', 'swipe', str(x1), str(y1), str(x2), str(y2)])
    logger.debug(f"Swiped from {str(x1)} {str(y1)} to {str(x2)} {str(y2)}")
    
def back():
    subprocess.check_output(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_BACK'])
    logger.debug("Pressed back button")
    time.sleep(0.5)
    
def text(text):
    subprocess.check_output(['adb', 'shell', 'input', 'text', text])
    logger.debug(f"Sent text '{text}'") 
    time.sleep(0.5)