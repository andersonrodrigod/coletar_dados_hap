import customtkinter as ctk
import pandas as pd
from utils.loader import ler_arquivo, editar_dados_teste
import tkinter as tk
from datetime import datetime
from functools import partial
from datetime import datetime, timedelta

class Check_list(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("1230x800")
        self.container = ctk.CTkFrame(self)
        self.container.pack(padx=20, pady=20)

        self.grupo_frame = ctk.CTkFrame(self.container)
        self.grupo_frame.pack(pady=(0, 10))
        
        self.letras_frame = ctk.CTkFrame(self.container)
        self.letras_frame.pack(pady=(0, 10))

        self.filtros_frame = ctk.CTkFrame(self.container)
        self.filtros_frame.pack()
        
        self.processos_frame = ctk.CTkScrollableFrame(self.container, width=1200, height=500)
        self.processos_frame.pack(fill="both", expand=True, pady=10)
        
        # Novo frame para os controles inferiores
        self.controles_frame = ctk.CTkFrame(self.container)
        self.controles_frame.pack(fill="x", pady=(10, 0))
        
        # Frame para os botões de data/hora
        self.data_hora_frame = ctk.CTkFrame(self.controles_frame)
        self.data_hora_frame.pack(side="left", padx=10, pady=5)
        
        # Campo de entrada para data
        self.data_label = ctk.CTkLabel(self.data_hora_frame, text="Data (DD/MM/AAAA):")
        self.data_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.data_entry = ctk.CTkEntry(self.data_hora_frame, width=120)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Campo de entrada para hora (opcional)
        self.hora_label = ctk.CTkLabel(self.data_hora_frame, text="Hora (HH:MM):")
        self.hora_label.grid(row=0, column=2, padx=5, pady=5)
        
        self.hora_entry = ctk.CTkEntry(self.data_hora_frame, width=80)
        self.hora_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Botão para filtrar por data
        self.botao_filtrar_data = ctk.CTkButton(
            self.data_hora_frame, 
            text="Filtrar Data", 
            command=self.filtrar_por_data
        )
        self.botao_filtrar_data.grid(row=0, column=4, padx=5, pady=5)
        
        # Botão para filtrar por data e hora
        self.botao_filtrar_data_hora = ctk.CTkButton(
            self.data_hora_frame, 
            text="Filtrar Data+Hora", 
            command=self.filtrar_por_data_hora
        )
        self.botao_filtrar_data_hora.grid(row=0, column=5, padx=5, pady=5)

        # Adicione isso no self.data_hora_frame, depois dos outros botões
        self.botao_remover_nao_encontrados = ctk.CTkButton(
            self.data_hora_frame, 
            text="Remover Não Encontrados", 
            command=self.remover_nao_encontrados,
            fg_color="#d00000",  # Vermelho para indicar ação destrutiva
            hover_color="#9d0208"
        )
        self.botao_remover_nao_encontrados.grid(row=0, column=6, padx=5, pady=5)
        
        # Frame para os botões principais (confirmar/atualizar)
        self.botoes_frame = ctk.CTkFrame(self.controles_frame)
        self.botoes_frame.pack(side="right", padx=10, pady=5)
        
        self.botao_confirmar = ctk.CTkButton(self.botoes_frame, text="Confirmar", command=self.confirmar_botao)
        self.botao_confirmar.pack(side="left", padx=10)
        
        self.botao_atualizar = ctk.CTkButton(self.botoes_frame, text="Atualizar", command=self.atualizar_interface)
        self.botao_atualizar.pack(side="left", padx=10)

        self.grupo_1 = list("ABCDEFGHI")
        self.grupo_2 = list("JKLMNOPQR")
        self.grupo_3 = list("STUVWXYZ")
        self.grupo_4 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        self.grupo_atual = "GERAL"
        self.letras_do_grupo = self.grupo_4
        self.dados = [] 
        self.botoes_filtro = ["TODOS", "TELEGRAMA", "PARECER", "RETORNO", "AGUARDANDO", "PENDENTE", "PRIMEIRO CONTATO", "SEM OBSERVACAO"]

        self.alteracoes_checkboxes = {}

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
                command=lambda l=letra: self.filtrar(letra=l)
            )
            botao.grid(row=0, column=idx, padx=2, pady=2)

    def criar_botoes_filtros(self):
        for idx, filtro in enumerate(self.botoes_filtro):
            btn = ctk.CTkButton(
                self.filtros_frame, text=filtro, 
                command=lambda f=filtro: self.filtrar(tipo_processo=f)
            )
            btn.grid(row=0, column=idx, padx=4, pady=4)

    def selecionar_grupo(self, grupo, letras):
        self.grupo_atual = grupo
        self.letras_do_grupo = letras
        self.atualizar_interface()

    def filtrar(self, letra=None, grupo=None, tipo_processo=None):
        df = pd.DataFrame(self.dados)

        if "removido" in df.columns:
            df = df[df["removido"] != True]

        # Filtra por grupo (automaticamente baseado no grupo_atual)
        if self.grupo_atual != "GERAL":
            df = df[df["nome"].str[0].str.upper().isin(self.letras_do_grupo)]

        # Filtra por letra, se informada
        if letra:
            df = df[df["nome"].str.upper().str.startswith(letra.upper())]

        # Filtra por tipo de processo, se diferente de "TODOS"
        if tipo_processo and tipo_processo.upper() != "TODOS":
            df = df[df["tipo"].str.upper().str.contains(tipo_processo.upper())]

        self.criar_widgets_processos(df)

    def filtrar_por_data(self):
        data_str = self.data_entry.get()
        try:
            # Converter para datetime no formato brasileiro
            data_filtro = datetime.strptime(data_str, "%d/%m/%Y").date()
            
            # Carregar e processar os dados
            df = pd.DataFrame(self.dados)
            if "data_hora_bot" not in df.columns:
                print("Nenhum dado de data_hora_bot encontrado")
                return
                
            # Explodir a coluna data_hora_bot
            df_explode = df.explode("data_hora_bot")
            
            # Converter para datetime
            df_explode["data_hora_bot"] = pd.to_datetime(df_explode["data_hora_bot"], errors="coerce")
            
            # Filtrar pela data
            df_filtrado = df_explode[df_explode["data_hora_bot"].dt.date == data_filtro]
            
            # Mostrar resultados
            if not df_filtrado.empty:
                self.criar_widgets_processos(df_filtrado)
                print(f"\nUsuários com data {data_str} em data_hora_bot:")
                for nome in df_filtrado["nome"].unique():
                    print(nome)
            else:
                print(f"Nenhum registro encontrado para a data {data_str}")
                
        except ValueError as e:
            print(f"Erro ao processar data: {e}. Use o formato DD/MM/AAAA")


    def remover_nao_encontrados(self):
        data_str = self.data_entry.get()
        hora_str = self.hora_entry.get()
        
        try:
            # Converter para datetime
            if hora_str:
                data_hora_str = f"{data_str} {hora_str}"
                filtro = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            else:
                filtro = datetime.strptime(data_str, "%d/%m/%Y").date()
            
            # Carregar dados
            df = pd.DataFrame(self.dados)

            # Filtrar apenas os que ainda não estão removidos
            df_nao_removidos = df[df.get("removido", False) != True].copy()

            # Criar coluna temporária para verificação
            df_nao_removidos['possui_data'] = df_nao_removidos['data_hora_bot'].apply(
                lambda x: any(
                    pd.to_datetime(item, errors='coerce') == filtro if hora_str
                    else pd.to_datetime(item, errors='coerce').date() == filtro
                    for item in (x if isinstance(x, list) else [])
                )
            )

            # Selecionar os que não possuem a data
            nao_encontrados = df_nao_removidos[~df_nao_removidos['possui_data']].copy()
            nao_encontrados['removido'] = True

            agora = datetime.now().strftime("%d/%m/%Y %H:%M")

            for _, row in nao_encontrados.iterrows():
                # Atualiza o campo resolvido_data_hora
                if isinstance(row.get("resolvido_data_hora"), list):
                    row["resolvido_data_hora"].append(agora)
                else:
                    row["resolvido_data_hora"] = [agora]

                # Adiciona ao dicionário de alterações
                self.alteracoes_checkboxes[row['codigo']] = row

            print(f"\n⚠️ {len(nao_encontrados)} registros marcados para remoção")
            print("Lembre-se de clicar em 'Confirmar' para salvar as alterações")
            
        except ValueError as e:
            print(f"Erro: {e}. Verifique o formato da data/hora.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    

    def filtrar_por_data_hora(self):
        data_str = self.data_entry.get()
        hora_str = self.hora_entry.get()
        
        if not data_str or not hora_str:
            print("Preencha ambos os campos: data e hora")
            return
            
        try:
            # Converter para datetime no formato brasileiro
            data_hora_str = f"{data_str} {hora_str}"
            data_hora_filtro = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            
            # Carregar e processar os dados
            df = pd.DataFrame(self.dados)
            if "data_hora_bot" not in df.columns:
                print("Nenhum dado de data_hora_bot encontrado")
                return
                
            # Explodir a coluna data_hora_bot
            df_explode = df.explode("data_hora_bot")
            
            # Converter para datetime
            df_explode["data_hora_bot"] = pd.to_datetime(df_explode["data_hora_bot"], errors="coerce")
            
            # Filtrar pela data e hora exata
            df_filtrado = df_explode[df_explode["data_hora_bot"] == data_hora_filtro]
            
            # Mostrar resultados
            if not df_filtrado.empty:
                self.criar_widgets_processos(df_filtrado)
                print(f"\nUsuários com data/hora {data_hora_str} em data_hora_bot:")
                for nome in df_filtrado["nome"].unique():
                    print(nome)
            else:
                print(f"Nenhum registro encontrado para a data/hora {data_hora_str}")
                
        except ValueError as e:
            print(f"Erro ao processar data/hora: {e}. Use os formatos DD/MM/AAAA e HH:MM")

    def criar_widgets_processos(self, df):
        # Limpa os widgets existentes no frame
        for widget in self.processos_frame.winfo_children():
            widget.destroy()

        # Criar widgets para cada processo
        for linha, row in df.iterrows():
            nome = row["nome"]
            tipo = row["tipo"]
            codigo = row["codigo"]

            # Cria um frame para cada linha de processo
            frame = ctk.CTkFrame(self.processos_frame)
            frame.pack(fill="x", pady=4, padx=4)

            # Nome do paciente (entry como readonly)
            nome_entry = ctk.CTkEntry(frame, width=320, font=("Arial", 14))
            nome_entry.insert(0, nome)
            nome_entry.configure(state="readonly")
            nome_entry.grid(row=linha, column=0, padx=10, pady=5, sticky="w")

            # Criar checkboxes para 'visto', 'verificar', 'resolvido'
            for idx, (campo, texto) in enumerate([("visto", "Visto"), ("verificar", "Verificar"), ("resolvido", "Resolvido")], start=1):
                var = tk.BooleanVar(value=row.get(campo, False))  # Use 'get' para evitar erro se o campo não existir

                # Usando partial para garantir que as variáveis sejam capturadas corretamente
                checkbox = ctk.CTkCheckBox(
                    frame,
                    text=texto,
                    variable=var,
                    command=partial(self.on_checkbox_click, row, campo, var)  # Passando a 'row' diretamente
                )
                checkbox.grid(row=linha, column=idx, padx=10, pady=5)

    def on_checkbox_click(self, pessoa, tipo, checkbox_var):
        novo_valor = checkbox_var.get()
        pessoa[tipo] = novo_valor

        self.atualizar_data_hora(tipo, novo_valor, pessoa)

        # Salva a alteração no dicionário
        codigo = pessoa["codigo"]
        self.alteracoes_checkboxes[codigo] = pessoa

        print(f"[{tipo.upper()}] Alterado para {novo_valor} | Código: {codigo}")
        print(f"→ Dados atuais: {pessoa}")

    def atualizar_data_hora(self, tipo, valor, pessoa):
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")

        if tipo == "visto":
            if valor:
                if isinstance(pessoa.get("visto_data_hora"), list):
                    pessoa["visto_data_hora"].append(agora)
                else:
                    pessoa["visto_data_hora"] = [agora]
                print(f"[INFO] visto_data_hora adicionada: {agora}")
            else:
                pessoa["visto_data_hora"] = []  # Ou use .pop(...) se quiser remover a chave
                print("[INFO] visto_data_hora esvaziada")

        elif tipo == "resolvido":
            if valor:
                if isinstance(pessoa.get("resolvido_data_hora"), list):
                    pessoa["resolvido_data_hora"].append(agora)
                else:
                    pessoa["resolvido_data_hora"] = [agora]
                print(f"[INFO] resolvido_data_hora adicionada: {agora}")
            else:
                pessoa["resolvido_data_hora"] = []
                print("[INFO] resolvido_data_hora esvaziada")

    def confirmar_botao(self):
        caminho_arquivo = f'{self.parent.caminho_pasta}/processos.json'
        self.salvar_alteracoes_processos(caminho_arquivo, self.alteracoes_checkboxes)
        self.atualizar_interface()

    def salvar_alteracoes_processos(self, arquivo, alteracoes_checkboxes):
        print("\n[ETAPA 1] Verificando alterações...")

        if not alteracoes_checkboxes:
            print("Nenhuma alteração detectada.")
            return

        alteracoes_salvas = []
        print("→ Alterações detectadas nos códigos:")

        for codigo, pessoa in alteracoes_checkboxes.items():
            # Verifica se pessoa é uma Series do pandas
            if not isinstance(pessoa, pd.Series):
                print(f"[ERRO] Dados de '{codigo}' não são válidos.")
                continue

            campos = {
                "visto": pessoa.get("visto", False),
                "verificar": pessoa.get("verificar", False),
                "resolvido": pessoa.get("resolvido", False),
                "visto_data_hora": pessoa.get("visto_data_hora", []),
                "resolvido_data_hora": pessoa.get("resolvido_data_hora", []),
                "removido": pessoa.get("removido", False)
            }

            if campos["resolvido"]:
                campos["visto"] = False
                campos["verificar"] = False
                campos["resolvido"] = False
                campos["removido"] = True

            alteracoes_salvas.append({
                "codigo": codigo,
                "alteracoes": campos
            })

        editar_dados_teste(alteracoes_salvas, arquivo)