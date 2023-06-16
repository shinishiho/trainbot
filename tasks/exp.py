from helper import load_coords, click, back, text, logger
import pytesseract

def run(image):
    x = int((400 / 1920) * image.width)
    y = int((100 / 1080) * image.height)
    image = image.crop((1, 1, x, y))
    result = pytesseract.image_to_string(image)
    logger.info(f"EXP: {result}")
    if len(result) < 7:
        buy()
    return

def buy():
    logger.info('BUY')
    coords = load_coords()
    click(coords['ItemBtn']['x'], coords['ItemBtn']['y'])
    click(80,60)
    click(80,60)
    text('wagr')
    back()
    click(coords['Buy']['x'], coords['Buy']['y'])
    click(coords['MaxSlider']['x'], coords['MaxSlider']['y'])
    click(coords['BuyBtn']['x'], coords['BuyBtn']['y'])
    click(81,850)
    click(80,60)
    click(80,60)
    text('wagr')
    back()
    click(coords['Buy']['x'], coords['Buy']['y'])
    click(coords['MaxSlider']['x'], coords['MaxSlider']['y'])
    click(coords['BuyBtn']['x'], coords['BuyBtn']['y'])
    click(coords['CloseSendTrain']['x'], coords['CloseSendTrain']['y'])