from tasks import startup, state, local
from helper import logger, take_screenshot

def main():
    startup.start()
    startup.complete()
    while True:
        image = take_screenshot()
        states = state.check_state(image)
        if states["LocalTrain"] == 1:
            local.run(image)

if __name__ == '__main__':
    main()