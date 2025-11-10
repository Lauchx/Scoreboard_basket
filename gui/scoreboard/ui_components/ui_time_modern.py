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
    Formato: MM:SS con fuente Digital-7 Italic real.

    Args:
        self: Instancia de Gui_scoreboard
    """
    minutes = self.match_state.seconds_time_left // 60
    seconds = self.match_state.seconds_time_left % 60

    # Obtener colores del modern_style
    bg_color = self.modern_style.COLORS['bg_center']
    fg_color = self.modern_style.COLORS['display_time']
    font_size = self.modern_style.BASE_SIZES['font_time']

    # La fuente Digital-7 Italic ya está cargada en Windows por modern_style
    # Usar el nombre exacto de la familia de fuente que Windows reconoce

    # Crear label con tk.Label (no ttk) para mejor soporte de fuentes personalizadas
    # Usar 'Digital-7 Italic' como nombre de familia (así es como Windows la registra)
    self.match.labels.time = tk.Label(
        self.frames.match,
        text=f"{minutes:02}:{seconds:02}",
        font=('Digital-7 Italic', font_size),  # Usar el nombre completo de la fuente
        fg=fg_color,
        bg=bg_color,
        anchor='center',
        padx=20,
        pady=15
    )

    print(f"✅ Reloj creado con fuente Digital-7 Italic (tamaño: {font_size})")

    # {minutes:02}:{seconds:02} -> (:02) agrega dos dígitos si el número es menor a 10
    self.match.labels.time.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

