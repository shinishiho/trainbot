from helper import logger, check_pixel, load_coords

coords = load_coords()
states = {
    "LocalTrain": 0,
    "ExprTrain": 0,
    'IT': 0,
    'Bonus': 0
}

def check_state(image):
    for state in states:
        states[state] = check_pixel(image, coords[state]['x'], coords[state]['y'], coords[state]['color'])
        logger.info(f"{state}: {states[state]}")
    return states