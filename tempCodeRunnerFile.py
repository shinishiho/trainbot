import tkinter as tk
import customtkinter as ctk
import configparser
from resource.UI import UI

def init():
    config = configparser.ConfigParser()
    config.read('config.ini')
    address, port, appearance, theme, scaling, width, height = config.get('Connection', 'address'), config.get('Connection', 'port'), config.get('UI', 'appearance'), config.get('UI', 'theme'), config.getfloat('UI', 'scaling'), config.getint('UI', 'width'), config.getint('UI', 'height')

    ctk.set_appearance_mode(appearance)
    ctk.set_default_color_theme(theme)
    ctk.set_widget_scaling(scaling)
    
    app=UI(width, height)
    app.mainloop()
    
def main():
    return
                
if __name__ == '__main__':
    init()
    main()