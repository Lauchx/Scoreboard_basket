"""
Componentes UI modernos para información del partido (cuarto, posesión).
Diseño profesional tipo NBA/FIBA.
"""

import tkinter as tk
from tkinter import ttk


def create_quarter_labels_modern(self, modern_style):
    """
    Crea el label del cuarto/período con estilo moderno.
    Diseño: número grande arriba, palabra "cuarto" pequeña abajo, con borde blanco.

    Args:
        self: Instancia de Gui_scoreboard
        modern_style: Instancia de ScoreboardModernStyle para obtener configuración
    """
    # Obtener configuración
    colors = modern_style.COLORS
    sizes = modern_style.BASE_SIZES
    fonts = modern_style.FONTS

    # Crear un Frame contenedor para el cuarto con borde
    quarter_frame = tk.Frame(
        self.frames.match,
        bg=colors['bg_quarter'],  # Fondo configurable del sector de cuarto
        highlightbackground='#ffffff',  # Borde blanco
        highlightcolor='#ffffff',
        highlightthickness=2,
        relief='solid',
        borderwidth=2
    )
    quarter_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 3), padx=2)  # Padding horizontal mínimo

    # Configurar grid del frame
    quarter_frame.grid_rowconfigure(0, weight=3)  # Número (más grande)
    quarter_frame.grid_rowconfigure(1, weight=1)  # Texto "cuarto" (más pequeño)
    quarter_frame.grid_columnconfigure(0, weight=1)

    # Label del número del cuarto (grande)
    font_size_number = int(sizes['font_quarter'] * modern_style.scale_factor * 2)  # Doble de tamaño
    self.match.labels.quarter_number = tk.Label(
        quarter_frame,
        text=str(self.match_state.quarter),
        font=(fonts['display'][0], font_size_number, 'bold'),
        fg=colors['display_quarter'],  # Color configurable del número de cuarto
        bg=colors['bg_quarter'],  # Fondo configurable
        anchor='center'
    )
    self.match.labels.quarter_number.grid(row=0, column=0, sticky="nsew", pady=(5, 0))  # Reducido padding

    # Label del texto "cuarto" (pequeño, abajo)
    font_size_text = int(sizes['font_label'] * modern_style.scale_factor)
    self.match.labels.quarter_text = tk.Label(
        quarter_frame,
        text="cuarto",
        font=(fonts['display'][0], font_size_text),
        fg='#FFFFFF',  # Blanco
        bg=colors['bg_quarter'],  # Fondo configurable
        anchor='center'
    )
    self.match.labels.quarter_text.grid(row=1, column=0, sticky="nsew", pady=(0, 5))  # Reducido padding

    # Guardar referencia al frame para actualizaciones
    self.match.labels.quarter = self.match.labels.quarter_number  # Para compatibilidad con update
    self.match.labels.quarter_frame = quarter_frame  # Para cambio de color de fondo


def create_possession_labels_modern(self):
    """
    Crea el label de posesión con estilo moderno (SOLO FLECHA, sin texto).
    REDUCIDO AL MÍNIMO ABSOLUTO para dar máximo espacio a la grilla de faltas.
    Centrado horizontalmente y colocado en la parte inferior.

    Args:
        self: Instancia de Gui_scoreboard
    """
    # Flecha de posesión (REDUCIDA AL MÍNIMO ABSOLUTO, solo flecha sin texto) - CENTRADA
    self.match.labels.possesion = ttk.Label(
        self.frames.match,
        text="-",
        style="Possession.TLabel",
        anchor='center'  # Centrado horizontal
    )
    # Padding vertical MÍNIMO ABSOLUTO (0px arriba, 0px abajo) - SIN MÁRGENES
    self.match.labels.possesion.grid(row=3, column=0, sticky="", pady=0)

    # NO crear el texto "POSESIÓN" - solo la flecha según requerimiento del usuario


def setup_ui_match_modern(self):
    """
    Configura el frame central del partido con estilo moderno.
    Padding horizontal mínimo para dar máximo espacio a las columnas de jugadores.

    Estructura de filas:
    - Row 0: Tiempo (reloj)
    - Row 1: Cuarto
    - Row 2: Grilla de faltas y BONUS (2x3)
    - Row 3: Flecha de posesión (solo flecha, sin texto, reducida)

    Args:
        self: Instancia de Gui_scoreboard
    """
    # Padding horizontal muy reducido (5px) para columna central compacta
    self.frames.match = ttk.Frame(self.root, style="CenterPanel.TFrame", padding=(5, 10))
    self.frames.match.grid(row=0, column=1, sticky="nsew", padx=2, pady=10)

    # Configurar grid responsive
    self.frames.match.grid_columnconfigure(0, weight=1)

    # Pesos de las filas: tiempo (10), cuarto (4), faltas (22), posesión flecha (0 - mínimo espacio)
    # Proporción: 10:4:22:0 = tiempo:cuarto:faltas:posesión
    # La posesión con weight=0 usa solo el espacio mínimo necesario
    # Faltas aumentadas de 18 a 22 para dar más espacio vertical
    row_weights = (10, 4, 22, 0)
    for index, weight in enumerate(row_weights):
        self.frames.match.grid_rowconfigure(index, weight=weight)

