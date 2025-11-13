import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from types import SimpleNamespace
# from PIL import Image, ImageTk
# import os -- Revisar uso.

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE DISEÑO
# ═══════════════════════════════════════════════════════════════════════════
# Cambiar a True para activar el diseño moderno profesional tipo NBA/FIBA
# Cambiar a False para usar el diseño original
USE_MODERN_DESIGN = True
# ═══════════════════════════════════════════════════════════════════════════

if USE_MODERN_DESIGN:
    # Importar módulos del diseño moderno
    from gui.scoreboard.apply_modern_design import (
        apply_modern_design,
        setup_ui_modern,
        creates_home_team_modern,
        creates_away_team_modern,
        update_label_players_modern
    )
else:
    # Importar módulos del diseño original
    from gui.scoreboard.styles_scoreboard import apply_styles
    from gui.scoreboard.ui_components.ui_time import create_time_labels
    from gui.scoreboard.ui_components.ui_teams import (
        create_names_labels, create_logos_labels,
        create_points_labels, teams_labels_grid_configure
    )
    from gui.scoreboard.ui_components.ui_players import create_players_labels
    from gui.scoreboard.ui_components.ui_match import (
        create_possession_labels, create_quarter_labels, setup_ui_match
    )
    from gui.scoreboard.ui_components.ui_timeouts import (
        create_timeout_indicators, update_timeout_indicators
    )
class Gui_scoreboard:
    def __init__(self, root, match_state):
        """
        Args:
            home_team (Team): Objeto Team compartido con Gui_control_panel.
            away_team (Team): Objeto Team compartido con Gui_control_panel.
        """
        self.root = root
        self.root.title("Scoreboard")
        self.root.protocol("WM_DELETE_WINDOW", lambda: messagebox.showinfo("Info", "No podés cerrar esta ventana."))

        # Aplicar estilos según configuración
        if USE_MODERN_DESIGN:
            apply_modern_design(self)
        else:
            apply_styles()
            self.root.configure(bg="black")

        simpleNamespace_forUi(self)
        self.match_state = match_state

        # Setup UI según diseño seleccionado
        if USE_MODERN_DESIGN:
            setup_ui_modern(self)
        else:
            setup_ui(self)

        if not hasattr(self, "labels"):
            self.labels = SimpleNamespace(home_team=SimpleNamespace(),
                                     away_team=SimpleNamespace(),
                                     match=SimpleNamespace())
        self.home_team_labels = _nameSpace_team_for_controller(self, self.match_state.home_team.name)
        self.away_team_labels =_nameSpace_team_for_controller(self, self.match_state.away_team.name)

        # Crear equipos según diseño seleccionado
        if USE_MODERN_DESIGN:
            creates_home_team_modern(self)
            creates_away_team_modern(self)
        else:
            creates_home_team(self)
            creates_away_team(self)
    # Updates labels functions
    def update_team_logo_label(self):
        self.labels.home_team.logo.config(image=self.match_state.home_team.logo)
        self.labels.away_team.logo.config(image=self.match_state.away_team.logo)
    def update_points_labels(self):
        self.labels.home_team.points.config(text=str(self.match_state.home_team.points))
        self.labels.away_team.points.config(text=str(self.match_state.away_team.points))

    def update_time_labels(self):
        minutes = self.match_state.seconds_time_left // 60
        seconds = self.match_state.seconds_time_left % 60
        time_str = f"{minutes:02}:{seconds:02}"

        # Actualizar el label (funciona tanto para diseño moderno como original)
        self.match.labels.time.config(text=time_str)

    def update_possession_labels(self, possession):
         self.match.labels.possesion.config(text=possession)   

    def update_team_names_labels(self):
        self.labels.home_team.name.config(text=self.match_state.home_team.name)
        self.labels.away_team.name.config(text=self.match_state.away_team.name)

    def update_quarter_labels(self, number):
        self.match_state.quarter += number
        if USE_MODERN_DESIGN:
            # En diseño moderno, solo actualizar el número (sin "Cuarto:")
            self.match.labels.quarter.config(text=str(self.match_state.quarter))
        else:
            # En diseño original, mostrar "Cuarto: X"
            self.match.labels.quarter.config(text=f"Cuarto: {self.match_state.quarter}")

    def update_possession_labels(self):
        current_possesion = self.match_state.possession
        if current_possesion == "Away":
            self.match_state.possession = "Home"
            new_possesion = "⇦"
            self.match.labels.possesion.config(text=str(new_possesion))
        else:
            self.match_state.possession = "Away"
            new_possesion = "⇨"
            self.match.labels.possesion.config(text=str(new_possesion))

    def update_timeout_labels(self):
        """
        Actualiza la visualización de los indicadores de timeout para ambos equipos.
        """
        if USE_MODERN_DESIGN:
            from gui.scoreboard.ui_components.ui_timeouts_modern import update_timeout_indicators_modern

            # Actualizar equipo local
            home_states = self.match_state.home_team.timeout_manager.get_timeout_states()
            update_timeout_indicators_modern(self.labels.home_team, home_states)

            # Actualizar equipo visitante
            away_states = self.match_state.away_team.timeout_manager.get_timeout_states()
            update_timeout_indicators_modern(self.labels.away_team, away_states)
        else:
            # Diseño original
            # Actualizar equipo local
            home_states = self.match_state.home_team.timeout_manager.get_timeout_states()
            update_timeout_indicators(self.labels.home_team, home_states)

            # Actualizar equipo visitante
            away_states = self.match_state.away_team.timeout_manager.get_timeout_states()
            update_timeout_indicators(self.labels.away_team, away_states)

    def update_label_players(self, player, team_contoller):
        if USE_MODERN_DESIGN:
            update_label_players_modern(self, player, team_contoller)
        else:
            team_simple_name_space = _nameSpace_team_for_controller(self, team_contoller.team.name)
            team_simple_name_space.labels.players.insert(tk.END, f"{player.jersey_number} - {player.name}" )
            index = team_simple_name_space.labels.players.size() - 1
            if player.is_active:
                team_simple_name_space.labels.players.itemconfig(index, {'fg': 'green'})
            else:
                team_simple_name_space.labels.players.itemconfig(index, {'fg': 'black'})

