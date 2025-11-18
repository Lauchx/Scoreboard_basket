import tkinter as tk
from tkinter import ttk
from gui.control_panel.gui_control_panel_test_ui import setup_ui

class Gui_control_panel_test:
    def __init__(self, root, match_state_controller, main_panel=None):
        self.root = root
        self.root.title("ControlPanelTest")
        self.root.configure(bg="white")
        self.root.minsize(675, 540)
        self.match_state_controller = match_state_controller
        self.main_panel = main_panel
        self.is_active_timer = None  

        setup_ui(self)

    def _create_score_panel(self, team_type, column, title, team_attr):
        panel = ttk.Frame(self.right_frame, style="PanelTestScore.TFrame")
        panel.grid(row=1, column=column, sticky="nsew", padx=6, pady=6)
        panel.grid_rowconfigure(0, weight=0)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_rowconfigure(2, weight=0)
        panel.grid_columnconfigure(0, weight=1)

        ttk.Label(panel, text=title, style="PanelTestScoreTitle.TLabel", anchor="center").grid(row=0, column=0, sticky="ew", pady=(2, 0))

        # Obtener puntos de forma segura
        try:
            team = getattr(self.match_state_controller.match_state, team_attr, None)
            points = getattr(team, 'points', 0) if team is not None else 0
        except Exception:
            points = 0

        score_label = ttk.Label(panel, text=str(points), style="PanelTestScore.TLabel", anchor="center")
        score_label.grid(row=1, column=0, sticky="nsew", pady=(6, 4))

        # Botones de puntos
        buttons_frame = ttk.Frame(panel)
        buttons_frame.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        buttons_inner = ttk.Frame(buttons_frame)
        buttons_inner.pack(anchor="center")

        # Obtener el controlador de equipo correspondiente
        if team_type == "local":
            team_controller = self.match_state_controller.home_team_controller
        else:  # visitor
            team_controller = self.match_state_controller.away_team_controller

        minus_btn = ttk.Button(buttons_inner, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: self._subtract_point(team_type, score_label, team_controller))
        plus_btn = ttk.Button(buttons_inner, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: self._add_point(team_type, score_label, team_controller))
        minus_btn.pack(side='left', padx=4)
        plus_btn.pack(side='left', padx=4)

        # Guardar referencias
        setattr(self, f"{team_type}_score_panel", panel)
        setattr(self, f"{team_type}_score_label", score_label)
        setattr(self, f"{team_type}_minus_btn", minus_btn)
        setattr(self, f"{team_type}_plus_btn", plus_btn)

    def _create_fouls_panel(self, team_type, column, title, team_attr):
        container = ttk.Frame(self.right_frame)
        container.grid(row=2, column=column, sticky="nsew", padx=6, pady=6)

        ttk.Label(container, text=title, style="PanelFoulsTitle.TLabel").pack(side="top", pady=(2, 0))

        fouls_panel = ttk.Frame(container, style="PanelFouls.TFrame")
        fouls_panel.pack(fill="x", expand=False, pady=(4, 0), ipadx=4, ipady=4)

        # Obtener faltas de forma segura
        try:
            team = getattr(self.match_state_controller.match_state, team_attr, None)
            fouls = getattr(team, 'fouls', 0) if team is not None else 0
        except Exception:
            fouls = 0

        fouls_label = ttk.Label(fouls_panel, text=str(fouls), style="PanelFouls.TLabel")
        fouls_label.pack(anchor="center", pady=(4, 2))

        # Botones de control
        buttons_frame = ttk.Frame(fouls_panel)
        buttons_frame.pack(side="bottom", fill="x", pady=(2, 0))

        buttons_inner = ttk.Frame(buttons_frame)
        buttons_inner.pack(anchor="center")

        # Obtener el controlador de equipo correspondiente
        if team_type == "local":
            team_controller = self.match_state_controller.home_team_controller
        else:  # visitor
            team_controller = self.match_state_controller.away_team_controller

        minus_btn = ttk.Button(buttons_inner, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: self._subtract_foul(team_type, fouls_label, team_controller))
        plus_btn = ttk.Button(buttons_inner, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: self._add_foul(team_type, fouls_label, team_controller))
        minus_btn.pack(side='left', padx=4)
        plus_btn.pack(side='left', padx=4)

        # Guardar referencias
        setattr(self, f"{team_type}_fouls_container", container)
        setattr(self, f"{team_type}_fouls_label", fouls_label)
        setattr(self, f"{team_type}_fouls_minus_btn", minus_btn)
        setattr(self, f"{team_type}_fouls_plus_btn", plus_btn)


    def update_time_label(self, force=False):
        """Actualiza los labels de tiempo y cuarto"""
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

    def _update_score_label(self, score_label, team_controller):
        """Actualiza el label de puntos con el valor actual"""
        try:
            points = getattr(team_controller.team, 'points', 0)
            score_label.config(text=str(points))
        except Exception:
            pass

    def _update_fouls_labels(self):
        """Actualiza los labels de faltas con los valores actuales"""
        try:
            local_fouls = getattr(self.match_state_controller.home_team_controller.team, 'fouls', 0)
            local_fouls_label = getattr(self, 'local_fouls_label', None)
            if local_fouls_label:
                local_fouls_label.config(text=str(local_fouls))
        except Exception:
            pass
        
        try:
            visitor_fouls = getattr(self.match_state_controller.away_team_controller.team, 'fouls', 0)
            visitor_fouls_label = getattr(self, 'visitor_fouls_label', None)
            if visitor_fouls_label:
                visitor_fouls_label.config(text=str(visitor_fouls))
        except Exception:
            pass

    def _update_score_labels(self):
        """Actualiza los labels de puntos con los valores actuales"""
        try:
            local_points = getattr(self.match_state_controller.home_team_controller.team, 'points', 0)
            local_score_label = getattr(self, 'local_score_label', None)
            if local_score_label:
                local_score_label.config(text=str(local_points))
        except Exception:
            pass
        
        try:
            visitor_points = getattr(self.match_state_controller.away_team_controller.team, 'points', 0)
            visitor_score_label = getattr(self, 'visitor_score_label', None)
            if visitor_score_label:
                visitor_score_label.config(text=str(visitor_points))
        except Exception:
            pass
    def _manage_timer(self):
        """Inicia/pausa el temporizador sincronizado con scoreboard"""
        if self.is_active_timer is not None:
            self.is_active_timer = not self.is_active_timer
            if self.is_active_timer:
                self._timer_tick()
        else:
            self.is_active_timer = True
            self._timer_tick()
        
        text = "Pausar" if self.is_active_timer else "Reanudar"
        self.btn_iniciar.config(text=text)

    def _timer_tick(self):
        """Decrementa el tiempo y sincroniza con scoreboard cada segundo"""
        seconds_left = getattr(self.match_state_controller.match_state, 'seconds_time_left', 0)
        if seconds_left > 0 and self.is_active_timer:
            self.match_state_controller.match_state.seconds_time_left -= 1
            self.update_time_label(force=True)
            if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
                self.main_panel.scoreboard_window.update_time_labels()
            self.root.after(1000, self._timer_tick)

    def _reset_timer(self):
        """Reinicia el temporizador al valor original"""
        if self.match_state_controller and hasattr(self.match_state_controller, 'match_state'):
            match_state = self.match_state_controller.match_state
            match_state.seconds_time_left = getattr(match_state, 'seconds_match_time', 900)
            if self.is_active_timer:
                self.is_active_timer = False
                self.btn_iniciar.config(text="Iniciar")
            self.update_time_label(force=True)
            if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
                self.main_panel.scoreboard_window.update_time_labels()


    def _quarter_plus(self):
        """Incrementa el cuarto y sincroniza con scoreboard"""
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_quarter_labels(1)
            self.update_time_label(force=True)

    def _quarter_minus(self):
        """Decrementa el cuarto y sincroniza con scoreboard"""
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_quarter_labels(-1)
            self.update_time_label(force=True)

    def _add_point(self, team_type, score_label, team_controller):
        """Suma un punto al equipo y sincroniza con scoreboard"""
        team_controller.add_point()
        self._update_score_label(score_label, team_controller)
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_points_labels()

    def _subtract_point(self, team_type, score_label, team_controller):
        """Resta un punto al equipo y sincroniza con scoreboard"""
        team_controller.substract_point()
        self._update_score_label(score_label, team_controller)
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_points_labels()

    def _clear_points(self):
        """Limpia los puntos de ambos equipos y sincroniza con scoreboard"""
        self.match_state_controller.home_team_controller.team.points = 0
        self.match_state_controller.away_team_controller.team.points = 0
        self._update_score_labels()
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_points_labels()

    # ============= MÉTODOS DE FALTAS =============

    def _add_foul(self, team_type, fouls_label, team_controller):
        """Suma una falta al equipo y sincroniza con scoreboard"""
        team_controller.add_foul()
        self._update_fouls_label(fouls_label, team_controller)
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_fouls_labels()

    def _subtract_foul(self, team_type, fouls_label, team_controller):
        """Resta una falta al equipo y sincroniza con scoreboard"""
        team_controller.substract_foul()
        self._update_fouls_label(fouls_label, team_controller)
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_fouls_labels()

    def _update_fouls_label(self, fouls_label, team_controller):
        """Actualiza el label de faltas con el valor actual"""
        try:
            fouls = getattr(team_controller.team, 'fouls', 0)
            fouls_label.config(text=str(fouls))
        except Exception:
            pass

    def _clear_fouls(self):
        """Limpia las faltas de ambos equipos y sincroniza con scoreboard"""
        self.match_state_controller.home_team_controller.team.fouls = 0
        self.match_state_controller.away_team_controller.team.fouls = 0
        self._update_fouls_labels()
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_fouls_labels()

    # ============= MÉTODOS DE POSESIÓN =============

    def _change_possession(self):
        """Cambia la posesión de un equipo a otro y sincroniza con scoreboard"""
        if self.main_panel and hasattr(self.main_panel, 'scoreboard_window'):
            self.main_panel.scoreboard_window.update_possession_labels()
            self._update_possession_label()

    def _update_possession_label(self):
        """Actualiza el label de posesión con el valor actual"""
        try:
            possession = getattr(self.match_state_controller.match_state, 'possession', 'Home')
            text = "⇦" if possession == "Home" else "⇨"
            if hasattr(self, 'possession_label'):
                self.possession_label.config(text=text)
        except Exception:
            pass


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
