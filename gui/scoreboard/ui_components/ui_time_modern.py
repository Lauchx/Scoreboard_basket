"""
Componente UI moderno para el tiempo/reloj del scoreboard.
Estilo digital profesional con fuente tipo display LED de 7 segmentos.
"""

import tkinter as tk
from tkinter import font as tkfont
from pathlib import Path


def create_time_labels_modern(self):
    """
    Crea el label del reloj con fuente digital profesional tipo 7 segmentos.
    Formato: MM:SS con fuente Digital-7 Mono (monoespaciada para evitar saltos).
    Incluye un borde blanco para destacar visualmente el reloj.

    Args:
        self: Instancia de Gui_scoreboard
    """
    minutes = self.match_state.seconds_time_left // 60
    seconds = self.match_state.seconds_time_left % 60

    # Obtener colores y tamaños del modern_style
    bg_color = self.modern_style.COLORS['bg_center']
    fg_color = self.modern_style.COLORS['display_time']
    font_size = self.modern_style.BASE_SIZES['font_time']
    border_width = self.modern_style.BASE_SIZES['time_border_width']

    # Usar fuente MONO (monoespaciada) para que el reloj no "salte"
    # La fuente Digital-7 Mono tiene todos los dígitos del mismo ancho
    font_family = 'Digital-7 Mono'

    # Crear label del reloj con fuente monoespaciada
    self.match.labels.time = tk.Label(
        self.frames.match,
        text=f"{minutes:02}:{seconds:02}",
        font=(font_family, font_size),
        fg=fg_color,
        bg=bg_color,
        anchor='center',
        padx=15,
        pady=12,
        # Borde blanco alrededor del reloj
        highlightbackground='#ffffff',
        highlightcolor='#ffffff',
        highlightthickness=border_width,
        relief='solid',
        borderwidth=border_width
    )
    self.match.labels.time.grid(row=0, column=0, sticky="nsew", pady=(5, 5), padx=2)

    print(f"[OK] Reloj creado con fuente {font_family} (tamaño: {font_size}, monoespaciada)")

