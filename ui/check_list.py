import customtkinter as ctk
import pandas as pd
from utils.loader import ler_arquivo

class Check_list(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.container = ctk.CTkFrame(self)
        self.container.pack(padx=20, pady=20)

        self.grupo_frame = ctk.CTkFrame(self.container)
        self.grupo_frame.pack(pady=(0, 10))
        
        self.letras_frame = ctk.CTkFrame(self.container)
        self.letras_frame.pack(pady=(0, 10))

        self.filtros_frame = ctk.CTkFrame(self.container)
        self.filtros_frame.pack()

        self.grupo_1 = list("ABCDEFGHI")
        self.grupo_2 = list("JKLMNOPQR")
        self.grupo_3 = list("STUVWXYZ")
        self.grupo_4 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        self.grupo_atual = "GERAL"
        self.letras_do_grupo = self.grupo_4
        self.dados = [] 
        self.botoes_filtro = ["TODOS", "TELEGRAMA", "PARECER", "RETORNO", "AGUARDANDO", "PENDENTE", "PRIMEIRO CONTATO", "SEM OBSERVACAO"]

    def carregar_dados_processos(self):
        caminho_arquivo = f"{self.parent.caminho_pasta}/processos.json"
        df = ler_arquivo(caminho_arquivo)
        return df.to_dict(orient="records")

    def atualizar_interface(self):
        if self.parent.caminho:
            self.dados = self.carregar_dados_processos()

            # Limpar os frames antes de atualizar
            for widget in self.grupo_frame.winfo_children():
                widget.destroy()
            for widget in self.letras_frame.winfo_children():
                widget.destroy()

            self.criar_botoes_grupo()
            self.criar_botoes_alfabeto()
            self.criar_botoes_filtros()

    def criar_botoes_grupo(self):
        ctk.CTkButton(
            self.grupo_frame, text="Rodrigo", 
            command=lambda: self.selecionar_grupo("RODRIGO", self.grupo_1)
        ).grid(row=0, column=0, padx=5, pady=5)

        ctk.CTkButton(
            self.grupo_frame, text="Keisiane", 
            command=lambda: self.selecionar_grupo("KEISIANE", self.grupo_2)
        ).grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkButton(
            self.grupo_frame, text="Gabriel", 
            command=lambda: self.selecionar_grupo("GABRIEL", self.grupo_3)
        ).grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkButton(
            self.grupo_frame, text="Geral", 
            command=lambda: self.selecionar_grupo("GERAL", self.grupo_4)
        ).grid(row=0, column=3, padx=5, pady=5)

    def criar_botoes_alfabeto(self):
        alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for idx, letra in enumerate(alfabeto):
            botao = ctk.CTkButton(
                self.letras_frame, text=letra, width=40, 
                command=lambda l=letra: self.filtrar_letras(l)
            )
            botao.grid(row=0, column=idx, padx=2, pady=2)

    def criar_botoes_filtros(self):
        for idx, filtro in enumerate(self.botoes_filtro):
            btn = ctk.CTkButton(
                self.filtros_frame, text=filtro, 
                command=lambda f=filtro: self.filtrar_processos(f)
            )
            btn.grid(row=0, column=idx, padx=4, pady=4)

    def selecionar_grupo(self, grupo, letras):
        self.grupo_atual = grupo
        self.letras_do_grupo = letras
        self.atualizar_interface()

    def filtrar_letras(self, letra):
        df = pd.DataFrame(self.dados)
        df_filtrado = df[df["nome"].str.upper().str.startswith(letra.upper())]

        print(df_filtrado)

    def filtrar_grupo_letras(self, grupo):
        df = pd.DataFrame(self.dados)
        df_filtrados = df[df["nome"].str[0].str.upper().isin(grupo)]
        print(df_filtrados)

    def filtrar_processos(self, tipo_processo):
        df = pd.DataFrame(self.dados)

        # Filtra pelas letras do grupo, se não for o modo "GERAL"
        if self.grupo_atual != "GERAL":
            df = df[df["nome"].str[0].str.upper().isin(self.letras_do_grupo)]

        df = df[df["tipo"].str.upper().str.contains(tipo_processo.upper())]

        # Agora filtra pelo tipo de processo
        if tipo_processo != "TODOS":
            df = df[df["tipo"].str.upper().str.contains(tipo_processo.upper())]

        print(df)
