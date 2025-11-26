from tkinter import ttk

def setup_action_panel(self, parent_frame):
    """Configura el panel central con botones de acción y indicador de posesión"""
    self.frames.match.action = ttk.Frame(parent_frame, style="ControlPanel.Stack.TFrame")
    self.frames.match.action.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)

    self.frames.match.action.grid_rowconfigure(0, weight=1)
    self.frames.match.action.grid_rowconfigure(1, weight=1)
    self.frames.match.action.grid_columnconfigure(0, weight=1)

    action_buttons = ttk.Frame(self.frames.match.action, style="ControlPanel.Stack.TFrame")
    action_buttons.grid(row=0, column=0, sticky="n", pady=(10, 0))

    ttk.Button(
        action_buttons,
        text="Borrar puntos",
        style="ControlPanel.Button.TButton",
        command=lambda: clear_points(self)
    ).pack(side="top", pady=6)

    ttk.Button(
        action_buttons,
        text="Cambiar posesión",
        style="ControlPanel.Button.TButton",
        command=lambda: change_possession(self)
    ).pack(side="top", pady=6)

    # Flecha abajo (indicador de posesión)
    possession_indicator = ttk.Frame(self.frames.match.action)
    possession_indicator.grid(row=1, column=0, sticky="ew", pady=(0, 10))
    possession_indicator.grid_columnconfigure(0, weight=1)

    self.match.possession_label = ttk.Label(
        possession_indicator,
        text=get_possession_text(self),
        style="PanelTestScore.TLabel",
        anchor="center"  
    )
    self.match.possession_label.pack(fill="x", expand=True)

def clear_points(self):
    """Limpia los puntos de ambos equipos y sincroniza con scoreboard"""
    self.home_team_controller.team.points = 0
    self.away_team_controller.team.points = 0
    
    # Actualizar labels de puntos si existen
    if hasattr(self.home_team, 'score_label'):
        self.home_team.score_label.config(text="0")
    if hasattr(self.away_team, 'score_label'):
        self.away_team.score_label.config(text="0")
        
    self.scoreboard_window.update_points_labels()

def change_possession(self):
    """Cambia la posesión de un equipo a otro y sincroniza con scoreboard"""
    from gui.control_panel.ui_components.ui_possession import toggle_possession
    toggle_possession(self)
    update_possession_label(self)

def update_possession_label(self):
    """Actualiza el label de posesión con el valor actual"""
    if hasattr(self.match, 'possession_label') and self.match.possession_label.winfo_exists():
        self.match.possession_label.config(text=get_possession_text(self))

def get_possession_text(self):
    possession = self.match_state_controller.match_state.possession
    return "⇦" if possession == "Home" else "⇨"
