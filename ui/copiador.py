import customtkinter as ctk
import pyperclip
import os
import json


class Copiador(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Copiador Texto")
        self.geometry("350x520")  # Janela um pouco maior
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        
        self.pages = {}      # Dicionário de páginas
        self.entries = {}    # Dicionário de entries
        self.current_page = 1
        
        self._setup_ui()
        self._bind_keys()
        self.show_page(1)


    def _setup_ui(self):
        """Configura a interface"""
        self._create_pages_with_labels()
        self._create_small_page_buttons()

    def _create_pages_with_labels(self):
        """Cria páginas com entries e labels F1-F12"""
        for page_num in range(1, 4):
            frame = ctk.CTkFrame(self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[page_num] = frame
            self.entries[page_num] = {}

            for i in range(1, 13):
                # Frame para cada linha (entry + label)
                row_frame = ctk.CTkFrame(frame)
                row_frame.grid(row=i-1, column=0, sticky="ew", pady=2)
                row_frame.grid_columnconfigure(1, weight=1)

                # Label F1-F12
                label = ctk.CTkLabel(row_frame, text=f"F{i}:", width=30)
                label.grid(row=0, column=0, padx=(5,0))

                # Entry maior
                entry = ctk.CTkEntry(row_frame, height=35, width=300)  # Altura aumentada
                entry.grid(row=0, column=1, padx=5, sticky="ew")
                self.entries[page_num][f"f{i}"] = entry

                entry.bind("<FocusOut>", lambda e: self._save_entries())

    def _create_small_page_buttons(self):
        """Cria botões pequenos 1 2 3"""
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=0, pady=5)
        
        for i in range(1, 4):
            btn = ctk.CTkButton(
                button_frame,
                text=str(i),
                width=30,
                command=lambda p=i: self.show_page(p)
            )
            btn.grid(row=0, column=i-1, padx=2)

    def show_page(self, page_num):
        """Mostra a página especificada"""
        for _, frame in self.pages.items():
            frame.grid_remove()
        self.pages[page_num].grid()
        self.current_page = page_num

    def _bind_keys(self):
        """Configura atalhos F1-F12"""
        for i in range(1, 13):
            self.bind_all(
                f"<F{i}>",
                lambda e, idx=i: self._handle_key_press(idx)
            )

    def _handle_key_press(self, idx):
        """Processa teclas F1-F12"""
        value = self.entries[self.current_page][f"f{idx}"].get()
        print(f"F{idx} da página {self.current_page}: {value}")
        pyperclip.copy(value)

    def _get_data_file_path(self):
        """Retorna o caminho completo do arquivo copiador.json"""
        return os.path.join(self.parent.caminho_pasta, "copiador.json")

    def _save_entries(self):
        """Salva todos os valores das entries em um arquivo JSON"""
        data = {}
        for page, entries in self.entries.items():
            data[page] = {}
            for key, entry in entries.items():
                data[page][key] = entry.get()
        caminho = self._get_data_file_path()
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _load_entries(self):
        """Carrega valores salvos das entries, se existir"""
        # Só tenta carregar se self.parent.caminho_pasta estiver definido
        if not getattr(self.parent, "caminho_pasta", None):
            return  # caminho ainda não definido, não faz nada

        caminho = self._get_data_file_path()
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                data = json.load(f)
            for page, entries in data.items():
                for key, value in entries.items():
                    if key in self.entries[int(page)]:
                        self.entries[int(page)][key].insert(0, value)

    def carregar_dados(self):
        """Chama o load entries quando o caminho estiver definido"""
        if getattr(self.parent, "caminho_pasta", None):
            self._load_entries()

    def _setup_ui(self):
        """Configura a interface"""
        self._create_pages_with_labels()
        self._create_small_page_buttons()
        
        # Carrega valores salvos do JSON
        self._load_entries()
