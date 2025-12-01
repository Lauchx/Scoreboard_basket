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

    # Botón toggle para mostrar/ocultar jugadores en el scoreboard
    toggle_btn = ttk.Button(
        buttons_inner,
        text='👁',
        width=3,
        style="ControlPanel.Toggle.TButton",
        command=lambda: toggle_players_visibility(control_panel, team_controller)
    )
    toggle_btn.pack(side='left', padx=4)

    # Guardar referencia al botón y estado
    team_namespace.fouls.toggle_players_btn = toggle_btn
    team_namespace.fouls.players_visible = True  # Estado inicial: visible

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
    """
    Suma una falta al equipo.
    Las faltas de equipo no pueden superar 5 (límite implementado en FoulManager).
    """
    result = team_controller.add_team_foul()
    update_fouls_label(fouls_label, team_controller)
    update_scoreboard_fouls(control_panel, team_controller)

    # Log para debug
    if result.get('at_limit'):
        print(f"⚠️ Faltas de equipo en el límite (5). No se puede sumar más.")
    elif result.get('bonus_activated'):
        print(f"🔴 ¡BONUS ACTIVADO! El equipo tiene {result['total_fouls']} faltas")
    else:
        print(f"➕ Falta de equipo añadida: {result['total_fouls']}/5")

def subtract_team_foul(control_panel, team_controller, fouls_label):
    """
    Resta una falta al equipo.
    Las faltas de equipo no pueden bajar de 0.
    """
    team_controller.subtract_team_foul()
    update_fouls_label(fouls_label, team_controller)
    update_scoreboard_fouls(control_panel, team_controller)
    print(f"➖ Falta de equipo restada: {team_controller.get_team_fouls()}/5")

def update_fouls_label(fouls_label, team_controller):
    """Actualiza la etiqueta de faltas en el panel de control."""
    if fouls_label.winfo_exists():
        fouls_label.config(text=str(team_controller.get_team_fouls()))

def clear_all_fouls(control_panel):
    """
    Limpia las faltas de ambos equipos (resetea usando FoulManager).
    """
    # Obtener el cuarto actual
    current_quarter = control_panel.match_state_controller.match_state.quarter

    # Resetear faltas de ambos equipos usando el sistema de FoulManager
    control_panel.home_team_controller.update_foul_quarter(current_quarter)
    control_panel.away_team_controller.update_foul_quarter(current_quarter)

    # Actualizar labels en el panel de control
    if hasattr(control_panel.home_team, 'fouls') and hasattr(control_panel.home_team.fouls, 'label'):
        update_fouls_label(control_panel.home_team.fouls.label, control_panel.home_team_controller)
    if hasattr(control_panel.away_team, 'fouls') and hasattr(control_panel.away_team.fouls, 'label'):
        update_fouls_label(control_panel.away_team.fouls.label, control_panel.away_team_controller)

    # Actualizar scoreboard
    control_panel.scoreboard_window.update_fouls_labels()

    print("🔄 Faltas de equipo limpiadas para ambos equipos")

def update_scoreboard_fouls(control_panel, team_controller):
    """Actualiza el BONUS y contador de faltas en el marcador (scoreboard)."""
    # Llamar directamente a update_fouls_labels() que maneja correctamente
    # tanto el diseño moderno como el original
    control_panel.scoreboard_window.update_fouls_labels()


# ═══════════════════════════════════════════════════════════════════════════════
# TOGGLE VISIBILIDAD DE JUGADORES EN SCOREBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def toggle_players_visibility(control_panel, team_controller):
    """
    Alterna la visibilidad de la sección de jugadores en el scoreboard.

    Args:
        control_panel: Instancia del panel de control
        team_controller: Controlador del equipo (home o away)
    """
    # Determinar si es equipo local o visitante
    is_home = team_controller == control_panel.home_team_controller
    team_namespace = control_panel.home_team if is_home else control_panel.away_team

    # Alternar estado
    current_state = team_namespace.fouls.players_visible
    new_state = not current_state
    team_namespace.fouls.players_visible = new_state

    # Actualizar texto del botón
    btn_text = '👁' if new_state else '👁‍🗨'
    team_namespace.fouls.toggle_players_btn.config(text=btn_text)

    # Enviar comando al scoreboard
    control_panel.scoreboard_window.toggle_players_section(is_home, new_state)

    # Log para debug
    team_name = "LOCAL" if is_home else "VISITANTE"
    visibility = "visible" if new_state else "oculto"
    print(f"👁 Jugadores {team_name}: {visibility}")
