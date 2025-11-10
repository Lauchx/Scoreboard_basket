"""
Módulo de integración para aplicar el diseño moderno al scoreboard.

Este módulo permite activar/desactivar fácilmente el diseño moderno profesional
sin modificar el código original del scoreboard.

Uso:
    En gui_scoreboard.py, importar y usar:
    
    from gui.scoreboard.apply_modern_design import apply_modern_design
    
    # En __init__ de Gui_scoreboard, reemplazar:
    # apply_styles()
    # por:
    # apply_modern_design(self)
"""

from gui.scoreboard.modern_style import ScoreboardModernStyle
from gui.scoreboard.ui_components.ui_teams_modern import (
    create_names_labels_modern,
    create_logos_labels_modern, 
    create_points_labels_modern,
    teams_labels_grid_configure
)
from gui.scoreboard.ui_components.ui_time_modern import create_time_labels_modern
from gui.scoreboard.ui_components.ui_match_modern import (
    create_quarter_labels_modern,
    create_possession_labels_modern,
    setup_ui_match_modern
)
from gui.scoreboard.ui_components.ui_players_modern import create_players_labels_modern


def apply_modern_design(scoreboard_instance):
    """
    Aplica el diseño moderno completo al scoreboard.
    
    Esta función reemplaza las funciones de creación de UI originales
    por sus versiones modernas, sin alterar la lógica del scoreboard.
    
    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    # Crear e inicializar el sistema de estilos modernos
    modern_style = ScoreboardModernStyle(scoreboard_instance.root)
    
    # Guardar referencia al estilo para uso posterior
    scoreboard_instance.modern_style = modern_style
    
    # Configurar fondo de la ventana principal
    scoreboard_instance.root.configure(bg=modern_style.COLORS['bg_primary'])
    
    return modern_style


def setup_ui_modern(scoreboard_instance):
    """
    Configura el UI con diseño moderno (reemplaza setup_ui original).
    
    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    # Configurar grid de la ventana principal (responsive)
    for column in range(3):
        scoreboard_instance.root.grid_columnconfigure(column, weight=1, uniform="scoreboard")
    
    scoreboard_instance.root.grid_rowconfigure(0, weight=1)
    scoreboard_instance.root.grid_rowconfigure(1, weight=0)
    
    # Crear componentes del panel central con estilo moderno
    setup_ui_match_modern(scoreboard_instance)
    create_time_labels_modern(scoreboard_instance)
    create_possession_labels_modern(scoreboard_instance)
    create_quarter_labels_modern(scoreboard_instance)


def creates_home_team_modern(scoreboard_instance):
    """
    Crea el panel del equipo local con diseño moderno.
    
    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    from tkinter import ttk
    
    # Crear frame con estilo moderno
    scoreboard_instance.home_team.frames = ttk.Frame(
        scoreboard_instance.root, 
        style="HomeTeam.TFrame", 
        padding=(20, 15)
    )
    scoreboard_instance.home_team.frames.grid(
        row=0, column=0, sticky="nsew", padx=(20, 10), pady=20
    )
    
    # Configurar grid
    teams_labels_grid_configure(scoreboard_instance.home_team.frames)
    
    # Crear componentes UI con estilo moderno
    create_names_labels_modern(
        scoreboard_instance.home_team.frames, 
        scoreboard_instance.labels.home_team, 
        scoreboard_instance.match_state.home_team.name
    )
    create_logos_labels_modern(
        scoreboard_instance.home_team.frames, 
        scoreboard_instance.labels.home_team
    )
    create_points_labels_modern(
        scoreboard_instance.home_team.frames, 
        scoreboard_instance.labels.home_team, 
        scoreboard_instance.match_state.home_team.points
    )
    
    # Crear lista de jugadores con estilo moderno
    create_players_labels_modern(
        scoreboard_instance.home_team, 
        True,  # is_home_team
        scoreboard_instance.modern_style
    )


def creates_away_team_modern(scoreboard_instance):
    """
    Crea el panel del equipo visitante con diseño moderno.
    
    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    from tkinter import ttk
    
    # Crear frame con estilo moderno
    scoreboard_instance.away_team.frames = ttk.Frame(
        scoreboard_instance.root, 
        style="AwayTeam.TFrame", 
        padding=(20, 15)
    )
    scoreboard_instance.away_team.frames.grid(
        row=0, column=2, sticky="nsew", padx=(10, 20), pady=20
    )
    
    # Configurar grid
    teams_labels_grid_configure(scoreboard_instance.away_team.frames)
    
    # Crear componentes UI con estilo moderno
    create_names_labels_modern(
        scoreboard_instance.away_team.frames, 
        scoreboard_instance.labels.away_team, 
        scoreboard_instance.match_state.away_team.name
    )
    create_logos_labels_modern(
        scoreboard_instance.away_team.frames, 
        scoreboard_instance.labels.away_team
    )
    create_points_labels_modern(
        scoreboard_instance.away_team.frames, 
        scoreboard_instance.labels.away_team, 
        scoreboard_instance.match_state.away_team.points
    )
    
    # Crear lista de jugadores con estilo moderno
    create_players_labels_modern(
        scoreboard_instance.away_team, 
        False,  # is_home_team
        scoreboard_instance.modern_style
    )


def update_label_players_modern(scoreboard_instance, player, team_controller):
    """
    Actualiza la lista de jugadores con colores modernos para activos/inactivos.
    
    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
        player: Objeto Player
        team_controller: Controlador del equipo
    """
    import tkinter as tk
    from gui.scoreboard.gui_scoreboard import _nameSpace_team_for_controller
    
    team_simple_name_space = _nameSpace_team_for_controller(
        scoreboard_instance, 
        team_controller.team.name
    )
    
    team_simple_name_space.labels.players.insert(
        tk.END, 
        f"{player.jersey_number} - {player.name}"
    )
    
    index = team_simple_name_space.labels.players.size() - 1
    
    # Usar colores del estilo moderno
    if player.is_active:
        color = scoreboard_instance.modern_style.get_active_player_color()
    else:
        color = scoreboard_instance.modern_style.get_inactive_player_color()
    
    team_simple_name_space.labels.players.itemconfig(index, {'fg': color})

