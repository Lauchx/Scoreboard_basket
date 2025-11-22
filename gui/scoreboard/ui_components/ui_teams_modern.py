"""
Componentes UI modernos para los equipos en el scoreboard.
Versión con diseño profesional tipo NBA/FIBA.
"""

import tkinter as tk
from tkinter import ttk


def create_names_labels_modern(team_frame, team_labels, team_name):
    """
    Crea el label del nombre del equipo con estilo moderno.
    Ancho fijo de 12 caracteres para mantener columnas uniformes.

    Args:
        team_frame: Frame contenedor del equipo
        team_labels: Namespace para almacenar referencias a labels
        team_name: Nombre del equipo
    """
    # Truncar nombre a 12 caracteres máximo
    display_name = team_name[:12] if len(team_name) > 12 else team_name

    # Usar tk.Label para poder especificar width fijo
    team_labels.name = tk.Label(
        team_frame,
        text=display_name,
        font=('Arial Narrow', 24, 'bold'),  # Fuente condensada para más caracteres
        fg='#FFFFFF',  # Blanco
        bg='#1a1a2e',  # Fondo oscuro
        anchor='center',
        width=12,  # ANCHO FIJO: 12 caracteres
        padx=5,
        pady=5
    )
    team_labels.name.grid(row=1, column=1, padx=2, pady=(2, 3), sticky="nsew")  # Padding mínimo para columna compacta


def create_logos_labels_modern(team_frame, team_labels):
    """
    Crea el label para el logo del equipo con estilo moderno.
    El logo se centra en su espacio asignado.

    Args:
        team_frame: Frame contenedor del equipo
        team_labels: Namespace para almacenar referencias a labels
    """
    # Usar tk.Label para mejor control del centrado de la imagen
    team_labels.logo = tk.Label(
        team_frame,
        bg='#1a1a2e',  # Fondo oscuro (mismo que Info.TLabel)
        anchor='center'  # Centrar el contenido
    )
    team_labels.logo.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")  # Padding mínimo para columna compacta


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
        padx=5,   # Reducido de 10 a 5 para columna más compacta
        pady=5,   # Reducido de 8 a 5 para columna más compacta
        # Borde blanco alrededor del puntaje (igual que el reloj)
        highlightbackground='#ffffff',
        highlightcolor='#ffffff',
        highlightthickness=border_width,
        relief='solid',
        borderwidth=border_width
    )
    team_labels.points.grid(row=2, column=1, padx=2, pady=(2, 2), sticky="nsew")  # Padding mínimo para columna compacta


def teams_labels_grid_configure(team_frame):
    """
    Configura el grid del frame del equipo para layout responsive.
    Columna 0 (jugadores) tiene más espacio que columna 1 (info equipo).

    Args:
        team_frame: Frame contenedor del equipo
    """
    # Configurar columnas con pesos para dar más espacio a jugadores
    team_frame.grid_columnconfigure(0, weight=3)  # Columna jugadores - MÁS ESPACIO
    team_frame.grid_columnconfigure(1, weight=1)  # Columna info equipo - MENOS ESPACIO
    team_frame.grid_columnconfigure(2, weight=0)  # Columna vacía (si existe)

    # Configurar filas con pesos para responsive
    for row in range(3):
        team_frame.grid_rowconfigure(row, weight=1)

