from tasks import startup, state, local, expr
from helper import logger, take_screenshot

def main():
    startup.start()
    startup.complete()
    while True:
        image = take_screenshot()
        states = state.check_state(image)
        if states["LocalTrain"]:
            local.run(image)
        if states['Bonus']:
            local.bonus()
        if states['ExprTrain']:
            expr.run()

if __name__ == '__main__':
    main()