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
    # Obtener el color de fondo desde modern_style si está disponible
    from gui.scoreboard.modern_style import ScoreboardModernStyle
    bg_color = '#1a1a2e'  # Valor por defecto
    try:
        # Intentar obtener el color configurado
        if hasattr(team_frame.master, 'modern_style'):
            bg_color = team_frame.master.modern_style.COLORS.get('bg_team_name', '#1a1a2e')
    except:
        pass

    team_labels.name = tk.Label(
        team_frame,
        text=display_name,
        font=('Arial Narrow', 24, 'bold'),  # Fuente condensada para más caracteres
        fg='#FFFFFF',  # Blanco
        bg=bg_color,  # Fondo configurable
        anchor='center',
        width=12,  # ANCHO FIJO: 12 caracteres
        wraplength=150,  # Envolver texto a 100 píxeles de ancho
        justify='center',
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
    # Obtener el color de fondo desde modern_style si está disponible
    from gui.scoreboard.modern_style import ScoreboardModernStyle
    bg_color = '#1a1a2e'  # Valor por defecto
    try:
        # Intentar obtener el color configurado
        if hasattr(team_frame.master, 'modern_style'):
            bg_color = team_frame.master.modern_style.COLORS.get('bg_logo', '#1a1a2e')
    except:
        pass

    # Usar tk.Label para mejor control del centrado de la imagen
    team_labels.logo = tk.Label(
        team_frame,
        bg=bg_color,  # Fondo configurable
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
        bg=colors['bg_score'],  # Fondo configurable del sector de puntajes
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


def teams_labels_grid_configure(team_frame, is_home_team=True):
    """
    Configura el grid del frame del equipo para layout responsive.
    Las columnas de jugadores son flexibles, las de info (nombre/logo/puntos) son rígidas.

    Args:
        team_frame: Frame contenedor del equipo
        is_home_team: True si es equipo local, False si es visitante
    """
    if is_home_team:
        # Para equipo LOCAL:
        # Columna 0: Jugadores (flexible)
        # Columna 1: Info equipo - nombre, logo, puntos (rígida)
        # Columna 2: Vacía (sin uso)
        team_frame.grid_columnconfigure(0, weight=3)  # Columna jugadores LOCAL - FLEXIBLE
        team_frame.grid_columnconfigure(1, weight=1)  # Columna info equipo - RÍGIDA
        team_frame.grid_columnconfigure(2, weight=0)  # Columna vacía - SIN USO
    else:
        # Para equipo VISITANTE:
        # Columna 0: Vacía (sin uso)
        # Columna 1: Info equipo - nombre, logo, puntos (rígida)
        # Columna 2: Jugadores (flexible)
        team_frame.grid_columnconfigure(0, weight=0)  # Columna vacía - SIN USO
        team_frame.grid_columnconfigure(1, weight=1)  # Columna info equipo - RÍGIDA
        team_frame.grid_columnconfigure(2, weight=3)  # Columna jugadores VISITANTE - FLEXIBLE

    # Configurar filas con pesos para responsive
    for row in range(3):
        team_frame.grid_rowconfigure(row, weight=1)

