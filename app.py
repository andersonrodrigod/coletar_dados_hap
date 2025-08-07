import customtkinter as ctk
from tkinter import messagebox
from loader import carregar_arquivo_json, ler_arquivo, criar_arquivo_cordenadas, salvar_dados, criar_arquivo_novo_dados, criar_arquivo_processos, criar_arquivo_dados_analitics
from check_list_func import filtrar_letras, criar_botoes_alfabeto
import pandas as pd

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



class Carregar(ctk.CTkFrame):
    def __init__(self, parent, menu, app):
        super().__init__(parent)

        self.app = app 
        self.menu = menu

        self.grid_columnconfigure(0, weight=1, minsize=330)
        self.grid_columnconfigure(1, weight=1, minsize=330)
        self.grid_columnconfigure(2, weight=1, minsize=330)

        self.label_info_inicial = ctk.CTkLabel(self, text="Carregue um arquivo para executar")
        self.label_info_inicial.grid(row=0, column=1, pady=15, padx=(0, 0))

        self.btn_carregar_arquivo = ctk.CTkButton(self, text="Carregar Arquivo", command=self.carregar_dados)
        self.btn_carregar_arquivo.grid(row=1, column=1, pady=(10, 0), padx=(10, 0))

        self.btn_novo_arquivo = ctk.CTkButton(self, text="Novo Arquivo", command=self.novo_arquivo_dados)
        self.btn_novo_arquivo.grid(row=2, column=1, pady=(10, 5), padx=(10, 0))

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
            self.grid_forget()
            self.app.alterar_tamanho("1000x700")

            self.menu.grid(row=0, column=0, columnspan=3, sticky="nsew")  
            return df,caminho, caminho_pasta
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo foi carregado corretamente.")
        return 

    def novo_arquivo_dados(self):
        criar_arquivo_novo_dados()


class Menu(ctk.CTkFrame):
    def __init__(self, parent, formatar_texto, check_list):
        super().__init__(parent)

        self.formatar_texto = formatar_texto
        self.parent = parent
        self.check_list = check_list

        self.default_size = parent.geometry()

        self.grid_columnconfigure(0, weight=1, minsize=330)
        self.grid_columnconfigure(1, weight=1, minsize=330)
        self.grid_columnconfigure(2, weight=1, minsize=330)

        self.label_menu = ctk.CTkLabel(self, text="MENU DE OPÇÕES")
        self.label_menu.grid(row=0, column=1, pady=15, padx=(1, 1))

        self.btn_formatar_texto = ctk.CTkButton(self, text="Formatar Texto", width=250, command=self.exibir_formatar_texto)
        self.btn_formatar_texto.grid(row=0, column=1, pady=(10,0), padx=(1, 1))

        self.btn_check_list = ctk.CTkButton(self, text="Check List", width=250, command=self.exibir_check_list)
        self.btn_check_list.grid(row=1, column=1, pady=(5,0), padx=(1, 1))  

    def exibir_formatar_texto(self):
        self.formatar_texto.deiconify()
        self.formatar_texto.lift()

    def exibir_check_list(self):
        self.check_list.deiconify()
        self.check_list.lift()
        print(self.parent.caminho)
        self.check_list.atualizar_interface()

class Formatar_texto(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        #self.default_size = parent.geometry()
        self.geometry("800x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

class Check_list(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        if self.parent.caminho:
            self.dados = self.carregar_dados_processos() 
        else:
            print("caminho indefinido")

        self.container = ctk.CTkFrame(self)
        self.container.pack(padx=20, pady=20)

    def carregar_dados_processos(self):
        caminho_arquivo = f"{self.parent.caminho_pasta}/processos.json"
        df = ler_arquivo(caminho_arquivo)
        dados_usuarios = df.to_dict(orient="records")
        return dados_usuarios

    def atualizar_interface(self):
        if self.parent.caminho:
            print(f"Caminho encontrado: {self.parent.caminho}")
            self.dados = self.carregar_dados_processos()

            for widget in self.container.winfo_children():
                widget.destroy()

            self.criar_botoes_alfabeto()
        else:
            print("Caminho indefinido")
            
    def criar_botoes_alfabeto(self):
        alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for idx, letra in enumerate(alfabeto):
            botao = ctk.CTkButton(
                self.container,
                text = letra,
                width=40,
                command=lambda l=letra: self.filtrar_letras(l)
            )

            botao.grid(row=0, column=idx, padx=5, pady=5)

    def filtrar_letras(self, filtro):
        df = pd.DataFrame(self.dados)

        filtro = filtro.lower()

        df_filtrado = df[df["nome"].str.lower().str.startswith(filtro)]
        
        print(df_filtrado)

if __name__ == "__main__":
    app = App("DATAFORMAT", "1000x700")
    app.mainloop()