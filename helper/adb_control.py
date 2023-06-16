import subprocess
import io
from PIL import Image
from helper import logger

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
    subprocess.check_output(['adb', 'shell', 'input', 'touchscreen', 'tap', str(x), str(y)])
    logger.debug(f"Executed click command 'adb shell input touchsreen tap {str(x)} {str(y)}'")
    
def swipe(x1, y1, x2, y2):
    subprocess.check_output(['adb', 'shell', 'input', 'touchscreen', 'swipe', str(x1), str(y1), str(x2), str(y2)])
    logger.debug(f"Executed swipe command 'adb shell input touchscreen swipe {str(x1)} {str(y1)} {str(x2)} {str(y2)}'")