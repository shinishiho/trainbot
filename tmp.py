import threading
import subprocess
from PIL import Image
import io
import time

# Function to capture the screen using adb and return the image object
def capture_screen():
    # Use adb to capture the screen and get the stdout output
    output = subprocess.check_output(['adb', 'exec-out', 'screencap', '-p'])

    # Convert the stdout output to an image object
    image = Image.open(io.BytesIO(output))
    return image

# Function to get scaled coordinates based on a reference screen size
def get_scaled_coordinates(x, y, reference_width, reference_height, actual_width, actual_height):
    scaled_x = int((x / reference_width) * actual_width)
    scaled_y = int((y / reference_height) * actual_height)
    return scaled_x, scaled_y

# Function to get pixel color at coordinates
def get_pixel_color(image, x, y):
    # Get the pixel color at the given coordinates from the captured image
    pixel_color = image.getpixel((x, y))
    return pixel_color

# Function to periodically check the pixel color
def check_pixel_color(x_coord, y_coord):
    reference_width = 1920
    reference_height = 1080

    while True:
        # Capture the screen
        image = capture_screen()

        # Get the actual screen size from the captured image
        actual_width, actual_height = image.size

        # Calculate the scaled coordinates
        scaled_x, scaled_y = get_scaled_coordinates(x_coord, y_coord, reference_width, reference_height, actual_width, actual_height)

        # Get the pixel color at the scaled coordinates
        color = get_pixel_color(image, scaled_x, scaled_y)

        # Print the RGB values of the pixel color
        print("Pixel color at ({}, {}): RGB({})".format(scaled_x, scaled_y, color))

        time.sleep(5)  # Wait for 5 seconds before checking again

# Start the pixel color checking thread
pixel_check_thread = threading.Thread(target=check_pixel_color)
pixel_check_thread.start()