from tasks import startup, local, popup, exp
from helper import take_screenshot, load_coords, check_pixel, click
import asyncio

states = {
    "Popup": 0,
    "LocalTrain": 0,
    "ExprTrain": 0,
    'IT': 0,
    'Bonus': 0
}
coords = load_coords()

def check_state(image, state):
    states[state] = check_pixel(image, coords[state]['x'], coords[state]['y'], coords[state]['color'])
    return states[state]

async def locl(image):
    if check_state(image, 'LocalTrain'):
        local.run(image)
        
async def bonus(image):
    if check_state(image, 'Bonus'):
        click(coords['Bonus']['x'], coords['Bonus']['y'])

async def close_popup(image):
    if check_state(image, 'Popup'):
        popup.run(image)
        
async def buy(image):
    exp.run(image)
    
async def stuck(image):
    if check_pixel(image, 1, 1, (0, 0, 0)):
        await asyncio.sleep(10)
        image = take_screenshot()
        if check_pixel(image, 1, 1, (0, 0, 0)):
            startup.quit()
            startup.runapp()

async def main():
    startup.start()
    startup.complete()
    while True:
        image = take_screenshot()
        await asyncio.gather(locl(image), bonus(image), close_popup(image), buy(image), stuck(image))
        
if __name__ == '__main__':
    asyncio.run(main())