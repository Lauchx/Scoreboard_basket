"""
Componente UI moderno para la lista de jugadores en el scoreboard.
Diseño profesional con colores diferenciados para jugadores activos/inactivos.
"""

import tkinter as tk


def create_players_labels_modern(team_simple_name_space, is_home_team, modern_style):
    """
    Crea el Listbox de jugadores con estilo moderno.
    
    Args:
        team_simple_name_space: Namespace del equipo
        is_home_team: True si es equipo local, False si es visitante
        modern_style: Instancia de ScoreboardModernStyle para obtener configuración
    """
    # Obtener configuración de estilo
    listbox_config = modern_style.get_player_listbox_config()
    
    # Crear Listbox con configuración moderna
    team_simple_name_space.labels.players = tk.Listbox(
        team_simple_name_space.frames,
        **listbox_config
    )
    
    # Posicionamiento según equipo
    col = 0 if is_home_team else 2
    padding = (0, 15) if is_home_team else (15, 0)
    
    team_simple_name_space.labels.players.grid(
        row=0, 
        column=col, 
        rowspan=3, 
        sticky="nsew", 
        padx=padding, 
        pady=5
    )

