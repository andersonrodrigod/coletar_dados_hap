import pandas as pd
from datetime import datetime
from loader import ler_arquivo
import customtkinter as ctk


df = pd.read_json("processos.json")



def filtrar_letras(dados, filtro):

    df = pd.DataFrame(dados)

    filtro = filtro.lower()


    df_filtrado = df[df["nome"].str.lower().str.startswith(filtro)]
    
    return df_filtrado

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




filtro = "A"

resultado = filtrar_letras(df, filtro)

# command=lambda l=letra: self.filtrar_letras(l)

#print(resultado)




