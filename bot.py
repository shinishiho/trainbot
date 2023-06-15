from tasks import startup
from resource import logger, check_pixel, take_screenshot

def main():
    startup.start()
    startup.complete()
    while True:
        image = take_screenshot()

if __name__ == '__main__':
    main()