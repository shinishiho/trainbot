from helper import logger

def scaled_coords(x, y, width, height):
    scaled_x = int((x / 1920) * width)
    scaled_y = int((y / 1080) * height)
    return scaled_x, scaled_y

def check_pixel(image, x, y, color, threshold=0.9):
    coord_x, coord_y = scaled_coords(x, y, image.width, image.height)
    pixel = image.getpixel((coord_x, coord_y))
    r = 1 - abs(pixel[0] - color[0])/255
    g = 1 - abs(pixel[1] - color[1])/255
    b = 1 - abs(pixel[2] - color[2])/255
    logger.debug("Pixel at " + str(coord_x) + ", " + str(coord_y) + " is " + str(pixel) + " with a similarity of " + str(r) + ", " + str(g) + ", " + str(b))
    if r > threshold and g > threshold and b > threshold:
        logger.debug("Threshold met")
        return True
    return False