from tkinter import ttk

def setup_left_panel(self):
    # Crear el frame izquierdo y notebook
    self.left_frame = ttk.Frame(self.root, style="PanelTestLeft.TFrame")
    self.left_frame.grid(row=0, column=0, sticky="nsew")

    self.notebook = ttk.Notebook(self.left_frame)
    self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

    self.tab_jugadores = ttk.Frame(self.notebook)
    self.notebook.add(self.tab_jugadores, text="Jugadores")

    self.tab_ajustes = ttk.Frame(self.notebook)
    self.notebook.add(self.tab_ajustes, text="Ajustes")

    setup_tab_jugadores(self)
    
def setup_tab_jugadores(self):
    self.player_input_panel = ttk.Frame(self.tab_jugadores, padding=10)
    self.player_input_panel.pack(fill="x", padx=10, pady=10)

    # Nombre del equipo
    self.team_name_label = ttk.Label(self.player_input_panel, text="Nombre del equipo:", style="PlayerForm.TLabel")
    self.team_name_label.grid(row=0, column=0, sticky="w")
    self.team_name_entry = ttk.Entry(self.player_input_panel, width=30, style="PlayerForm.TEntry")
    self.team_name_entry.grid(row=0, column=1, padx=6, pady=4)

    self.update_team_name_btn = ttk.Button(
        self.player_input_panel,
        text="Actualizar nombre",
        style="PlayerForm.TButton",
        command=lambda: None
    )
    self.update_team_name_btn.grid(row=0, column=2, padx=6)

    # Nombre del jugador
    self.player_name_label = ttk.Label(self.player_input_panel, text="Nombre del jugador:", style="PlayerForm.TLabel")
    self.player_name_label.grid(row=1, column=0, sticky="w")
    self.player_name_entry = ttk.Entry(self.player_input_panel, width=30, style="PlayerForm.TEntry")
    self.player_name_entry.grid(row=1, column=1, padx=6, pady=4)

    # Dorsal
    self.dorsal_label = ttk.Label(self.player_input_panel, text="Dorsal:", style="PlayerForm.TLabel")
    self.dorsal_label.grid(row=2, column=0, sticky="w")
    self.dorsal_combobox = ttk.Combobox(
        self.player_input_panel,
        values=[str(i) for i in range(0, 100)],
        width=5,
        style="PlayerForm.TCombobox"
    )
    self.dorsal_combobox.grid(row=2, column=1, sticky="w", padx=6, pady=4)
    self.dorsal_combobox.set("0")

    # Botón añadir jugador
    self.add_player_btn = ttk.Button(
        self.player_input_panel,
        text="Añadir jugador",
        style="PlayerForm.TButton",
        command=lambda: None
    )
    self.add_player_btn.grid(row=2, column=2, padx=6)