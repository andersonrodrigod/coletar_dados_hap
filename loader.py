import pandas as pd
from tkinter import filedialog, messagebox
from palavras import cordenadas
import os
import json






def criar_arquivo_novo_dados():
    caminho_pasta = filedialog.askdirectory()

    if not caminho_pasta:
        print("operação cancelada")
        return

    if os.path.exists(caminho_pasta + "/dados_coletados.json"):
        messagebox.showinfo("ATENÇÃO", "Já existe um arquivo de dados_coletados na pasta, carregue o arquivo de dados_coletados para continuar")

    else:
        df = pd.DataFrame()
        df.to_json("dados_coletados.json", orient="records", indent=4)
        messagebox.showinfo("Sucesso", "Arquivo criado com sucesso, carregue o arquivo criado de dados_coletadoas para continuar")

def criar_arquivo_dados_analitics(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/dados_analitics.json"):
        df = pd.DataFrame()
        df.to_json("dados_analitics.json", orient="records", indent=4)
        print("arquivo criado com sucesso")

def criar_arquivo_cordenadas(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/cordenadas.json"):
        df = pd.DataFrame([cordenadas])
        df.to_json("cordenadas.json", orient="records", indent=4)
        print("arquivo criado com sucesso")

def criar_arquivo_processos(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/processos.json"):
        df = pd.DataFrame()
        df.to_json("processos.json", orient="records", indent=4)
        print("arquivo criado com sucesso")

def ler_arquivo(arquivo):
    return pd.read_json(arquivo)

def carregar_dados_existentes(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_existentes = json.load(f)
        return dados_existentes

def salvar_dados(dados, caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(dados)

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    messagebox.showinfo("Sucesso", "Erro enviado com sucesso")


def carregar_arquivo_json(caminho_arquivo=None):
    messagebox.showinfo("ATENÇÃO", "Selecione o arquivo JSON dados_coletados")
    if not caminho_arquivo:
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo JSON dados_coletados",
            filetypes=[("Arquivos JSON", "*.json")]
        )

    if caminho_arquivo:

        caminho_pasta = os.path.dirname(caminho_arquivo)
        try:
            df = pd.read_json(caminho_arquivo)
            messagebox.showinfo("Sucesso", "Arquivo JSON carregado com sucesso")
            if df is not None:
                return df, caminho_arquivo, caminho_pasta
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo JSON:\n{e}")
        except Exception as e:
            messagebox.showerror("Erro", "invesperado: \n{e}")
            
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado")

        return None
    
