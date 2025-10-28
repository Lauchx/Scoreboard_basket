import tkinter as tk
from tkinter import ttk
from gui.control_panel.styles_control_panel_test import apply_styles_control_panel_test


class Gui_control_panel_test:
    def __init__(self, root, match_state_controller, main_panel=None):
        self.root = root
        self.root.title("ControlPanelTest")
        self.root.configure(bg="white")
        self.root.minsize(900, 600)
        self.match_state_controller = match_state_controller

        self.main_panel = main_panel

        apply_styles_control_panel_test()

        # Configurar el grid raíz (1/6 izquierda y 5/6 derecha)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=7)

        # Frame izquierdo (1/6): panel de jugadores con pestañas
        self.left_frame = ttk.Frame(self.root, style="PanelTestLeft.TFrame")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.notebook = ttk.Notebook(self.left_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        self.tab_jugadores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_jugadores, text="Jugadores")
        self.tab_ajustes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ajustes, text="Ajustes")

        # Frame derecho (5/6): divide en 3x3 uniforme
        self.right_frame = ttk.Frame(self.root, style="PanelTest.TFrame")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        for r in range(3):
            self.right_frame.grid_rowconfigure(r, weight=1, uniform='rightgrid')
        for c in range(3):
            self.right_frame.grid_columnconfigure(c, weight=1, uniform='rightgrid')

        # ---------------- FILA 1 ----------------
        # Contenedor del tiempo (row=0, col=0)
        self.time_container = ttk.Frame(self.right_frame, style="PanelTestTime.TFrame")
        self.time_container.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.label_tiempo = ttk.Label(self.time_container, text="TIEMPO", style="PanelTestTimeTitle.TLabel")
        self.label_tiempo.pack(side="top", fill="x", pady=(2, 0))
        self.time_label = ttk.Label(self.time_container, text="00:00", style="PanelTestTime.TLabel")
        self.time_label.pack(side="top", fill='both', expand=True, pady=(0, 2))

       # ---------------- quarter (row=0, col=2) ----------------
        self.quarter_panel = ttk.Frame(self.right_frame, style="PanelTestQuarter.TFrame")
        self.quarter_panel.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)

        # Permitir que el panel se expanda y distribuya espacio
        self.quarter_panel.grid_rowconfigure(0, weight=1)
        self.quarter_panel.grid_columnconfigure(0, weight=1)

        # Contenedor centrado dentro del panel
        quarter_content = ttk.Frame(self.quarter_panel)
        quarter_content.grid(row=0, column=0, sticky="nsew")  # ← centrado total

        # Centrado interno vertical
        quarter_content.grid_rowconfigure(0, weight=1)
        quarter_content.grid_columnconfigure(0, weight=1)

        # Título del cuarto
        self.quarter_panel_title = ttk.Label(quarter_content, text="CUARTO", style="PanelTestQuarterTitle.TLabel")
        self.quarter_panel_title.pack(pady=(6, 6))

        # Número del cuarto
        self.quarter_panel_label = ttk.Label(
            quarter_content,
            text=str(getattr(self.match_state_controller.match_state, 'quarter', 1)),
            style="PanelTestQuarter.TLabel"
        )
        self.quarter_panel_label.pack(pady=(4, 4))

        # Botones + y -
        qbtns = ttk.Frame(quarter_content)
        qbtns.pack()

        self.quarter_minus_btn = ttk.Button(qbtns, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: None)
        self.quarter_minus_btn.pack(side='left', padx=4)

        self.quarter_plus_btn = ttk.Button(qbtns, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: None)
        self.quarter_plus_btn.pack(side='left', padx=4)

        # ---------------- botones de control (row=0, col=1) ----------------
        # Mantener tamaño natural (no fill expand)
        self.button_container = ttk.Frame(self.right_frame, style="ControlPanel.Stack.TFrame")
        self.button_container.grid(row=0, column=1, sticky="n", padx=6, pady=6)
        self.buttons_inner = ttk.Frame(self.button_container, style="ControlPanel.Stack.TFrame")
        self.buttons_inner.pack(anchor="center", pady=10)
        self.btn_iniciar = ttk.Button(self.buttons_inner, text="Iniciar", style="ControlPanel.Button.TButton", command=lambda: None)
        self.btn_reiniciar = ttk.Button(self.buttons_inner, text="Reiniciar", style="ControlPanel.Button.TButton", command=lambda: None)
        # No usar fill='x' para conservar ancho natural
        self.btn_iniciar.pack(side="top", pady=6)
        self.btn_reiniciar.pack(side="top", pady=6)

        # ---------------- FILA 2: PUNTOS ----------------
        # Local (row=1, col=0)
        self.local_score_panel = ttk.Frame(self.right_frame, style="PanelTestScore.TFrame")
        self.local_score_panel.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.local_score_title = ttk.Label(self.local_score_panel, text="LOCAL", style="PanelTestScoreTitle.TLabel")
        self.local_score_title.pack(side="top", pady=(2, 0))
        try:
            home_team = getattr(self.match_state_controller.match_state, 'home_team', None)
            home_points = getattr(home_team, 'points', 0) if home_team is not None else 0
        except Exception:
            home_points = 0
        self.local_score_label = ttk.Label(self.local_score_panel, text=str(home_points), style="PanelTestScore.TLabel")
        # Mantener tamaño natural; reservar espacio para botones +/- que se agregarán luego
        self.local_score_label.pack(side="top", pady=(6, 4))
        self.local_score_buttons = ttk.Frame(self.local_score_panel)
        self.local_score_buttons.pack(side="top")

        # Centro vacío (row=1, col=1) reservado

        # Visitante (row=1, col=2)
        self.visitor_score_panel = ttk.Frame(self.right_frame, style="PanelTestScore.TFrame")
        self.visitor_score_panel.grid(row=1, column=2, sticky="nsew", padx=6, pady=6)
        self.visitor_score_title = ttk.Label(self.visitor_score_panel, text="VISITANTE", style="PanelTestScoreTitle.TLabel")
        self.visitor_score_title.pack(side="top", pady=(2, 0))
        try:
            away_team = getattr(self.match_state_controller.match_state, 'away_team', None)
            away_points = getattr(away_team, 'points', 0) if away_team is not None else 0
        except Exception:
            away_points = 0
        self.visitor_score_label = ttk.Label(self.visitor_score_panel, text=str(away_points), style="PanelTestScore.TLabel")
        self.visitor_score_label.pack(side="top", pady=(6, 4))
        self.visitor_score_buttons = ttk.Frame(self.visitor_score_panel)
        self.visitor_score_buttons.pack(side="top")

        # Inicializar valores visuales
        self.update_time_label()

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
