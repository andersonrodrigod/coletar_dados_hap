import customtkinter as ctk
from tkinter import messagebox
from utils.loader import carregar_arquivo_json, criar_arquivo_cordenadas, criar_arquivo_processos, criar_arquivo_novo_dados, criar_arquivo_dados_analitics, criar_arquivo_copiador


class Carregar(ctk.CTkFrame):
    def __init__(self, parent, menu, app):
        super().__init__(parent)
        self.app = app 
        self.menu = menu

        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.label_info_inicial = ctk.CTkLabel(self, text="Carregue um arquivo para executar")
        self.label_info_inicial.grid(row=0, column=1, pady=8)

        self.btn_carregar_arquivo = ctk.CTkButton(self, text="Carregar Arquivo", command=self.carregar_dados)
        self.btn_carregar_arquivo.grid(row=1, column=1, pady=(10, 0))

        self.btn_novo_arquivo = ctk.CTkButton(self, text="Novo Arquivo", command=self.novo_arquivo_dados)
        self.btn_novo_arquivo.grid(row=2, column=1, pady=(5, 10))

    def carregar_dados(self):
        resultado = carregar_arquivo_json()
        if resultado:
            df, caminho, caminho_pasta = resultado
            self.app.df = df
            self.app.caminho = caminho
            self.app.caminho_pasta = caminho_pasta
            criar_arquivo_dados_analitics(caminho_pasta)
            criar_arquivo_cordenadas(caminho_pasta)
            criar_arquivo_processos(caminho_pasta)
            criar_arquivo_copiador(caminho_pasta)
            self.grid_forget()
            self.app.alterar_tamanho("300x230")
            self.menu.grid(row=0, column=0, columnspan=3, sticky="nsew")
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo foi carregado corretamente.")

    def novo_arquivo_dados(self):
        criar_arquivo_novo_dados()
