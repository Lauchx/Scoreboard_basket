import tkinter as tk
from tkinter import ttk
from gui.control_panel.styles_control_panel_test import apply_styles_control_panel_test
from gui.control_panel.gui_left_control_panel import setup_left_panel

class Gui_control_panel_test:
    def __init__(self, root, match_state_controller, main_panel=None):
        self.root = root
        self.root.title("ControlPanelTest")
        self.root.configure(bg="white")
        self.root.minsize(900, 600)
        self.match_state_controller = match_state_controller
        self.main_panel = main_panel

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
        self.time_container = ttk.Frame(self.right_frame, style="PanelTestTime.TFrame")
        self.time_container.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.time_container.grid_rowconfigure(0, weight=0)
        self.time_container.grid_rowconfigure(1, weight=1)
        self.time_container.grid_columnconfigure(0, weight=1)

        self.label_tiempo = ttk.Label(self.time_container, text="TIEMPO", style="PanelTestTimeTitle.TLabel", anchor="center")
        self.label_tiempo.grid(row=0, column=0, sticky="ew", pady=(2, 0))

        self.time_label = ttk.Label(self.time_container, text="00:00", style="PanelTestTime.TLabel", anchor="center")
        self.time_label.grid(row=1, column=0, sticky="nsew", pady=(0, 2))

        # Fila 1 - Panel de cuarto (quarter)
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

        self.quarter_minus_btn = ttk.Button(qbtns, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: None)
        self.quarter_minus_btn.pack(side='left', padx=4)

        self.quarter_plus_btn = ttk.Button(qbtns, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: None)
        self.quarter_plus_btn.pack(side='left', padx=4)

        # Fila 1 - Botones de control (Iniciar / Reiniciar)
        self.button_container = ttk.Frame(self.right_frame, style="ControlPanel.Stack.TFrame")
        self.button_container.grid(row=0, column=1, sticky="n", padx=6, pady=6)

        self.buttons_inner = ttk.Frame(self.button_container, style="ControlPanel.Stack.TFrame")
        self.buttons_inner.pack(anchor="center", pady=10)

        self.btn_iniciar = ttk.Button(self.buttons_inner, text="Iniciar", style="ControlPanel.Button.TButton", command=lambda: None)
        self.btn_reiniciar = ttk.Button(self.buttons_inner, text="Reiniciar", style="ControlPanel.Button.TButton", command=lambda: None)

        self.btn_iniciar.pack(side="top", pady=6)
        self.btn_reiniciar.pack(side="top", pady=6)

        # Fila 2 - Panel de puntuación LOCAL
        self.local_score_panel = ttk.Frame(self.right_frame, style="PanelTestScore.TFrame")
        self.local_score_panel.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.local_score_panel.grid_rowconfigure(0, weight=0)
        self.local_score_panel.grid_rowconfigure(1, weight=1)
        self.local_score_panel.grid_rowconfigure(2, weight=0)
        self.local_score_panel.grid_columnconfigure(0, weight=1)

        self.local_score_title = ttk.Label(self.local_score_panel, text="LOCAL", style="PanelTestScoreTitle.TLabel", anchor="center")
        self.local_score_title.grid(row=0, column=0, sticky="ew", pady=(2, 0))

        try:
            home_team = getattr(self.match_state_controller.match_state, 'home_team', None)
            home_points = getattr(home_team, 'points', 0) if home_team is not None else 0
        except Exception:
            home_points = 0

        self.local_score_label = ttk.Label(self.local_score_panel, text=str(home_points), style="PanelTestScore.TLabel", anchor="center")
        self.local_score_label.grid(row=1, column=0, sticky="nsew", pady=(6, 4))

        self.local_score_buttons = ttk.Frame(self.local_score_panel)
        self.local_score_buttons.grid(row=2, column=0, sticky="ew", pady=(4, 0))

        self.local_buttons_inner = ttk.Frame(self.local_score_buttons)
        self.local_buttons_inner.pack(anchor="center")

        self.local_minus_btn = ttk.Button(
            self.local_buttons_inner,
            text='-',
            width=3,
            style="ControlPanel.Minus.TButton",
            command=lambda: None
        )
        self.local_minus_btn.pack(side='left', padx=4)

        self.local_plus_btn = ttk.Button(
            self.local_buttons_inner,
            text='+',
            width=3,
            style="ControlPanel.Plus.TButton",
            command=lambda: None
        )
        self.local_plus_btn.pack(side='left', padx=4)
        
        # Fila 2 - Panel de puntuación VISITANTE
        self.visitor_score_panel = ttk.Frame(self.right_frame, style="PanelTestScore.TFrame")
        self.visitor_score_panel.grid(row=1, column=2, sticky="nsew", padx=6, pady=6)
        self.visitor_score_panel.grid_rowconfigure(0, weight=0)
        self.visitor_score_panel.grid_rowconfigure(1, weight=1)
        self.visitor_score_panel.grid_rowconfigure(2, weight=0)
        self.visitor_score_panel.grid_columnconfigure(0, weight=1)

        self.visitor_score_title = ttk.Label(self.visitor_score_panel, text="VISITANTE", style="PanelTestScoreTitle.TLabel", anchor="center")
        self.visitor_score_title.grid(row=0, column=0, sticky="ew", pady=(2, 0))

        try:
            away_team = getattr(self.match_state_controller.match_state, 'away_team', None)
            away_points = getattr(away_team, 'points', 0) if away_team is not None else 0
        except Exception:
            away_points = 0

        self.visitor_score_label = ttk.Label(self.visitor_score_panel, text=str(away_points), style="PanelTestScore.TLabel", anchor="center")
        self.visitor_score_label.grid(row=1, column=0, sticky="nsew", pady=(6, 4))

        self.visitor_score_buttons = ttk.Frame(self.visitor_score_panel)
        self.visitor_score_buttons.grid(row=2, column=0, sticky="ew", pady=(4, 0))

        self.visitor_buttons_inner = ttk.Frame(self.visitor_score_buttons)
        self.visitor_buttons_inner.pack(anchor="center")

        self.visitor_minus_btn = ttk.Button(
            self.visitor_buttons_inner,
            text='-',
            width=3,
            style="ControlPanel.Minus.TButton",
            command=lambda: None
        )
        self.visitor_minus_btn.pack(side='left', padx=4)

        self.visitor_plus_btn = ttk.Button(
            self.visitor_buttons_inner,
            text='+',
            width=3,
            style="ControlPanel.Plus.TButton",
            command=lambda: None
        )
        self.visitor_plus_btn.pack(side='left', padx=4)
        
        # Fila 2 - Panel central: botones arriba, flecha abajo
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
            command=lambda: None
        )
        self.btn_cambiar_posesion = ttk.Button(
            self.action_buttons,
            text="Cambiar posesión",
            style="ControlPanel.Button.TButton",
            command=lambda: None
        )

        self.btn_borrar_puntos.pack(side="top", pady=6)
        self.btn_cambiar_posesion.pack(side="top", pady=6)

        # 🔽 Flecha abajo
        self.possession_indicator = ttk.Frame(self.action_panel)
        self.possession_indicator.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.possession_indicator.grid_columnconfigure(0, weight=1)

        self.possession_label = ttk.Label(
            self.possession_indicator,
            text="⇨",  # Valor inicial
            style="PanelTestScore.TLabel",
            anchor="center"  # Asegura que el texto esté centrado
        )
        self.possession_label.pack(fill="x", expand=True)

        # Inicializar valores visuales
        self.update_time_label()
        
        # Fila 3 - Panel de faltas LOCAL

        # Contenedor general (sin fondo negro)
        self.local_fouls_container = ttk.Frame(self.right_frame)
        self.local_fouls_container.grid(row=2, column=0, sticky="nsew", padx=6, pady=6)

        # Título fuera del fondo negro
        self.local_fouls_title = ttk.Label(
            self.local_fouls_container,
            text="FALTAS LOCAL",
            style="PanelFoulsTitle.TLabel"
        )
        self.local_fouls_title.pack(side="top", pady=(2, 0))

        # Subpanel negro más chico
        self.local_fouls_panel = ttk.Frame(self.local_fouls_container, style="PanelFouls.TFrame")
        self.local_fouls_panel.pack(fill="x", expand=False, pady=(4, 0), ipadx=4, ipady=4)

        # Valor inicial de faltas
        try:
            home_team = getattr(self.match_state_controller.match_state, 'home_team', None)
            home_fouls = getattr(home_team, 'fouls', 0) if home_team is not None else 0
        except Exception:
            home_fouls = 0

        self.local_fouls_label = ttk.Label(
            self.local_fouls_panel,
            text=str(home_fouls),
            style="PanelFouls.TLabel"
        )
        self.local_fouls_label.pack(anchor="center", pady=(4, 2))

        # Botones de control
        self.local_fouls_buttons = ttk.Frame(self.local_fouls_panel)
        self.local_fouls_buttons.pack(side="bottom", fill="x", pady=(2, 0))

        self.local_fouls_inner = ttk.Frame(self.local_fouls_buttons)
        self.local_fouls_inner.pack(anchor="center")

        self.local_fouls_minus_btn = ttk.Button(
            self.local_fouls_inner,
            text='-',
            width=3,
            style="ControlPanel.Minus.TButton",
            command=lambda: None
        )
        self.local_fouls_minus_btn.pack(side='left', padx=4)

        self.local_fouls_plus_btn = ttk.Button(
            self.local_fouls_inner,
            text='+',
            width=3,
            style="ControlPanel.Plus.TButton",
            command=lambda: None
        )
        self.local_fouls_plus_btn.pack(side='left', padx=4)
        
        # Fila 3 - Panel de faltas VISITANTE

        # Contenedor general (sin fondo negro)
        self.visitor_fouls_container = ttk.Frame(self.right_frame)
        self.visitor_fouls_container.grid(row=2, column=2, sticky="nsew", padx=6, pady=6)

        # Título fuera del fondo negro
        self.visitor_fouls_title = ttk.Label(
            self.visitor_fouls_container,
            text="FALTAS VISITANTE",
            style="PanelFoulsTitle.TLabel"
        )
        self.visitor_fouls_title.pack(side="top", pady=(2, 0))

        # Subpanel negro más chico
        self.visitor_fouls_panel = ttk.Frame(self.visitor_fouls_container, style="PanelFouls.TFrame")
        self.visitor_fouls_panel.pack(fill="x", expand=False, pady=(4, 0), ipadx=4, ipady=4)

        # Valor inicial de faltas
        try:
            away_team = getattr(self.match_state_controller.match_state, 'away_team', None)
            away_fouls = getattr(away_team, 'fouls', 0) if away_team is not None else 0
        except Exception:
            away_fouls = 0

        self.visitor_fouls_label = ttk.Label(
            self.visitor_fouls_panel,
            text=str(away_fouls),
            style="PanelFouls.TLabel"
        )
        self.visitor_fouls_label.pack(anchor="center", pady=(4, 2))

        # Botones de control
        self.visitor_fouls_buttons = ttk.Frame(self.visitor_fouls_panel)
        self.visitor_fouls_buttons.pack(side="bottom", fill="x", pady=(2, 0))

        self.visitor_fouls_inner = ttk.Frame(self.visitor_fouls_buttons)
        self.visitor_fouls_inner.pack(anchor="center")

        self.visitor_fouls_minus_btn = ttk.Button(
            self.visitor_fouls_inner,
            text='-',
            width=3,
            style="ControlPanel.Minus.TButton",
            command=lambda: None
        )
        self.visitor_fouls_minus_btn.pack(side='left', padx=4)

        self.visitor_fouls_plus_btn = ttk.Button(
            self.visitor_fouls_inner,
            text='+',
            width=3,
            style="ControlPanel.Plus.TButton",
            command=lambda: None
        )
        self.visitor_fouls_plus_btn.pack(side='left', padx=4)
        
        # Fila 3 - Panel central: botón "Borrar faltas"
        self.clear_fouls_panel = ttk.Frame(self.right_frame, style="ControlPanel.Stack.TFrame")
        self.clear_fouls_panel.grid(row=2, column=1, sticky="n", padx=6, pady=6)

        self.clear_fouls_inner = ttk.Frame(self.clear_fouls_panel, style="ControlPanel.Stack.TFrame")
        self.clear_fouls_inner.pack(anchor="center", pady=10)

        self.clear_fouls_button = ttk.Button(
            self.clear_fouls_inner,
            text="Borrar faltas",
            style="ControlPanel.ClearFouls.TButton",  # Estilo exclusivo
            command=lambda: None
        )
        self.clear_fouls_button.pack(side="top", pady=6)

        ##codigo##

    def update_time_label(self, force=False):
        try:
            if getattr(self, 'time_label', None) and getattr(self.match_state_controller, 'match_state', None):
                seconds_left = getattr(self.match_state_controller.match_state, 'seconds_time_left', 0)
                minutes = seconds_left // 60
                seconds = seconds_left % 60
                self.time_label.config(text=f"{minutes:02}:{seconds:02}")
        except Exception:
            pass
        try:
            quarter = getattr(self.match_state_controller.match_state, 'quarter', None)
            if quarter is not None and getattr(self, 'quarter_panel_label', None):
                self.quarter_panel_label.config(text=str(quarter))
            if quarter is not None and getattr(self, 'quarter_label', None):
                self.quarter_label.config(text=str(quarter))
        except Exception:
            pass

    # Placeholders para acciones de los botones
    def start_action(self):
        return

    def pause_action(self):
        pass

    def reset_action(self):
        return

    def _timer_tick(self):
        return

    def _quarter_plus(self):
        return

    def _quarter_minus(self):
        return


if __name__ == "__main__":
    # Minimal stub to run the window for visual testing
    class _StubMatchState:
        def __init__(self):
            self.seconds_time_left = 0
            self.quarter = 1
            from model.team import Team
            self.home_team = Team("", "Equipo Local", 0, 12, [], 3)
            self.away_team = Team("", "Equipo Visitante", 0, 8, [], 3)

    class _StubController:
        def __init__(self):
            self.match_state = _StubMatchState()

    root = tk.Tk()
    stub = _StubController()
    app = Gui_control_panel_test(root, stub)
    root.mainloop()
