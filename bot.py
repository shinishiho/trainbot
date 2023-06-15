from tasks import startup
import subprocess
from PIL import Image
import io
import sys
sys.path.append('./')
from resource.logger import logger

def main():
    startup.start()
    startup.complete()
    while True:
        capture = subprocess.check_output(['adb', 'exec-out', 'screencap', '-p'])
        image = Image.open(io.BytesIO(capture))
        i = 0
        while not image:
            logger.error("SCREENSHOT_ERROR")
            i += 1
            if i > 10:
                logger.critical("SCREENSHOT_RETRY_EXCEEDED")
                exit()
            capture = subprocess.check_output(['adb', 'exec-out', 'screencap', '-p'])
            image = Image.open(io.BytesIO(capture))
        logger.debug("SCREENSHOT_OK")

if __name__ == '__main__':
    main()