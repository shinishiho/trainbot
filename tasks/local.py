import cv2
import numpy as np
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
    screen = take_screenshot()
    
    metro = 'Closed'
    for state in ['Open', 'Video']:
        r = check_pixel(screen, coords[f"Metropolis{state}"]['x'], coords[f"Metropolis{state}"]['y'], coords[f"Metropolis{state}"]['color'])
        if r:
            metro = state
    
    if metro == 'Video':
        click(coords['MetropolisVideo']['x'], coords['MetropolisVideo']['y'])
        logger.info('METROPOLIS_VIDEO')
        if config.getboolean('LocalTrain', 'metropolis_ad'):     
            watch_ad.run()
        else:
            metro = 'Closed'
    if metro == 'Closed':
        return
    config.set('LocalTrain', 'destination', 'Metropolis')
    logger.info('METROPOLIS_OPEN')
    save_config(config)

def local_state(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    arrvd = cv2.imread('template/arrvd.png', cv2.IMREAD_GRAYSCALE)
    arrv = cv2.imread('template/arrv.png', cv2.IMREAD_GRAYSCALE)
    pending = cv2.imread('template/pending.png', cv2.IMREAD_GRAYSCALE)
    
    arrvd = cv2.matchTemplate(image, arrvd, cv2.TM_CCOEFF_NORMED)
    arrv = cv2.matchTemplate(image, arrv, cv2.TM_CCOEFF_NORMED)
    pending = cv2.matchTemplate(image, pending, cv2.TM_CCOEFF_NORMED)
    
    r = {
        'arrvd': cv2.minMaxLoc(arrvd)[1],
        'arrv': cv2.minMaxLoc(arrv)[1],
        'pending': cv2.minMaxLoc(pending)[1]
    }
    return max(r, key=r.get)
    
def run(image):
    state = local_state(image)
    if state == 'arrv':
        return
    
    resend = check_pixel(image, coords['Resend']['x'], coords['Resend']['y'], coords['Resend']['color'])
    if resend and config.get('LocalTrain', 'destination') == 'Metropolis':
        click(coords['Resend']['x'], coords['Resend']['y'])
        logger.info('RESEND')
    metropolis(resend)
    if config.get('LocalTrain', 'destination') != 'Metropolis':
        click(coords['Resend']['x'], coords['Resend']['y'])
        logger.info('RESEND')
    
    # Send dest
        