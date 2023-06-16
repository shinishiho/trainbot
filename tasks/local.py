import time
from helper import logger, check_pixel, load_coords, load_config, save_config, click, swipe, take_screenshot
from tasks import watch_ad

config = load_config()
coords = load_coords()
def metropolis(resend):
    if not resend:
        config.set('LocalTrain', 'destination', config.get('LocalTrain', 'def_dest'))
        logger.info('METROPOLIS_CLOSED')
        save_config(config)
        return
    
    click(coords['TrainBtn']['x'], coords['TrainBtn']['y'])
    swipe(500, 250, 500, 750)
    click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
    screen = take_screenshot()
    if check_pixel(screen, coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'], coords['SendTrainBtn']['color']):
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
            watch_ad.run()
        else:
            metro = 'Closed'
    if metro == 'Closed':
        return
    config.set('LocalTrain', 'destination', 'Metropolis')
    logger.info('METROPOLIS_OPEN')
    save_config(config)

def send():
    screen = take_screenshot()
    if not check_pixel(screen, coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'], coords['CloseTrainSend']['color'], 0.99):
        click(coords['TrainBtn']['x'], coords['TrainBtn']['y'])
        click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
        click(coords['SendTrainBtn']['x'], coords['SendTrainBtn']['y'])
    complete = False
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
            time.sleep(1)

def local_state(image):
    if check_pixel(image, coords['LocalTrainPen1']['x'], coords['LocalTrainPen1']['y'], coords['LocalTrainPen1']['color']) or \
        check_pixel(image, coords['LocalTrainPen2']['x'], coords['LocalTrainPen2']['y'], coords['LocalTrainPen2']['color']):
        return 'pending'
    if check_pixel(image, coords['LocalTrainArrv1']['x'], coords['LocalTrainArrv1']['y'], coords['LocalTrainArrv1']['color']) or \
        check_pixel(image, coords['LocalTrainArrv2']['x'], coords['LocalTrainArrv2']['y'], coords['LocalTrainArrv2']['color']):
        return 'arrv'
    if check_pixel(image, coords['LocalTrainArrvd']['x'], coords['LocalTrainArrvd']['y'], coords['LocalTrainArrvd']['color']):
        return 'arrvd'

def run(image):
    state = local_state(image)
    if state == 'arrv':
        return
    resend = check_pixel(image, coords['Resend']['x'], coords['Resend']['y'], coords['Resend']['color'])
    if resend and config.get('LocalTrain', 'destination') == 'Metropolis':
        click(coords['Resend']['x'], coords['Resend']['y'])
        click(coords['Resend']['x'], coords['Resend']['y'])
        logger.info('RESEND')
        return
    metropolis(resend)
    if resend and config.get('LocalTrain', 'destination') != 'Metropolis':
        click(coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'])
        click(coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'])
        click(coords['Resend']['x'], coords['Resend']['y'])
        click(coords['Resend']['x'], coords['Resend']['y'])
        logger.info('RESEND')
        return
    send()

def bonus():
    click(coords['Bonus']['x'], coords['Bonus']['y'])