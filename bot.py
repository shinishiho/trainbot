from tasks import startup, state, local, popup, exp
from helper import take_screenshot, load_coords, check_pixel
import asyncio

states = {
    "Popup": 0,
    "LocalTrain": 0,
    "ExprTrain": 0,
    'IT': 0,
    'Bonus': 0
}
def check_state(image, state):
    coords = load_coords()
    states[state] = check_pixel(image, coords[state]['x'], coords[state]['y'], coords[state]['color'])

async def locl(image):
    if state.check_state(image, 'LocalTrain'):
        local.run(image)
        exp.run(image)
        
async def bonus(image):
    if state.check_state(image, 'Bonus'):
        local.bonus()

async def popup(image):
    if state.check_state(image, 'Popup'):
        popup.run(image)

async def main():
    startup.start()
    startup.complete()
    while True:
        image = take_screenshot()
        await asyncio.gather(locl(image), bonus(image), popup(image))
        
if __name__ == '__main__':
    asyncio.run(main())