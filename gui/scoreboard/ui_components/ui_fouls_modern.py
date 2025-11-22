"""
Componente UI moderno para faltas de equipo y estado de BONUS en el scoreboard.
Muestra una grilla 2x2 con indicadores de BONUS y contadores de faltas para cada equipo.
"""

import tkinter as tk
from tkinter import ttk


def create_fouls_grid_modern(self, modern_style):
    """
    Crea la grilla 2x2 de faltas y BONUS para ambos equipos.
    
    Estructura:
    ┌─────────────┬─────────────┐
    │ BONUS HOME  │ BONUS AWAY  │  <- Fila 0: Indicadores de BONUS
    │   [LED]     │   [LED]     │
    ├─────────────┼─────────────┤
    │ Faltas: X   │ Faltas: X   │  <- Fila 1: Contadores de faltas
    └─────────────┴─────────────┘
    
    Args:
        self: Instancia de Gui_scoreboard
        modern_style: Instancia de ScoreboardModernStyle
    """
    # Obtener configuración
    colors = modern_style.COLORS
    sizes = modern_style.BASE_SIZES
    fonts = modern_style.FONTS
    
    # Crear frame contenedor para la grilla de faltas
    fouls_frame = tk.Frame(
        self.frames.match,
        bg=colors['bg_center']
    )
    fouls_frame.grid(row=2, column=0, sticky="nsew", pady=(5, 5), padx=2)
    
    # Configurar grid del frame (2 columnas, 3 filas)
    fouls_frame.grid_columnconfigure(0, weight=1)  # Columna HOME
    fouls_frame.grid_columnconfigure(1, weight=1)  # Columna AWAY
    fouls_frame.grid_rowconfigure(0, weight=1, minsize=30)     # Fila BONUS (mínimo 30px)
    fouls_frame.grid_rowconfigure(1, weight=1, minsize=25)     # Fila texto "Faltas" (mínimo 25px)
    fouls_frame.grid_rowconfigure(2, weight=2, minsize=80)     # Fila número (más grande, mínimo 80px)
    
    # Inicializar namespace para labels de faltas
    if not hasattr(self.match.labels, 'fouls'):
        from types import SimpleNamespace
        self.match.labels.fouls = SimpleNamespace()
        self.match.labels.fouls.home = SimpleNamespace()
        self.match.labels.fouls.away = SimpleNamespace()
    
    # ═══════════════════════════════════════════════════════════
    # EQUIPO LOCAL (HOME) - Columna 0
    # ═══════════════════════════════════════════════════════════
    
    # Frame para BONUS HOME
    home_bonus_frame = tk.Frame(fouls_frame, bg=colors['bg_center'])
    home_bonus_frame.grid(row=0, column=0, sticky="n", padx=2, pady=2)  # sticky="n" para alinear arriba
    
    # Label "BONUS"
    font_size_bonus = int(sizes['font_label'] * modern_style.scale_factor * 0.8)
    home_bonus_label = tk.Label(
        home_bonus_frame,
        text="BONUS",
        font=(fonts['display'][0], font_size_bonus, 'bold'),
        fg='#FFFFFF',
        bg=colors['bg_center'],
        anchor='center'
    )
    home_bonus_label.pack(side='left', padx=(5, 2))
    
    # LED indicador de BONUS (círculo)
    home_bonus_canvas = tk.Canvas(
        home_bonus_frame,
        width=20,
        height=20,
        bg=colors['bg_center'],
        highlightthickness=0
    )
    home_bonus_canvas.pack(side='left', padx=(2, 5))
    
    # Crear círculo LED (apagado por defecto)
    home_bonus_led = home_bonus_canvas.create_oval(
        2, 2, 18, 18,
        fill='#404040',  # Gris oscuro (apagado)
        outline='#606060',
        width=1
    )
    
    # Guardar referencias
    self.match.labels.fouls.home.bonus_canvas = home_bonus_canvas
    self.match.labels.fouls.home.bonus_led = home_bonus_led

    # Texto "Faltas" HOME
    font_size_text = int(sizes['font_label'] * modern_style.scale_factor * 0.6)
    home_fouls_text = tk.Label(
        fouls_frame,
        text="Faltas",
        font=(fonts['display'][0], font_size_text),
        fg='#FFFFFF',
        bg=colors['bg_center'],
        anchor='center'
    )
    home_fouls_text.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

    # Contador de faltas HOME (número grande pero menor que el reloj)
    # Reloj = font_time (100), Faltas = 70% del reloj = 70
    font_size_counter = int(70 * modern_style.scale_factor)
    home_fouls_counter = tk.Label(
        fouls_frame,
        text="0",
        font=(fonts['display'][0], font_size_counter, 'bold'),
        fg=colors['accent_orange'],
        bg=colors['bg_center'],
        anchor='center'
    )
    home_fouls_counter.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)

    self.match.labels.fouls.home.counter = home_fouls_counter
    
    # ═══════════════════════════════════════════════════════════
    # EQUIPO VISITANTE (AWAY) - Columna 1
    # ═══════════════════════════════════════════════════════════
    
    # Frame para BONUS AWAY
    away_bonus_frame = tk.Frame(fouls_frame, bg=colors['bg_center'])
    away_bonus_frame.grid(row=0, column=1, sticky="n", padx=2, pady=2)  # sticky="n" para alinear arriba
    
    # Label "BONUS"
    away_bonus_label = tk.Label(
        away_bonus_frame,
        text="BONUS",
        font=(fonts['display'][0], font_size_bonus, 'bold'),
        fg='#FFFFFF',
        bg=colors['bg_center'],
        anchor='center'
    )
    away_bonus_label.pack(side='left', padx=(5, 2))
    
    # LED indicador de BONUS (círculo)
    away_bonus_canvas = tk.Canvas(
        away_bonus_frame,
        width=20,
        height=20,
        bg=colors['bg_center'],
        highlightthickness=0
    )
    away_bonus_canvas.pack(side='left', padx=(2, 5))
    
    # Crear círculo LED (apagado por defecto)
    away_bonus_led = away_bonus_canvas.create_oval(
        2, 2, 18, 18,
        fill='#404040',  # Gris oscuro (apagado)
        outline='#606060',
        width=1
    )
    
    # Guardar referencias
    self.match.labels.fouls.away.bonus_canvas = away_bonus_canvas
    self.match.labels.fouls.away.bonus_led = away_bonus_led

    # Texto "Faltas" AWAY
    away_fouls_text = tk.Label(
        fouls_frame,
        text="Faltas",
        font=(fonts['display'][0], font_size_text),
        fg='#FFFFFF',
        bg=colors['bg_center'],
        anchor='center'
    )
    away_fouls_text.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)

    # Contador de faltas AWAY (número MUY grande - mismo tamaño que HOME)
    away_fouls_counter = tk.Label(
        fouls_frame,
        text="0",
        font=(fonts['display'][0], font_size_counter, 'bold'),
        fg=colors['accent_orange'],
        bg=colors['bg_center'],
        anchor='center'
    )
    away_fouls_counter.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)

    self.match.labels.fouls.away.counter = away_fouls_counter

    print("✅ Grilla de faltas y BONUS creada (2x3 - BONUS, texto, número)")


