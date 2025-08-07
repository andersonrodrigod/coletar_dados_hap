import customtkinter as ctk

class Formatar_texto(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("800x500")
        self.grid_columnconfigure((0, 1, 2), weight=1)
