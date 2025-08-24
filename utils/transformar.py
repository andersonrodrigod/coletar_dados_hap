import pandas as pd
from pathlib import Path
from datetime import datetime
import json




bruto_path = Path("dados_coletados.json")
hist_path  = Path("dados_historico.json")

# Carrega os dados brutos
df_bruto = pd.read_json(bruto_path)
df_bruto["data_hora_bot"] = pd.to_datetime(df_bruto["data_hora_bot"], dayfirst=True)

# Carrega histórico
if hist_path.exists() and hist_path.stat().st_size > 0:
    df_hist = pd.read_json(hist_path)
else:
    df_hist = pd.DataFrame(columns=df_bruto.columns)

# Filtra pela data desejada
data_escolhida = "24/08/2025"
data_obj = datetime.strptime(data_escolhida, "%d/%m/%Y").date()
df_selecionado = df_bruto[df_bruto["data_hora_bot"].dt.date == data_obj]

# Converte apenas colunas de texto (sem data)
for col in ["codigo", "nome", "codigo_procedimento", "nome_procedimento", "info_assistente", "info_medico", "medico_solicitante"]:
    if col in df_selecionado:
        df_selecionado[col] = df_selecionado[col].astype(str)
    if col in df_hist.columns:
        df_hist[col] = df_hist[col].astype(str)

# Atualiza histórico
for idx, row in df_selecionado.iterrows():
    codigo = row["codigo"]

    df_hist_codigo = df_hist[df_hist["codigo"] == codigo]

    info_bruto = str(row["info_assistente"])

    if df_hist_codigo.empty:
        df_hist = pd.concat([df_hist, pd.DataFrame([row]).copy()], ignore_index=True)
    else:
        ultimo_hist = df_hist_codigo.iloc[-1]

        ultimo_hist = df_hist_codigo.iloc[-1]
        info_hist = str(ultimo_hist["info_assistente"])

        if info_bruto.startswith(info_hist) and info_bruto != info_hist:
            df_hist = pd.concat([df_hist, pd.DataFrame([row]).copy()], ignore_index=True)

# Converte datas para datetime de forma segura
df_hist["data_hora_bot"] = pd.to_datetime(df_hist["data_hora_bot"], dayfirst=True)
# Formata datas para string no padrão desejado
df_hist["data_hora_bot"] = df_hist["data_hora_bot"].dt.strftime("%d/%m/%Y %H:%M")

dados = df_hist.to_dict(orient="records")
with open("dados_historico.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)

with open("dados_historico.json", "r", encoding="utf-8") as f:
    dados_lidos = json.load(f)

print(dados_lidos[0]["info_assistente"])



#df.to_excel("dados.xlsx")
