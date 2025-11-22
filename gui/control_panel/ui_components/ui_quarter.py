from tkinter import ttk


def buttons_change_quarter(self):
    ttk.Label(self.frames.match.time, text="Cuarto:").grid(row=2, column=0, pady=5, padx=5, sticky="nsew")
    ttk.Button(self.frames.match.time, text="-", command=lambda: substract_quarter(self)).grid(row=2, column=1, sticky="nsew" )
    ttk.Button(self.frames.match.time, text="+", command=lambda: add_quarter(self)).grid(row=2, column=2, sticky="nsew")


def add_quarter(self):
    self.scoreboard_window.update_quarter_labels(1)
    # Actualizar los timeouts para el nuevo cuarto
    update_timeouts_for_quarter_change(self)
    # Actualizar las faltas para el nuevo cuarto (resetear contador de equipo y bonus)
    update_fouls_for_quarter_change(self)
    # Reiniciar el formateador de tiempo (nuevo cuarto = formato normal)
    self.scoreboard_window.time_formatter.reset()
    self.scoreboard_window.update_time_labels()


def substract_quarter(self):
    self.scoreboard_window.update_quarter_labels(-1)
    # Actualizar los timeouts para el nuevo cuarto
    update_timeouts_for_quarter_change(self)
    # Actualizar las faltas para el nuevo cuarto (resetear contador de equipo y bonus)
    update_fouls_for_quarter_change(self)
    # Reiniciar el formateador de tiempo (nuevo cuarto = formato normal)
    self.scoreboard_window.time_formatter.reset()
    self.scoreboard_window.update_time_labels()


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
    if hasattr(self.home_team, 'fouls') and hasattr(self.home_team.fouls, 'status'):
        self.home_team.fouls.status.update_status()

    if hasattr(self.away_team, 'fouls') and hasattr(self.away_team.fouls, 'status'):
        self.away_team.fouls.status.update_status()

    print(f"✅ Faltas reseteadas para el cuarto {current_quarter}")