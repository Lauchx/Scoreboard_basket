import tkinter as tk
from tkinter import ttk
from gui.control_panel.styles_control_panel_test import apply_styles_control_panel_test
from gui.control_panel.gui_left_control_panel import setup_left_panel

def setup_ui(self):
    """Configura toda la interfaz de usuario para gui_control_panel_test"""
    apply_styles_control_panel_test()
    setup_left_panel(self)
    
    # Configuración del grid raíz (1/6 izquierda, 5/6 derecha)
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_columnconfigure(1, weight=7)

    # Panel derecho: estructura 3x3 uniforme
    self.right_frame = ttk.Frame(self.root, style="PanelTest.TFrame")
    self.right_frame.grid(row=0, column=1, sticky="nsew")
    for r in range(3):
        self.right_frame.grid_rowconfigure(r, weight=1, uniform='rightgrid')
    for c in range(3):
        self.right_frame.grid_columnconfigure(c, weight=1, uniform='rightgrid')

    # Fila 1 - Panel de tiempo (cronómetro principal)
    setup_time_panel(self)
    
    # Fila 1 - Panel de cuarto (quarter)
    setup_quarter_panel(self)
    
    # Fila 1 - Botones de control (Iniciar / Reiniciar)
    setup_timer_buttons(self)

    # Fila 2 - Paneles de puntuación LOCAL y VISITANTE
    self._create_score_panel("local", 0, "LOCAL", "home_team")
    self._create_score_panel("visitor", 2, "VISITANTE", "away_team")
    
    # Fila 2 - Panel central: botones arriba, flecha abajo
    setup_action_panel(self)

    self.update_time_label()
    
    # Fila 3 - Paneles de faltas LOCAL y VISITANTE
    self._create_fouls_panel("local", 0, "FALTAS LOCAL", "home_team")
    self._create_fouls_panel("visitor", 2, "FALTAS VISITANTE", "away_team")
    
    # Fila 3 - Panel central: botón "Borrar faltas"
    setup_clear_fouls_panel(self)

def setup_time_panel(self):
    """Configura el panel de tiempo (cronómetro)"""
    self.time_container = ttk.Frame(self.right_frame, style="PanelTestTime.TFrame")
    self.time_container.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    self.time_container.grid_rowconfigure(0, weight=0)
    self.time_container.grid_rowconfigure(1, weight=1)
    self.time_container.grid_columnconfigure(0, weight=1)

    self.label_tiempo = ttk.Label(self.time_container, text="TIEMPO", style="PanelTestTimeTitle.TLabel", anchor="center")
    self.label_tiempo.grid(row=0, column=0, sticky="ew", pady=(2, 0))

    self.time_label = ttk.Label(self.time_container, text="00:00", style="PanelTestTime.TLabel", anchor="center")
    self.time_label.grid(row=1, column=0, sticky="nsew", pady=(0, 2))

def setup_quarter_panel(self):
    """Configura el panel de cuartos"""
    self.quarter_panel = ttk.Frame(self.right_frame, style="PanelTestQuarter.TFrame")
    self.quarter_panel.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
    self.quarter_panel.grid_rowconfigure(0, weight=1)
    self.quarter_panel.grid_columnconfigure(0, weight=1)

    quarter_content = ttk.Frame(self.quarter_panel)
    quarter_content.grid(row=0, column=0, sticky="nsew")
    quarter_content.grid_rowconfigure(0, weight=1)
    quarter_content.grid_columnconfigure(0, weight=1)

    self.quarter_panel_title = ttk.Label(quarter_content, text="CUARTO", style="PanelTestQuarterTitle.TLabel")
    self.quarter_panel_title.pack(pady=(6, 6))

    self.quarter_panel_label = ttk.Label(
        quarter_content,
        text=str(getattr(self.match_state_controller.match_state, 'quarter', 1)),
        style="PanelTestQuarter.TLabel"
    )
    self.quarter_panel_label.pack(pady=(4, 4))

    qbtns = ttk.Frame(quarter_content)
    qbtns.pack()

    self.quarter_minus_btn = ttk.Button(qbtns, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: self._quarter_minus())
    self.quarter_minus_btn.pack(side='left', padx=4)

    self.quarter_plus_btn = ttk.Button(qbtns, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: self._quarter_plus())
    self.quarter_plus_btn.pack(side='left', padx=4)

