import tkinter as tk
import customtkinter as ctk
import configparser
from resource.UI import UI

def init():
    config = configparser.ConfigParser()
    config.read('config.ini')
    ctk.set_appearance_mode(config.get('UI', 'appearance'))
    ctk.set_default_color_theme(config.get('UI', 'theme'))  
    
    app=UI(config.getint('UI', 'width'), config.getint('UI', 'height'))
    app.mainloop()
    
def main():
    return
                
if __name__ == '__main__':
    init()
    main()