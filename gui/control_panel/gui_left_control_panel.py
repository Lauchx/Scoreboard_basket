from tkinter import ttk

def setup_left_panel(self):
    self.left_frame = ttk.Frame(self.root, style="PanelTestLeft.TFrame")
    self.left_frame.grid(row=0, column=0, sticky="nsew")

    self.notebook = ttk.Notebook(self.left_frame)
    self.notebook.pack(fill="both", expand=True, padx=2, pady=2)

    # Pestaña de Equipos (con notebook interno)
    self.tab_equipos = ttk.Frame(self.notebook)
    self.notebook.add(self.tab_equipos, text="Equipos")
    setup_tab_equipos(self)

    # Pestaña de Ajustes
    self.tab_ajustes = ttk.Frame(self.notebook)
    self.notebook.add(self.tab_ajustes, text="Ajustes")

def setup_tab_equipos(self):
    inner_notebook = ttk.Notebook(self.tab_equipos, style="Compact.TNotebook")
    inner_notebook.pack(fill="both", expand=True, padx=2, pady=2)

    # Pestaña Local
    self.tab_local_team = ttk.Frame(inner_notebook)
    inner_notebook.add(self.tab_local_team, text="Local")
    setup_team_form(self, self.tab_local_team, "local")

    # Pestaña Visitante
    self.tab_visitor_team = ttk.Frame(inner_notebook)
    inner_notebook.add(self.tab_visitor_team, text="Visitante")
    setup_team_form(self, self.tab_visitor_team, "visitor")


def setup_team_form(self, parent_frame, team_type):
    form_panel = ttk.Frame(parent_frame, padding=3)
    form_panel.pack(fill="x", padx=2, pady=2)

    # Nombre del equipo
    ttk.Label(form_panel, text="Equipo:", style="PlayerForm.TLabel").grid(row=0, column=0, sticky="w", padx=2, pady=1)
    team_entry = ttk.Entry(form_panel, width=15, style="PlayerForm.TEntry")
    team_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=1)
    setattr(self, f"{team_type}_team_name_entry", team_entry)

    ttk.Button(form_panel, text="Actualizar", style="PlayerForm.TButton", command=lambda: None).grid(row=0, column=2, padx=2, pady=1)

    # Nombre del jugador
    ttk.Label(form_panel, text="Jugador:", style="PlayerForm.TLabel").grid(row=1, column=0, sticky="w", padx=2, pady=1)
    player_entry = ttk.Entry(form_panel, width=15, style="PlayerForm.TEntry")
    player_entry.grid(row=1, column=1, sticky="ew", padx=2, pady=1)
    setattr(self, f"{team_type}_player_name_entry", player_entry)

    # Dorsal
    ttk.Label(form_panel, text="Dorsal:", style="PlayerForm.TLabel").grid(row=2, column=0, sticky="w", padx=2, pady=1)
    dorsal_combo = ttk.Combobox(form_panel, values=[str(i) for i in range(0, 100)], width=5, style="PlayerForm.TCombobox")
    dorsal_combo.set("0")
    dorsal_combo.grid(row=2, column=1, sticky="w", padx=2, pady=1)
    setattr(self, f"{team_type}_dorsal_combobox", dorsal_combo)

    ttk.Button(form_panel, text="Añadir", style="PlayerForm.TButton", command=lambda: None).grid(row=2, column=2, padx=2, pady=1)

    # Configurar columnas para que se expandan adecuadamente
    form_panel.columnconfigure(1, weight=1)

    # Frame para la lista de jugadores
    list_panel = ttk.Frame(parent_frame, padding=3)
    list_panel.pack(fill="both", expand=True, padx=2, pady=2)

    ttk.Label(list_panel, text="Jugadores:", style="PlayerForm.TLabel").pack(anchor="w", padx=2, pady=1)

    # Treeview para mostrar lista de jugadores (compacto)
    columns = ("Dorsal", "Nombre")
    player_tree = ttk.Treeview(list_panel, columns=columns, height=8, show="tree headings", style="Compact.Treeview")
    player_tree.column("#0", width=0, stretch="no")
    player_tree.column("Dorsal", anchor="center", width=40)
    player_tree.column("Nombre", anchor="w", width=100)
    player_tree.heading("Dorsal", text="Dorsal")
    player_tree.heading("Nombre", text="Nombre")
    player_tree.pack(fill="both", expand=True, padx=2, pady=1)

    setattr(self, f"{team_type}_players_tree", player_tree)
    setattr(self, f"{team_type}_players_list", [])