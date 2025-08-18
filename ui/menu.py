import customtkinter as ctk
from utils.coletar_dados import save_data, save_info_assistente, copy_vazio
from tkinter import messagebox
import time

class Menu(ctk.CTkFrame):
    def __init__(self, parent, formatar_texto, check_list, copiador_texto):
        super().__init__(parent)
        self.parent = parent
        self.formatar_texto = formatar_texto
        self.check_list = check_list
        self.copiador_texto = copiador_texto

        
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.label_menu = ctk.CTkLabel(self, text="MENU DE OPÇÕES")
        self.label_menu.grid(row=0, column=1, pady=8)

        self.btn_formatar_texto = ctk.CTkButton(self, text="Formatar Texto", width=250, command=self.exibir_formatar_texto)
        self.btn_formatar_texto.grid(row=1, column=1, pady=(10,0))

        self.btn_check_list = ctk.CTkButton(self, text="Check List", width=250, command=self.exibir_check_list)
        self.btn_check_list.grid(row=2, column=1, pady=(5,0))

        self.btn_coletar_dados = ctk.CTkButton(self, text="Coletar Dados", command=lambda: self.quantidade_coletar_dados("dados"), width=250)
        self.btn_coletar_dados.grid(row=3, column=1, pady=(5, 0))

        self.btn_coletar_dados_info_assistente = ctk.CTkButton(self, text="Coletar Info Assistente", command=lambda: self.quantidade_coletar_dados("assistente"), width=250)
        self.btn_coletar_dados_info_assistente.grid(row=4, column=1, pady=(5, 0))

        self.btn_copiador_texto = ctk.CTkButton(self, text="Copiador Texto", width=250, command=self.exibir_copiador_texto)
        self.btn_copiador_texto.grid(row=5, column=1, pady=(5, 10))

    def exibir_copiador_texto(self):
        self.copiador_texto.deiconify()
        self.copiador_texto.lift()
        self.copiador_texto._load_entries()

    def exibir_formatar_texto(self):
        self.formatar_texto.deiconify()
        self.formatar_texto.lift()

    def exibir_check_list(self):
        self.check_list.deiconify()
        self.check_list.lift()
        self.check_list.atualizar_interface()

    def quantidade_coletar_dados(self, tipo):
        dialog = ctk.CTkInputDialog(title="Número de Coletas", text="Digite o número de coletas")
        try:
            quantidade_str = dialog.get_input()
            if quantidade_str is None or quantidade_str.strip() == "":
                raise ValueError("Nenhum valor foi inserido")

            quantidade = int(quantidade_str)

            if quantidade <= 0:
                raise ValueError("O número deve ser maior que zero")
            
            if tipo == "dados": 
                self.coletar_dados(quantidade)
            elif tipo == "assistente":
                self.coletar_info_assistente(quantidade)

        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")


    def coletar_dados(self, quantidade):
        cordenada = f"{self.parent.caminho_pasta}/cordenadas.json"
        try:
            caminho = self.parent.caminho
            copy_vazio()
            for i in range(quantidade):
                dados = save_data(caminho, cordenada)

        except Exception as e:
            print(f"Erro em coletar_dados: {e}")

    def coletar_info_assistente(self, quantidade):
        caminho_coletar_dados = self.parent.caminho
        cordenada = f'{self.parent.caminho_pasta}/cordenadas.json'
        caminho_arquivo = f'{self.parent.caminho_pasta}/processos.json'
        try:
            time.sleep(2)
            for i in range(quantidade):
                dados = save_info_assistente(caminho_arquivo, cordenada, caminho_coletar_dados)
            
        except Exception as e:
            print(f"Erro em coletar_dados: {e}")