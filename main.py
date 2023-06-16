import tkinter as tk
import customtkinter as ctk
import configparser
from helper import UI, load_config

def init():
    config = load_config()
    appearance, theme, scaling, width, height = config.get('UI', 'appearance'), config.get('UI', 'theme'), config.getfloat('UI', 'scaling'), config.getint('UI', 'width'), config.getint('UI', 'height')

    ctk.set_appearance_mode(appearance)
    ctk.set_default_color_theme(theme)
    ctk.set_widget_scaling(scaling)
    
    app=UI(width, height, scaling)
    app.mainloop()
    
def main():
    print("Starting bot...")
    return
                
if __name__ == '__main__':
    init()