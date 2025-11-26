"""
Módulo para gestión de faltas en el panel de control.
"""
import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace


def setup_fouls_panel(control_panel, parent_frame):
    """
    Configura los paneles de faltas en el grid 3x3 (Fila 2)
    """
    setup_team_fouls_panel(parent_frame, control_panel, control_panel.home_team_controller, "FALTAS LOCAL", 0, control_panel.home_team)
    setup_team_fouls_panel(parent_frame, control_panel, control_panel.away_team_controller, "FALTAS VISITANTE", 2, control_panel.away_team)
    setup_clear_fouls_panel(parent_frame, control_panel)

def setup_team_fouls_panel(parent_frame, control_panel, team_controller, title, column, team_namespace):
    container = ttk.Frame(parent_frame)
    container.grid(row=2, column=column, sticky="nsew", padx=6, pady=6)

    ttk.Label(container, text=title, style="PanelFoulsTitle.TLabel").pack(side="top", pady=(2, 0))

    fouls_panel = ttk.Frame(container, style="PanelFouls.TFrame")
    fouls_panel.pack(fill="x", expand=False, pady=(4, 0), ipadx=4, ipady=4)

    fouls = team_controller.get_team_fouls()
    fouls_label = ttk.Label(fouls_panel, text=str(fouls), style="PanelFouls.TLabel")
    fouls_label.pack(anchor="center", pady=(4, 2))
    
    # Guardar referencia
    if not hasattr(team_namespace, 'fouls'):
        team_namespace.fouls = SimpleNamespace()
    team_namespace.fouls.label = fouls_label

    # Botones de control
    buttons_frame = ttk.Frame(fouls_panel)
    buttons_frame.pack(side="bottom", fill="x", pady=(2, 0))

    buttons_inner = ttk.Frame(buttons_frame)
    buttons_inner.pack(anchor="center")

    ttk.Button(buttons_inner, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: subtract_team_foul(control_panel, team_controller, fouls_label)).pack(side='left', padx=4)
    ttk.Button(buttons_inner, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: add_team_foul(control_panel, team_controller, fouls_label)).pack(side='left', padx=4)

def setup_clear_fouls_panel(parent_frame, control_panel):
    """Configura el panel del botón de limpiar faltas"""
    clear_fouls_panel = ttk.Frame(parent_frame, style="ControlPanel.Stack.TFrame")
    clear_fouls_panel.grid(row=2, column=1, sticky="n", padx=6, pady=6)

    clear_fouls_inner = ttk.Frame(clear_fouls_panel, style="ControlPanel.Stack.TFrame")
    clear_fouls_inner.pack(anchor="center", pady=10)

    ttk.Button(
        clear_fouls_inner,
        text="Borrar faltas",
        style="ControlPanel.ClearFouls.TButton",  
        command=lambda: clear_all_fouls(control_panel)
    ).pack(side="top", pady=6)

def add_team_foul(control_panel, team_controller, fouls_label):
    """Suma una falta al equipo."""
    team_controller.add_team_foul()
    update_fouls_label(fouls_label, team_controller)
    update_scoreboard_fouls(control_panel, team_controller)

def subtract_team_foul(control_panel, team_controller, fouls_label):
    """Resta una falta al equipo."""
    team_controller.subtract_team_foul()
    update_fouls_label(fouls_label, team_controller)
    update_scoreboard_fouls(control_panel, team_controller)

def update_fouls_label(fouls_label, team_controller):
    if fouls_label.winfo_exists():
        fouls_label.config(text=str(team_controller.get_team_fouls()))

def clear_all_fouls(control_panel):
    """Limpia las faltas de ambos equipos"""
    control_panel.home_team_controller.team.fouls = 0
    control_panel.away_team_controller.team.fouls = 0
    
    if hasattr(control_panel.home_team.fouls, 'label'):
        update_fouls_label(control_panel.home_team.fouls.label, control_panel.home_team_controller)
    if hasattr(control_panel.away_team.fouls, 'label'):
        update_fouls_label(control_panel.away_team.fouls.label, control_panel.away_team_controller)
        
    control_panel.scoreboard_window.update_fouls_labels()

def update_scoreboard_fouls(control_panel, team_controller):
    """Actualiza el BONUS y contador de faltas en el marcador."""
    fouls = team_controller.get_team_fouls()
    is_bonus = team_controller.is_team_bonus()

    if team_controller.team.name == control_panel.match_state_controller.home_team_controller.team.name:
        if hasattr(control_panel.scoreboard_window, 'home_bonus_fouls'):
            control_panel.scoreboard_window.home_bonus_fouls.update_fouls(fouls)
            control_panel.scoreboard_window.home_bonus_fouls.set_bonus(is_bonus)
    else:
        if hasattr(control_panel.scoreboard_window, 'away_bonus_fouls'):
            control_panel.scoreboard_window.away_bonus_fouls.update_fouls(fouls)
            control_panel.scoreboard_window.away_bonus_fouls.set_bonus(is_bonus)

