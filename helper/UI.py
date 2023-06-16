from typing import Optional, Tuple, Union
import customtkinter as ctk
import bot

class UI(ctk.CTk):
    def __init__(self, width=800, height=600, scaling=1, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        self.title('TrainStationBot')
        self.geometry('%dx%d' % (scaling*800, scaling*600))
        self.minsize(width, height)
        
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.tab_view = TabView(parent=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        # Create start button
        self.start_button = ctk.CTkButton(self, text="Start", command=main)
        
class TabView(ctk.CTkTabview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.add("Trains")
        self.add("Contracts")
        self.add("Misc")
        self.add("Settings")

        # Trains tab
        