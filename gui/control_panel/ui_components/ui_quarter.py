from tkinter import ttk

def setup_quarter_panel(self, parent_frame):
    """Configura el panel de cuartos"""
    self.frames.match.quarter = ttk.Frame(parent_frame, style="PanelTestQuarter.TFrame")
    self.frames.match.quarter.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
    self.frames.match.quarter.grid_rowconfigure(0, weight=1)
    self.frames.match.quarter.grid_columnconfigure(0, weight=1)

    quarter_content = ttk.Frame(self.frames.match.quarter)
    quarter_content.grid(row=0, column=0, sticky="nsew")
    quarter_content.grid_rowconfigure(0, weight=1)
    quarter_content.grid_columnconfigure(0, weight=1)

    ttk.Label(quarter_content, text="CUARTO", style="PanelTestQuarterTitle.TLabel").pack(pady=(6, 6))

    self.match.quarter_label = ttk.Label(
        quarter_content,
        text=str(self.match_state_controller.match_state.quarter),
        style="PanelTestQuarter.TLabel"
    )
    self.match.quarter_label.pack(pady=(4, 4))

    qbtns = ttk.Frame(quarter_content)
    qbtns.pack()

    ttk.Button(qbtns, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: substract_quarter(self)).pack(side='left', padx=4)
    ttk.Button(qbtns, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: add_quarter(self)).pack(side='left', padx=4)

def add_quarter(self):
    self.scoreboard_window.update_quarter_labels(1)
    update_quarter_label(self)
    # Actualizar los timeouts para el nuevo cuarto
    update_timeouts_for_quarter_change(self)
    # Actualizar las faltas para el nuevo cuarto (resetear contador de equipo y bonus)
    update_fouls_for_quarter_change(self)
    # Reiniciar el formateador de tiempo (nuevo cuarto = formato normal)
    self.scoreboard_window.time_formatter.reset()
    self.scoreboard_window.update_time_labels()


def substract_quarter(self):
    self.scoreboard_window.update_quarter_labels(-1)
    update_quarter_label(self)
    # Actualizar los timeouts para el nuevo cuarto
    update_timeouts_for_quarter_change(self)
    # Actualizar las faltas para el nuevo cuarto (resetear contador de equipo y bonus)
    update_fouls_for_quarter_change(self)
    # Reiniciar el formateador de tiempo (nuevo cuarto = formato normal)
    self.scoreboard_window.time_formatter.reset()
    self.scoreboard_window.update_time_labels()

def update_quarter_label(self):
    if hasattr(self.match, 'quarter_label') and self.match.quarter_label.winfo_exists():
        self.match.quarter_label.config(text=str(self.match_state_controller.match_state.quarter))

def update_timeouts_for_quarter_change(self):
    """
    Actualiza los timeouts cuando cambia el cuarto.
    """
    from gui.control_panel.ui_components.ui_timeouts import update_timeout_controls_for_quarter, sync_timeout_checkbuttons

    # Obtener el cuarto actual del match_state
    current_quarter = self.match_state_controller.match_state.quarter

    # Actualizar los controles de timeout para el nuevo cuarto
    update_timeout_controls_for_quarter(self, current_quarter)

    # Sincronizar los checkbuttons con el estado actual
    sync_timeout_checkbuttons(self)


def update_fouls_for_quarter_change(self):
    """
    Actualiza las faltas cuando cambia el cuarto.
    Resetea el contador de faltas del equipo y el estado de BONUS.
    Las faltas de jugadores NO se resetean.
    """
    # Obtener el cuarto actual del match_state
    current_quarter = self.match_state_controller.match_state.quarter

    # Resetear faltas del equipo local
    self.home_team_controller.update_foul_quarter(current_quarter)

    # Resetear faltas del equipo visitante
    self.away_team_controller.update_foul_quarter(current_quarter)

    # Actualizar display en el scoreboard
    self.scoreboard_window.update_fouls_labels()

    # Actualizar display en el panel de control (si existe la pestaña de faltas)
    if hasattr(self.home_team, 'fouls') and hasattr(self.home_team.fouls, 'label'):
        from gui.control_panel.ui_components.ui_fouls import update_fouls_label
        update_fouls_label(self.home_team.fouls.label, self.home_team_controller)

    if hasattr(self.away_team, 'fouls') and hasattr(self.away_team.fouls, 'label'):
        from gui.control_panel.ui_components.ui_fouls import update_fouls_label
        update_fouls_label(self.away_team.fouls.label, self.away_team_controller)

    print(f"✅ Faltas reseteadas para el cuarto {current_quarter}")