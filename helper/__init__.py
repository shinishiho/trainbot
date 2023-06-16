import sys
sys.path.append('./')
from helper.logger import logger
from helper.check_pixel import check_pixel
from helper.adb_control import take_screenshot, click, swipe
from helper.data_loader import load_strings, load_coords, load_config, save_config