"""
Componentes UI modernos para los equipos en el scoreboard.
Versión con diseño profesional tipo NBA/FIBA.
"""

import tkinter as tk
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


def create_points_labels_modern(team_frame, team_labels, points_team, modern_style):
    """
    Crea el label del puntaje con estilo moderno (números grandes tipo LED con borde blanco).
    Usa tk.Label para poder agregar borde similar al reloj.

    Args:
        team_frame: Frame contenedor del equipo
        team_labels: Namespace para almacenar referencias a labels
        points_team: Puntaje inicial del equipo
        modern_style: Instancia de ScoreboardModernStyle para obtener configuración
    """
    # Obtener configuración de colores y tamaños
    colors = modern_style.COLORS
    sizes = modern_style.BASE_SIZES
    fonts = modern_style.FONTS

    # Calcular tamaño de fuente escalado
    font_size = int(sizes['font_score'] * modern_style.scale_factor)
    border_width = sizes.get('score_border_width', 2)  # Borde de 2px por defecto

    # Crear label con tk.Label para poder usar highlightbackground (borde)
    team_labels.points = tk.Label(
        team_frame,
        text=str(points_team),
        font=(fonts['score'][0], font_size, 'bold'),
        fg='#FFFFFF',  # Texto blanco
        bg=colors['bg_secondary'],  # Fondo oscuro
        anchor='center',
        padx=20,
        pady=15,
        # Borde blanco alrededor del puntaje (igual que el reloj)
        highlightbackground='#ffffff',
        highlightcolor='#ffffff',
        highlightthickness=border_width,
        relief='solid',
        borderwidth=border_width
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