def simpleNamespace_forUi(self):
        #self.labels = SimpleNamespace(home_team=SimpleNamespace(),away_team=SimpleNamespace(),match=SimpleNamespace())
        self.frames = SimpleNamespace(teams=SimpleNamespace()) 
        self.home_team = SimpleNamespace(labels=SimpleNamespace(), frames=SimpleNamespace())
        self.away_team = SimpleNamespace(labels=SimpleNamespace(), frames=SimpleNamespace())
        self.match = SimpleNamespace(labels=SimpleNamespace(), frames=SimpleNamespace())
# Create functions labels

def _nameSpace_team_for_controller(self, team_name) -> SimpleNamespace:
    if team_name == self.match_state.home_team.name:
        return self.home_team
    return self.away_team

def setup_ui(self):
    for column in range(3):
        self.root.grid_columnconfigure(column, weight=1, uniform="scoreboard")

    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_rowconfigure(1, weight=0)

    setup_ui_match(self)
    
    create_time_labels(self)
    create_possession_labels(self)
    create_quarter_labels(self)

def creates_home_team(self):
    self.home_team.frames = ttk.Frame(self.root, style="home_team.TFrame", padding=(20, 15))
    self.home_team.frames.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
    #ui_team
    teams_labels_grid_configure(self.home_team.frames)
    create_names_labels(self.home_team.frames, self.labels.home_team, self.match_state.home_team.name)
    create_logos_labels(self.home_team.frames, self.labels.home_team)
    create_points_labels(self.home_team.frames, self.labels.home_team, self.match_state.home_team.points)
    #ui_players
    create_players_labels(self.home_team, True)
    #ui_timeouts
    create_timeout_indicators(self.home_team.frames, self.labels.home_team)
   

def creates_away_team(self):
    self.away_team.frames = ttk.Frame(self.root, padding=(20, 15))
    self.away_team.frames.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=20)
    #ui_team
    teams_labels_grid_configure(self.away_team.frames)
    create_names_labels(self.away_team.frames, self.labels.away_team, self.match_state.away_team.name)
    create_logos_labels(self.away_team.frames, self.labels.away_team)
    create_points_labels(self.away_team.frames, self.labels.away_team, self.match_state.away_team.points)
    #ui_players
    create_players_labels(self.away_team, False)
    #ui_timeouts
    create_timeout_indicators(self.away_team.frames, self.labels.away_team)