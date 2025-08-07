import customtkinter as ctk

class Menu(ctk.CTkFrame):
    def __init__(self, parent, formatar_texto, check_list):
        super().__init__(parent)
        self.parent = parent
        self.formatar_texto = formatar_texto
        self.check_list = check_list

        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.label_menu = ctk.CTkLabel(self, text="MENU DE OPÇÕES")
        self.label_menu.grid(row=0, column=1, pady=15)

        self.btn_formatar_texto = ctk.CTkButton(self, text="Formatar Texto", width=250, command=self.exibir_formatar_texto)
        self.btn_formatar_texto.grid(row=1, column=1, pady=(10,0))

        self.btn_check_list = ctk.CTkButton(self, text="Check List", width=250, command=self.exibir_check_list)
        self.btn_check_list.grid(row=2, column=1, pady=(5,0))

    def exibir_formatar_texto(self):
        self.formatar_texto.deiconify()
        self.formatar_texto.lift()

    def exibir_check_list(self):
        self.check_list.deiconify()
        self.check_list.lift()
        self.check_list.atualizar_interface()
