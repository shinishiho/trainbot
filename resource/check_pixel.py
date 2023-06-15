from resource import logger

def scaled_coords(x, y, reference_width, reference_height, actual_width, actual_height):
    scaled_x = int((x / reference_width) * actual_width)
    scaled_y = int((y / reference_height) * actual_height)
    return scaled_x, scaled_y

def check_pixel(image, x, y, color, threshold=0.9):
    coord_x, coord_y = scaled_coords(x, y, 1920, 1080, image.width, image.height)
    pixel = image.getpixel((coord_x, coord_y))
    r = 1 - abs(pixel[0] - color[0])/255
    g = 1 - abs(pixel[1] - color[1])/255
    b = 1 - abs(pixel[2] - color[2])/255
    logger.debug("Pixel at " + str(coord_x) + ", " + str(coord_y) + " is " + str(pixel) + " with a similarity of " + str(r) + ", " + str(g) + ", " + str(b))
    if r > threshold and g > threshold and b > threshold:
        logger.debug("Threshold met")
        return True
    return False