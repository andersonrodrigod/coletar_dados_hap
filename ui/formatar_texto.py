import customtkinter as ctk
from utils.palavras import substituicoes

class Formatar_texto(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Formatar Texto")
        self.geometry("600x330")
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.text_area = ctk.CTkTextbox(self, width=550, height=250)
        self.text_area.pack(pady=20)

        # Botão
        self.btn_transformar = ctk.CTkButton(self, text="Transformar Texto", command=self.aplicar_substituicoes)
        self.btn_transformar.pack()

    def aplicar_substituicoes(self):
        texto = self.text_area.get("1.0", "end-1c")  # pega todo o texto do textarea
        for antigo, novo in substituicoes.items():
            texto = texto.replace(antigo, novo)
        self.text_area.delete("1.0", "end")  # limpa
        self.text_area.insert("1.0", texto)  # insere de volta