import cv2
import numpy as np
from helper import logger, click

def run(image):
    img = np.array(image)
    template = cv2.imread('template/collect.png')
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    logger.debug('OpenCV matchTemplate result: confidence ' + str(max_val))
    if max_val > 0.9:
        w, h = template.shape[::-1]
        center = (max_loc[0] + w / 2, max_loc[1] + h / 2)
        click(center[0], center[1])