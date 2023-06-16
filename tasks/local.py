import re
import time
import datetime
import pytesseract
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
        logger.debug("Metropolis time remaining OCR result: " + result)
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
# Rewrite run()
def run(image):
    resend = check_pixel(image, coords['Resend']['x'], coords['Resend']['y'], coords['Resend']['color'])
    if resend:
        if config.get('LocalTrain', 'destination') == 'Metropolis':
            click(coords['Resend']['x'], coords['Resend']['y'])
            click(coords['Resend']['x'], coords['Resend']['y'])
            logger.info('RESEND')
            time.sleep(6)
        else:
            next_metro = config.get('LocalTrain', 'next_metro')
            if datetime.datetime.now() > datetime.datetime.strptime(next_metro, "%Y-%m-%d %H:%M:%S"):
                metropolis()
            else:
                click(coords['Resend']['x'], coords['Resend']['y'])
                click(coords['Resend']['x'], coords['Resend']['y'])
                logger.info('RESEND')
                time.sleep(6)
        return
    arrvd = check_pixel(image, coords['LocalTrainArrv1']['x'], coords['LocalTrainArrv1']['y'], coords['LocalTrainArrv1']['color']) and \
        check_pixel(image, coords['LocalTrainArrv2']['x'], coords['LocalTrainArrv2']['y'], coords['LocalTrainArrv2']['color'])
    pending = check_pixel(image, coords['LocalTrainPen1']['x'], coords['LocalTrainPen1']['y'], coords['LocalTrainPen1']['color']) or \
        check_pixel(image, coords['LocalTrainPen2']['x'], coords['LocalTrainPen2']['y'], coords['LocalTrainPen2']['color'])
    if arrvd or pending:
        send()
    time.sleep(1)
