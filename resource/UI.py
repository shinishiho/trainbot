from typing import Optional, Tuple, Union
import customtkinter as ctk

class UI(ctk.CTk):
    def __init__(self, width=800, height=600, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        self.title('TrainStationBot')
        self.geometry('%dx%d' % (width, height))
        