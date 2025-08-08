import pandas as pd

# Carregar o JSON
df = pd.read_json("processos.json")

# Explodir a coluna data_hora_bot
df_explode = df.explode("data_hora_bot")

# Converter a coluna explodida para datetime (aqui está o ponto chave!)
df_explode["data_hora_bot"] = pd.to_datetime(df_explode["data_hora_bot"], errors="coerce")

# Definir a data alvo
data_filtro = pd.to_datetime("2025-08-01").date()

# Filtrar pela data (comparando só a parte da data)

data_hora_filtro = pd.to_datetime("2025-08-01 07:46")
data_filtro = df_explode["data_hora_bot"].dt.date == data_filtro

# Aplicar o filtro
df_filtrado = df_explode[data_filtro]

# Mostrar nomes únicos
print("Usuários com data 01/08/2025 em data_hora_bot:")
for nome in df_filtrado["nome"].unique():
    print(nome)
