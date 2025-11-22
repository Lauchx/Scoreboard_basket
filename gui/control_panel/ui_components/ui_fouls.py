"""
Módulo para gestión de faltas en el panel de control.

Gestiona:
- Faltas individuales de jugadores (agregar/restar)
- Suspensión manual de jugadores
- Visualización de faltas de equipo y estado de bonus
"""
import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace


def setup_fouls_tab(control_panel):
    """
    Configura la pestaña de faltas en el panel de control.

    Args:
        control_panel: Instancia de Gui_control_panel
    """
    frame = control_panel.frames.fouls
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    setup_team_fouls_section(frame, control_panel, control_panel.home_team_controller, True)
    setup_team_fouls_section(frame, control_panel, control_panel.away_team_controller, False)


def setup_team_fouls_section(parent_frame, control_panel, team_controller, is_home):
    """
    Configura la sección de faltas para un equipo.

    Args:
        parent_frame: Frame padre
        control_panel: Instancia de Gui_control_panel
        team_controller: Controlador del equipo
        is_home: True si es equipo local
    """
    column = 0 if is_home else 1
    team_name = team_controller.team.name

    team_frame = ttk.LabelFrame(parent_frame, text=f"Faltas - {team_name}", padding=10)
    team_frame.grid(row=0, column=column, sticky="nsew", padx=5, pady=5)

    team_frame.grid_rowconfigure(10, weight=1)
    team_frame.grid_columnconfigure(0, weight=1)

    ttk.Label(team_frame, text="Jugadores", font=("Arial", 12, "bold")).grid(
        row=0, column=0, sticky="w", pady=(0, 10)
    )

    player_frame = ttk.Frame(team_frame)
    player_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
    player_frame.grid_columnconfigure(0, weight=1)

    scrollbar = ttk.Scrollbar(player_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    players_listbox = tk.Listbox(
        player_frame,
        height=8,
        yscrollcommand=scrollbar.set,
        font=("Arial", 10)
    )
    players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=players_listbox.yview)

    populate_players_listbox(players_listbox, team_controller)

    controls_frame = ttk.Frame(team_frame)
    controls_frame.grid(row=2, column=0, sticky="ew", pady=5)
    controls_frame.grid_columnconfigure(0, weight=1)
    controls_frame.grid_columnconfigure(1, weight=1)
    controls_frame.grid_columnconfigure(2, weight=1)
    controls_frame.grid_columnconfigure(3, weight=1)

    ttk.Button(
        controls_frame,
        text="➕ Falta",
        command=lambda: add_player_foul(control_panel, team_controller, players_listbox)
    ).grid(row=0, column=0, sticky="ew", padx=2)

    ttk.Button(
        controls_frame,
        text="➖ Quitar",
        command=lambda: subtract_player_foul(control_panel, team_controller, players_listbox)
    ).grid(row=0, column=1, sticky="ew", padx=2)

    ttk.Button(
        controls_frame,
        text="🚫 Suspender",
        command=lambda: suspend_player_btn(control_panel, team_controller, players_listbox)
    ).grid(row=0, column=2, sticky="ew", padx=2)

    ttk.Button(
        controls_frame,
        text="✅ Des-suspender",
        command=lambda: unsuspend_player_btn(control_panel, team_controller, players_listbox)
    ).grid(row=0, column=3, sticky="ew", padx=2)

    ttk.Separator(team_frame, orient=tk.HORIZONTAL).grid(
        row=3, column=0, sticky="ew", pady=10
    )

    # Inicializar namespace de faltas ANTES de llamar a setup_team_fouls_status
    if is_home:
        control_panel.home_team.fouls = SimpleNamespace(
            players_listbox=players_listbox,
            team_frame=team_frame
        )
    else:
        control_panel.away_team.fouls = SimpleNamespace(
            players_listbox=players_listbox,
            team_frame=team_frame
        )

    setup_team_fouls_status(team_frame, control_panel, team_controller, is_home)


