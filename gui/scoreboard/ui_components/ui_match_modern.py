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
        bg=colors['bg_center'],
        highlightbackground='#ffffff',  # Borde blanco
        highlightcolor='#ffffff',
        highlightthickness=2,
        relief='solid',
        borderwidth=2
    )
    quarter_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 5), padx=10)

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
        fg=colors['accent_orange'],  # Naranja brillante
        bg=colors['bg_center'],
        anchor='center'
    )
    self.match.labels.quarter_number.grid(row=0, column=0, sticky="nsew", pady=(10, 0))

    # Label del texto "cuarto" (pequeño, abajo)
    font_size_text = int(sizes['font_label'] * modern_style.scale_factor)
    self.match.labels.quarter_text = tk.Label(
        quarter_frame,
        text="cuarto",
        font=(fonts['display'][0], font_size_text),
        fg='#FFFFFF',  # Blanco
        bg=colors['bg_center'],
        anchor='center'
    )
    self.match.labels.quarter_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

    # Guardar referencia al frame para actualizaciones
    self.match.labels.quarter = self.match.labels.quarter_number  # Para compatibilidad con update


def create_possession_labels_modern(self):
    """
    Crea los labels de posesión con estilo moderno (flecha grande + texto).
    Centrados horizontalmente.

    Args:
        self: Instancia de Gui_scoreboard
    """
    # Flecha de posesión (grande, estilo neón) - CENTRADA
    self.match.labels.possesion = ttk.Label(
        self.frames.match,
        text="-",
        style="Possession.TLabel",
        anchor='center'  # Centrado horizontal
    )
    self.match.labels.possesion.grid(row=2, column=0, sticky="nsew")

    # Texto "POSESION" - CENTRADO
    self.match.labels.possesion_text = ttk.Label(
        self.frames.match,
        text="POSESIÓN",
        style="PossessionText.TLabel",
        anchor='center'  # Centrado horizontal
    )
    self.match.labels.possesion_text.grid(row=3, column=0, sticky="nsew", pady=(10, 0))


def setup_ui_match_modern(self):
    """
    Configura el frame central del partido con estilo moderno.
    
    Args:
        self: Instancia de Gui_scoreboard
    """
    self.frames.match = ttk.Frame(self.root, style="CenterPanel.TFrame", padding=(20, 15))
    self.frames.match.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
    
    # Configurar grid responsive
    self.frames.match.grid_columnconfigure(0, weight=1)
    
    # Pesos de las filas: tiempo (2), cuarto (1), posesión (3), texto posesión (1)
    row_weights = (2, 1, 3, 1)
    for index, weight in enumerate(row_weights):
        self.frames.match.grid_rowconfigure(index, weight=weight)