def setup_timer_buttons(self):
    """Configura los botones de control del temporizador (Iniciar / Reiniciar)"""
    self.button_container = ttk.Frame(self.right_frame, style="ControlPanel.Stack.TFrame")
    self.button_container.grid(row=0, column=1, sticky="n", padx=6, pady=6)

    self.buttons_inner = ttk.Frame(self.button_container, style="ControlPanel.Stack.TFrame")
    self.buttons_inner.pack(anchor="center", pady=10)

    self.btn_iniciar = ttk.Button(self.buttons_inner, text="Iniciar", style="ControlPanel.Button.TButton", command=lambda: self._manage_timer())
    self.btn_reiniciar = ttk.Button(self.buttons_inner, text="Reiniciar", style="ControlPanel.Button.TButton", command=lambda: self._reset_timer())

    self.btn_iniciar.pack(side="top", pady=6)
    self.btn_reiniciar.pack(side="top", pady=6)

def setup_action_panel(self):
    """Configura el panel central con botones de acción y indicador de posesión"""
    self.action_panel = ttk.Frame(self.right_frame, style="ControlPanel.Stack.TFrame")
    self.action_panel.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)

    self.action_panel.grid_rowconfigure(0, weight=1)
    self.action_panel.grid_rowconfigure(1, weight=1)
    self.action_panel.grid_columnconfigure(0, weight=1)

    self.action_buttons = ttk.Frame(self.action_panel, style="ControlPanel.Stack.TFrame")
    self.action_buttons.grid(row=0, column=0, sticky="n", pady=(10, 0))

    self.btn_borrar_puntos = ttk.Button(
        self.action_buttons,
        text="Borrar puntos",
        style="ControlPanel.Button.TButton",
        command=lambda: self._clear_points()
    )
    self.btn_cambiar_posesion = ttk.Button(
        self.action_buttons,
        text="Cambiar posesión",
        style="ControlPanel.Button.TButton",
        command=lambda: self._change_possession()
    )

    self.btn_borrar_puntos.pack(side="top", pady=6)
    self.btn_cambiar_posesion.pack(side="top", pady=6)

    # Flecha abajo (indicador de posesión)
    self.possession_indicator = ttk.Frame(self.action_panel)
    self.possession_indicator.grid(row=1, column=0, sticky="ew", pady=(0, 10))
    self.possession_indicator.grid_columnconfigure(0, weight=1)

    self.possession_label = ttk.Label(
        self.possession_indicator,
        text="-",  # Valor inicial (neutral, como el scoreboard)
        style="PanelTestScore.TLabel",
        anchor="center"  
    )
    self.possession_label.pack(fill="x", expand=True)

def setup_clear_fouls_panel(self):
    """Configura el panel del botón de limpiar faltas"""
    self.clear_fouls_panel = ttk.Frame(self.right_frame, style="ControlPanel.Stack.TFrame")
    self.clear_fouls_panel.grid(row=2, column=1, sticky="n", padx=6, pady=6)

    self.clear_fouls_inner = ttk.Frame(self.clear_fouls_panel, style="ControlPanel.Stack.TFrame")
    self.clear_fouls_inner.pack(anchor="center", pady=10)

    self.clear_fouls_button = ttk.Button(
        self.clear_fouls_inner,
        text="Borrar faltas",
        style="ControlPanel.ClearFouls.TButton",  
        command=lambda: self._clear_fouls()
    )
    self.clear_fouls_button.pack(side="top", pady=6)
