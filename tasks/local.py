import re
import time
import datetime
import pytesseract
import cv2
import numpy as np
from helper import logger, check_pixel, load_coords, load_config, save_config, click, swipe, take_screenshot, back

config = load_config()
coords = load_coords()
def metropolis():
    click(coords['TrainBtn']['x'], coords['TrainBtn']['y'])
    swipe(500, 250, 500, 750)
    click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
    click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
    screen = take_screenshot()
    metro = 'Closed'
    for state in ['Open', 'Video']:
        r = check_pixel(screen, coords[f"Metropolis{state}"]['x'], coords[f"Metropolis{state}"]['y'], coords[f"Metropolis{state}"]['color'])
        if r:
            metro = state
    if metro == 'Video':
        logger.info('METROPOLIS_VIDEO')
        if config.getboolean('LocalTrain', 'metro_ad'):
            click(coords['MetropolisVideo']['x'], coords['MetropolisVideo']['y'])
            logger.info('WATCH_AD')
            time.sleep(45)
            logger.info('AD_COMPLETE')
            back()
        else:
            metro = 'Closed'
    click(coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'])
    click(coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'])
    if metro == 'Closed':
        x1, y1 = int((670 / 1920) * screen.width), int((460 / 1920) * screen.width)
        x2, y2 = int((1000 / 1080) * screen.height), int((500 / 1080) * screen.height)
        image = screen.crop((x1, y1, x2, y2))
        result = pytesseract.image_to_string(image)
        logger.info("Metropolis refresh time: " + result)
        match = re.search(r'(\d+)h (\d+)m', result)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            now = datetime.datetime.now()
            config.set('LocalTrain', 'next_metro', (now + datetime.timedelta(hours=hours, minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S"))
        return
    config.set('LocalTrain', 'destination', 'Metropolis')
    logger.info('METROPOLIS_OPEN')
    save_config(config)

def send():
    click(coords['TrainBtn']['x'], coords['TrainBtn']['y'])
    click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
    click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
    complete = False
    i = 0
    while not complete:
        if config.get('LocalTrain', 'destination') == 'Metropolis':
            click(coords['MetropolisOpen']['x'], coords['MetropolisOpen']['y'])
        else:
            click(coords['5min']['x'], coords['5min']['y'])
        while True:
            screen = take_screenshot()
            if check_pixel(screen, coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'], coords['SendTrainBtn']['color']):
                click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
                click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
                break
            if check_pixel(screen, coords['SendTrainComplete']['x'], coords['SendTrainComplete']['y'], coords['SendTrainComplete']['color']):
                click(coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'])
                complete = True
                break
            if i > 10:
                click(coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'])
                complete = True
                break
            i += 1
            time.sleep(1)  

def run(image):
    if config.get('LocalTrain', 'destination') == 'Metropolis':
        img = np.array(image)
        template = cv2.imread('template/resend.png')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        logger.debug('OpenCV matchTemplate result: confidence ' + str(max_val))
        if max_val > 0.9:
            click(coords['Resend']['x'], coords['Resend']['y'])
            click(coords['Resend']['x'], coords['Resend']['y'])
            logger.info('RESEND')
            time.sleep(6)
        else:
            metropolis()
        return
    else:
        next_metro = datetime.datetime.strptime(config.get('LocalTrain', 'next_metro'), "%Y-%m-%d %H:%M:%S")
        if datetime.datetime.now() < next_metro:
            click(coords['Resend']['x'], coords['Resend']['y'])
            click(coords['Resend']['x'], coords['Resend']['y'])
            logger.info('RESEND')
        else:
            metropolis()
        return
