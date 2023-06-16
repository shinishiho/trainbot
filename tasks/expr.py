from helper import click, take_screenshot, check_pixel, load_coords
import time
coords = load_coords()

def whistle():
    pass

def run():
    click(coords['ExprTrain']['x'], coords['ExprTrain']['y'])
    
