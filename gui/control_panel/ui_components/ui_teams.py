from tkinter import ttk

class ui_teams:
    def __init__(self, parent):
        self.parent = parent 
        self.home_team_controller = self.parent.match_state_controller.home_team_controller   
        self.away_team_controller = self.parent.match_state_controller.away_team_controller

    def setup_ui_teams(self):
        # Configurar paneles de puntuación en el grid 3x3 (Fila 1)
        self.setup_score_panel("local", 0, "LOCAL", self.parent.home_team, self.home_team_controller)
        self.setup_score_panel("visitor", 2, "VISITANTE", self.parent.away_team, self.away_team_controller)

    def setup_score_panel(self, team_type, column, title, team_namespace, team_controller):
        panel = ttk.Frame(self.parent.frames.match.right_frame, style="PanelTestScore.TFrame")
        panel.grid(row=1, column=column, sticky="nsew", padx=6, pady=6)
        panel.grid_rowconfigure(0, weight=0)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_rowconfigure(2, weight=0)
        panel.grid_columnconfigure(0, weight=1)

        ttk.Label(panel, text=title, style="PanelTestScoreTitle.TLabel", anchor="center").grid(row=0, column=0, sticky="ew", pady=(2, 0))

        # Label de puntuación
        points = team_controller.team.points
        score_label = ttk.Label(panel, text=str(points), style="PanelTestScore.TLabel", anchor="center")
        score_label.grid(row=1, column=0, sticky="nsew", pady=(6, 4))
        
        # Guardar referencia en el namespace para actualizaciones
        team_namespace.score_label = score_label

        # Botones de puntos
        buttons_frame = ttk.Frame(panel)
        buttons_frame.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        buttons_inner = ttk.Frame(buttons_frame)
        buttons_inner.pack(anchor="center")

        ttk.Button(buttons_inner, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: self.substract_point(team_controller, score_label)).pack(side='left', padx=4)
        ttk.Button(buttons_inner, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: self.add_point(team_controller, score_label)).pack(side='left', padx=4)



    def add_point(self, team_controller, score_label):
        team_controller.add_point()
        self.update_score_label(score_label, team_controller)
        self.parent.scoreboard_window.update_points_labels()

    def substract_point(self, team_controller, score_label):
        team_controller.substract_point()
        self.update_score_label(score_label, team_controller)
        self.parent.scoreboard_window.update_points_labels()

    def update_score_label(self, score_label, team_controller):
        if score_label.winfo_exists():
            score_label.config(text=str(team_controller.team.points))

    def buttons_points(self):
        # Deprecated: functionality moved to setup_score_panel
        pass

def update_player_combo(team_simple_name_space, team_controller):
    """
    Actualiza el combobox de selección de dorsal, eliminando los números ya usados.
    """
    if hasattr(team_simple_name_space.frames.team.combobox, 'jerseyNumber'):
        used_numbers = [int(p.jersey_number) for p in team_controller.team.players]
        available_numbers = [str(i) for i in range(100) if i not in used_numbers]
        team_simple_name_space.frames.team.combobox.jerseyNumber['values'] = available_numbers