def update_fouls_display_modern(scoreboard_instance):
    """
    Actualiza la visualización de faltas y BONUS para ambos equipos.

    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    if not hasattr(scoreboard_instance.match.labels, 'fouls'):
        return

    # Actualizar equipo LOCAL (HOME)
    home_foul_manager = scoreboard_instance.match_state.home_team.foul_manager
    home_status = home_foul_manager.get_status_info()

    # Actualizar contador de faltas HOME (solo el número)
    scoreboard_instance.match.labels.fouls.home.counter.config(
        text=str(home_status['team_fouls'])
    )

    # Actualizar LED de BONUS HOME
    if home_status['is_bonus']:
        # BONUS activado: LED rojo brillante
        scoreboard_instance.match.labels.fouls.home.bonus_canvas.itemconfig(
            scoreboard_instance.match.labels.fouls.home.bonus_led,
            fill='#FF0000',  # Rojo brillante
            outline='#FF4444'
        )
    else:
        # BONUS desactivado: LED gris oscuro
        scoreboard_instance.match.labels.fouls.home.bonus_canvas.itemconfig(
            scoreboard_instance.match.labels.fouls.home.bonus_led,
            fill='#404040',  # Gris oscuro
            outline='#606060'
        )

    # Actualizar equipo VISITANTE (AWAY)
    away_foul_manager = scoreboard_instance.match_state.away_team.foul_manager
    away_status = away_foul_manager.get_status_info()

    # Actualizar contador de faltas AWAY (solo el número)
    scoreboard_instance.match.labels.fouls.away.counter.config(
        text=str(away_status['team_fouls'])
    )

    # Actualizar LED de BONUS AWAY
    if away_status['is_bonus']:
        # BONUS activado: LED rojo brillante
        scoreboard_instance.match.labels.fouls.away.bonus_canvas.itemconfig(
            scoreboard_instance.match.labels.fouls.away.bonus_led,
            fill='#FF0000',  # Rojo brillante
            outline='#FF4444'
        )
    else:
        # BONUS desactivado: LED gris oscuro
        scoreboard_instance.match.labels.fouls.away.bonus_canvas.itemconfig(
            scoreboard_instance.match.labels.fouls.away.bonus_led,
            fill='#404040',  # Gris oscuro
            outline='#606060'
        )

