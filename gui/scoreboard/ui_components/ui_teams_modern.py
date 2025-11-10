"""
Componentes UI modernos para los equipos en el scoreboard.
Versión con diseño profesional tipo NBA/FIBA.
"""

from tkinter import ttk


def create_names_labels_modern(team_frame, team_labels, team_name):
    """
    Crea el label del nombre del equipo con estilo moderno.
    
    Args:
        team_frame: Frame contenedor del equipo
        team_labels: Namespace para almacenar referencias a labels
        team_name: Nombre del equipo
    """
    team_labels.name = ttk.Label(
        team_frame, 
        text=team_name, 
        style="TeamName.TLabel"
    )
    team_labels.name.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="nsew")


def create_logos_labels_modern(team_frame, team_labels):
    """
    Crea el label para el logo del equipo con estilo moderno.
    
    Args:
        team_frame: Frame contenedor del equipo
        team_labels: Namespace para almacenar referencias a labels
    """
    team_labels.logo = ttk.Label(team_frame, style="Info.TLabel")
    team_labels.logo.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")


def create_points_labels_modern(team_frame, team_labels, points_team):
    """
    Crea el label del puntaje con estilo moderno (números grandes tipo LED).
    
    Args:
        team_frame: Frame contenedor del equipo
        team_labels: Namespace para almacenar referencias a labels
        points_team: Puntaje inicial del equipo
    """
    team_labels.points = ttk.Label(
        team_frame, 
        text=str(points_team), 
        style="Score.TLabel",
        anchor="center"
    )
    team_labels.points.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="nsew")


def teams_labels_grid_configure(team_frame):
    """
    Configura el grid del frame del equipo para layout responsive.
    
    Args:
        team_frame: Frame contenedor del equipo
    """
    # Configurar columnas con pesos para responsive
    for column in range(3):
        team_frame.grid_columnconfigure(column, weight=1)
    
    # Configurar filas con pesos para responsive
    for row in range(3):
        team_frame.grid_rowconfigure(row, weight=1)

