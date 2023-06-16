from helper import load_coords, click, back, text, logger
import pytesseract
import time

def run(image):
    x1, y1 = int((125 / 1920) * image.width), int((25 / 1920) * image.width)
    x2, y2 = int((330 / 1080) * image.height), int((75 / 1080) * image.height)
    image = image.crop((x1, y1, x2, y2))
    result = pytesseract.image_to_string(image)
    if len(result) < 7:
        buy()
    return

def buy():
    logger.info('BUY')
    coords = load_coords()
    click(coords['ItemBtn']['x'], coords['ItemBtn']['y'])
    click(80,60)
    click(80,60)
    time.sleep(0.5)
    text('wagr')
    back()
    click(coords['Buy']['x'], coords['Buy']['y'])
    click(coords['MaxSlider']['x'], coords['MaxSlider']['y'])
    click(coords['BuyBtn']['x'], coords['BuyBtn']['y'])
    click(81,850)
    click(80,60)
    click(80,60)
    time.sleep(0.5)
    text('wagr')
    back()
    click(coords['Buy']['x'], coords['Buy']['y'])
    click(coords['MaxSlider']['x'], coords['MaxSlider']['y'])
    click(coords['BuyBtn']['x'], coords['BuyBtn']['y'])
    click(coords['CloseTrainSend']['x'], coords['CloseTrainSend']['y'])
    return