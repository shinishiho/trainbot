import subprocess
import io
from PIL import Image
from resource import logger

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