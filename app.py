import customtkinter as ctk
from ui.menu import Menu
from ui.carregar import Carregar
from ui.formatar_texto import Formatar_texto
from ui.check_list import Check_list

class App(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)

        self.df = None
        self.caminho = None
        self.caminho_pasta = None

        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="cols")

        self.check_list = Check_list(self)
        self.check_list.withdraw()

        self.formatar_texto = Formatar_texto(self)
        self.formatar_texto.withdraw()

        self.menu = Menu(self, self.formatar_texto, self.check_list)
        self.carregar = Carregar(self, self.menu, self)
        self.carregar.grid(row=0, column=0, columnspan=3, sticky="nsew")

    def alterar_tamanho(self, novo_tamanho):
        self.geometry(novo_tamanho)
