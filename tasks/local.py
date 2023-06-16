import cv2
import numpy as np
from helper import check_pixel, load_coords


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
    coords = load_coords()
    resend = check_pixel(image, coords['Resend']['x'], coords['Resend']['y'], coords['Resend']['color'])