def setup_team_fouls_status(parent_frame, control_panel, team_controller, is_home):
    """
    Configura la sección de estado de faltas de equipo.

    Args:
        parent_frame: Frame padre
        control_panel: Instancia de Gui_control_panel
        team_controller: Controlador del equipo
        is_home: True si es equipo local
    """
    status_frame = ttk.LabelFrame(parent_frame, text="Estado del Equipo", padding=10)
    status_frame.grid(row=4, column=0, sticky="nsew", pady=10)
    status_frame.grid_columnconfigure(0, weight=1)

    ttk.Label(status_frame, text="Faltas del equipo:", font=("Arial", 11, "bold")).grid(
        row=0, column=0, sticky="w", pady=5
    )

    fouls_count_label = ttk.Label(
        status_frame,
        text=str(team_controller.get_team_fouls()),
        font=("Arial", 24, "bold"),
        foreground="white"
    )
    fouls_count_label.grid(row=0, column=1, sticky="e", padx=10)

    bonus_frame = ttk.Frame(status_frame)
    bonus_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
    bonus_frame.grid_columnconfigure(0, weight=1)

    ttk.Label(bonus_frame, text="Estado BONUS:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)

    bonus_indicator = tk.Label(
        bonus_frame,
        text="●",
        font=("Arial", 24),
        foreground="gray"
    )
    bonus_indicator.pack(side=tk.LEFT, padx=10)

    def update_status():
        fouls = team_controller.get_team_fouls()
        is_bonus = team_controller.is_team_bonus()
        fouls_count_label.config(text=str(fouls))
        if is_bonus:
            bonus_indicator.config(foreground="red")
        else:
            bonus_indicator.config(foreground="gray")

    control_team_fouls_buttons = ttk.Frame(status_frame)
    control_team_fouls_buttons.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
    control_team_fouls_buttons.grid_columnconfigure(0, weight=1)
    control_team_fouls_buttons.grid_columnconfigure(1, weight=1)

    ttk.Button(
        control_team_fouls_buttons,
        text="➕ Falta de equipo",
        command=lambda: add_team_foul(control_panel, team_controller, update_status)
    ).grid(row=0, column=0, sticky="ew", padx=2)

    ttk.Button(
        control_team_fouls_buttons,
        text="➖ Quitar falta",
        command=lambda: subtract_team_foul(control_panel, team_controller, update_status)
    ).grid(row=0, column=1, sticky="ew", padx=2)

    # Agregar el namespace de status al namespace de fouls existente
    status_namespace = SimpleNamespace(
        fouls_label=fouls_count_label,
        bonus_indicator=bonus_indicator,
        update_status=update_status
    )

    if is_home:
        control_panel.home_team.fouls.status = status_namespace
    else:
        control_panel.away_team.fouls.status = status_namespace


def populate_players_listbox(listbox, team_controller):
    """Llena el listbox con los jugadores del equipo."""
    listbox.delete(0, tk.END)
    for player in team_controller.team.players:
        status = "🚫 SUSPENDIDO" if player.is_suspended else "✓ Activo"
        foul_text = f"{player.jersey_number}. {player.name} - Faltas: {player.foul}/5 ({status})"
        listbox.insert(tk.END, foul_text)


def add_player_foul(control_panel, team_controller, players_listbox):
    """Suma una falta a un jugador seleccionado."""
    selection = players_listbox.curselection()
    if not selection:
        return

    index = selection[0]
    player = team_controller.team.players[index]

    team_controller.add_player_foul(player)

    if player.foul >= 5:
        team_controller.add_team_foul()
        update_scoreboard_fouls(control_panel, team_controller)

    populate_players_listbox(players_listbox, team_controller)

    team_namespace = get_team_namespace(control_panel, team_controller)
    if hasattr(team_namespace, 'fouls') and hasattr(team_namespace.fouls, 'status'):
        team_namespace.fouls.status.update_status()


def subtract_player_foul(control_panel, team_controller, players_listbox):
    """Resta una falta a un jugador seleccionado."""
    selection = players_listbox.curselection()
    if not selection:
        return

    index = selection[0]
    player = team_controller.team.players[index]

    if player.foul > 0:
        team_controller.subtract_player_foul(player)
        populate_players_listbox(players_listbox, team_controller)
        update_scoreboard_fouls(control_panel, team_controller)


def suspend_player_btn(control_panel, team_controller, players_listbox):
    """Suspende manualmente un jugador."""
    selection = players_listbox.curselection()
    if not selection:
        return

    index = selection[0]
    player = team_controller.team.players[index]
    team_controller.suspend_player(player)

    populate_players_listbox(players_listbox, team_controller)
    update_scoreboard_players(control_panel, player, team_controller)


def unsuspend_player_btn(control_panel, team_controller, players_listbox):
    """Desuspende un jugador."""
    selection = players_listbox.curselection()
    if not selection:
        return

    index = selection[0]
    player = team_controller.team.players[index]
    team_controller.unsuspend_player(player)

    populate_players_listbox(players_listbox, team_controller)
    update_scoreboard_players(control_panel, player, team_controller)


def add_team_foul(control_panel, team_controller, update_status_callback):
    """Suma una falta al equipo."""
    result = team_controller.add_team_foul()
    update_status_callback()
    update_scoreboard_fouls(control_panel, team_controller)


def subtract_team_foul(control_panel, team_controller, update_status_callback):
    """Resta una falta al equipo."""
    result = team_controller.subtract_team_foul()
    update_status_callback()
    update_scoreboard_fouls(control_panel, team_controller)


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


def update_scoreboard_players(control_panel, player, team_controller):
    """Actualiza los colores de los jugadores en el marcador."""
    control_panel.scoreboard_window.update_label_players(player, team_controller)


def get_team_namespace(control_panel, team_controller):
    """Obtiene el namespace del equipo correspondiente."""
    if team_controller.team.name == control_panel.match_state_controller.home_team_controller.team.name:
        return control_panel.home_team
    return control_panel.away_team
