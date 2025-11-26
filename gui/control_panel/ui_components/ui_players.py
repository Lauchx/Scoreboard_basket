import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
from model.player import Player

from tkinter import messagebox

def setup_team_players(self, team_controller):
    team_simple_name_space = _nameSpace_for_controller(self,team_controller) ### Llama al name space del equipo correspondiente
    team_simple_name_space.player.name_var   = tk.StringVar(value="")
    team_simple_name_space.player.jerseyNumber_var = tk.StringVar(value="")
    team_simple_name_space.player.is_active_var = tk.BooleanVar(value=False)
    button_add_player(self, team_controller, team_simple_name_space)
    entry_players(team_simple_name_space)
    combobox_players(team_simple_name_space)
    checkbutton_players(team_simple_name_space)

    # Agregar controles de faltas en la misma pestaña
    setup_player_fouls_controls(self, team_controller, team_simple_name_space)

def entry_players(team_simple_name_space):
    ttk.Label(team_simple_name_space.frames.team.labelFrame, text="Nombre del jugador:").grid(row=4, column=0)
    team_simple_name_space.frames.team.entry.player_name = ttk.Entry(team_simple_name_space.frames.team.labelFrame, textvariable=team_simple_name_space.player.name_var)
    team_simple_name_space.frames.team.entry.player_name.grid(row=4, column=1)
    ttk.Label(team_simple_name_space.frames.team.labelFrame, text="Dorsal:").grid(row=4, column=2, sticky="w")
   
def combobox_players(team_simple_name_space):
    team_simple_name_space.frames.team.combobox.jerseyNumber = ttk.Combobox(team_simple_name_space.frames.team.labelFrame, state="readonly", values=[str(i) for i in range(100)], textvariable=team_simple_name_space.player.jerseyNumber_var, width=5)
    team_simple_name_space.frames.team.combobox.jerseyNumber.current(0) 
    team_simple_name_space.frames.team.combobox.jerseyNumber.grid(row=4, column=4, sticky="w")
def checkbutton_players(team_simple_name_space):
    team_simple_name_space.frames.team.checkbutton = ttk.Checkbutton(
        team_simple_name_space.frames.team.labelFrame,
        text="Titular",
        variable=team_simple_name_space.player.is_active_var
    )
    team_simple_name_space.frames.team.checkbutton.grid(row=4, column=5, sticky="w")

def button_add_player(self, team_controller, team_simple_name_space):
    ttk.Button(team_simple_name_space.frames.team.labelFrame, text=f"Añadir jugador", command=lambda: add_player(self, team_controller, team_simple_name_space)).grid(row=4, column=6)

def add_player(self, team_controller, team_simple_name_space):
    # llamaría al metodo del team_contorler que se encarga de agregar el jugador
    # team_controller.add_player()
    player_name = team_simple_name_space.player.name_var.get().strip()
    player_jersey_number = team_simple_name_space.player.jerseyNumber_var.get().strip()
    player_is_active = team_simple_name_space.player.is_active_var.get()

    # Validaciones: dorsal no vacío y numérico
    if not player_jersey_number:
        messagebox.showwarning("Dorsal inválido", "El número de dorsal no puede estar vacío.")
        return
    if not player_jersey_number.isdigit():
        messagebox.showwarning("Dorsal inválido", "El número de dorsal debe ser un número entero.")
        return

    jersey_int = int(player_jersey_number)

    # Verificar duplicados en el equipo
    existing = [int(p.jersey_number) for p in team_controller.team.players]
    if jersey_int in existing:
        messagebox.showwarning("Dorsal duplicado", f"El número #{jersey_int} ya está en uso en el equipo.")
        return

    # Crear jugador con dorsal como entero
    player = Player(player_name, jersey_int, player_is_active)
    team_controller.add_player_in_team(player)
    team_controller.show_team_players()

    # Actualizar el combo box de gestión de jugadores (lista ya está ordenada por controller)
    from gui.control_panel.ui_components.ui_teams import update_player_combo
    update_player_combo(team_simple_name_space, team_controller)

    # Actualizar scoreboard con la lista ordenada
    self.scoreboard_window.refresh_player_list(team_controller)

    # Limpiar campos de entrada
    team_simple_name_space.player.name_var.set("")
    team_simple_name_space.player.jerseyNumber_var.set("")

    # Actualizar listbox de faltas si existe
    if hasattr(team_simple_name_space.player, 'fouls_listbox'):
        populate_players_listbox_ui(team_controller, team_simple_name_space.player.fouls_listbox)

def _nameSpace_for_controller(self, team_controller) -> SimpleNamespace:
    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
        return self.home_team
    return self.away_team


def setup_player_fouls_controls(self, team_controller, team_simple_name_space):
    """
    Configura los controles de faltas de jugadores en la pestaña de equipos.
    """
    # Separador
    ttk.Separator(team_simple_name_space.frames.team.labelFrame, orient=tk.HORIZONTAL).grid(
        row=5, column=0, columnspan=7, sticky="ew", pady=10
    )

    # Título de sección de faltas
    ttk.Label(
        team_simple_name_space.frames.team.labelFrame,
        text="Gestión de Faltas",
        font=('TkDefaultFont', 10, 'bold')
    ).grid(row=6, column=0, columnspan=7, pady=5)

    # Listbox de jugadores con scrollbar
    listbox_frame = ttk.Frame(team_simple_name_space.frames.team.labelFrame)
    listbox_frame.grid(row=7, column=0, columnspan=7, padx=5, pady=5, sticky="nsew")

    scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
    players_listbox = tk.Listbox(
        listbox_frame,
        height=6,
        yscrollcommand=scrollbar.set,
        font=('TkDefaultFont', 9)
    )
    scrollbar.config(command=players_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Guardar referencia al listbox
    team_simple_name_space.player.fouls_listbox = players_listbox

    # Botones de control de faltas
    controls_frame = ttk.Frame(team_simple_name_space.frames.team.labelFrame)
    controls_frame.grid(row=8, column=0, columnspan=7, pady=5, sticky="ew")
    controls_frame.grid_columnconfigure(0, weight=1)
    controls_frame.grid_columnconfigure(1, weight=1)
    controls_frame.grid_columnconfigure(2, weight=1)
    controls_frame.grid_columnconfigure(3, weight=1)

    ttk.Button(
        controls_frame,
        text="➕ Añadir Falta",
        command=lambda: add_player_foul_ui(self, team_controller, players_listbox)
    ).grid(row=0, column=0, sticky="ew", padx=2)

    ttk.Button(
        controls_frame,
        text="➖ Quitar Falta",
        command=lambda: subtract_player_foul_ui(self, team_controller, players_listbox)
    ).grid(row=0, column=1, sticky="ew", padx=2)

    ttk.Button(
        controls_frame,
        text="🚫 Suspender",
        command=lambda: suspend_player_ui(self, team_controller, players_listbox)
    ).grid(row=0, column=2, sticky="ew", padx=2)

    ttk.Button(
        controls_frame,
        text="✅ Reactivar",
        command=lambda: unsuspend_player_ui(self, team_controller, players_listbox)
    ).grid(row=0, column=3, sticky="ew", padx=2)

    # Segunda fila de botones para cambiar estado activo/inactivo
    ttk.Button(
        controls_frame,
        text="✓ Marcar Titular",
        command=lambda: set_player_active_ui(self, team_controller, players_listbox, True)
    ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=(5, 0))

    ttk.Button(
        controls_frame,
        text="○ Marcar No Titular",
        command=lambda: set_player_active_ui(self, team_controller, players_listbox, False)
    ).grid(row=1, column=2, columnspan=2, sticky="ew", padx=2, pady=(5, 0))

    # Botón de Eliminar Jugador
    ttk.Button(
        controls_frame,
        text="🗑 Eliminar Jugador",
        command=lambda: remove_player_ui(self, team_controller, players_listbox)
    ).grid(row=2, column=0, columnspan=4, sticky="ew", padx=2, pady=(5, 0))

    # Display de estado del equipo (BONUS)
    status_frame = ttk.LabelFrame(team_simple_name_space.frames.team.labelFrame, text="Estado del Equipo")
    status_frame.grid(row=9, column=0, columnspan=7, padx=5, pady=10, sticky="ew")

    # Canvas para LED de BONUS
    bonus_canvas = tk.Canvas(status_frame, width=30, height=30, bg='white', highlightthickness=0)
    bonus_canvas.grid(row=0, column=0, padx=5, pady=5)
    bonus_indicator = bonus_canvas.create_oval(5, 5, 25, 25, fill='#808080', outline='#404040', width=2)

    ttk.Label(status_frame, text="BONUS:").grid(row=0, column=1, padx=5)

    # Label de faltas del equipo
    fouls_count_label = ttk.Label(
        status_frame,
        text="Faltas: 0/5",
        font=('TkDefaultFont', 12, 'bold')
    )
    fouls_count_label.grid(row=0, column=2, padx=10)

    # Guardar referencias para actualización
    team_simple_name_space.player.bonus_canvas = bonus_canvas
    team_simple_name_space.player.bonus_indicator = bonus_indicator
    team_simple_name_space.player.fouls_count_label = fouls_count_label

    # Función de actualización
    def update_team_status():
        team_fouls = team_controller.get_team_fouls()
        is_bonus = team_controller.is_team_bonus()

        # Actualizar label
        fouls_count_label.config(text=f"Faltas: {team_fouls}/5")

        # Actualizar LED
        color = '#FF0000' if is_bonus else '#808080'
        bonus_canvas.itemconfig(bonus_indicator, fill=color)

    team_simple_name_space.player.update_team_status = update_team_status

    # Actualizar listbox inicial
    populate_players_listbox_ui(team_controller, players_listbox)


def populate_players_listbox_ui(team_controller, listbox):
    """
    Rellena el listbox con los jugadores del equipo.
    """
    listbox.delete(0, tk.END)

    for player in team_controller.team.players:
        status = "🚫 SUSPENDIDO" if player.is_suspended else ("✓ Activo" if player.is_active else "○ Inactivo")
        text = f"#{player.jersey_number}. {player.name} - Faltas: {player.foul}/5 ({status})"
        listbox.insert(tk.END, text)


def add_player_foul_ui(self, team_controller, listbox):
    """
    Añade una falta al jugador seleccionado.
    """
    selection = listbox.curselection()
    if not selection:
        return

    player_index = selection[0]
    player = team_controller.team.players[player_index]

    # Añadir falta (automáticamente suma al equipo también)
    result = team_controller.add_player_foul(player)

    # Actualizar listbox
    populate_players_listbox_ui(team_controller, listbox)

    # Actualizar estado del equipo
    team_namespace = _nameSpace_for_controller(self, team_controller)
    if hasattr(team_namespace.player, 'update_team_status'):
        team_namespace.player.update_team_status()

    # Actualizar scoreboard
    self.scoreboard_window.update_label_players(player, team_controller)
    self.scoreboard_window.update_fouls_labels()

    print(f"➕ Falta añadida a {player.name}: {player.foul}/5 faltas")
    if result['player_info'].get('suspended'):
        print(f"🚫 {player.name} ha sido SUSPENDIDO (5 faltas)")
    if result['team_info'].get('bonus_activated'):
        print(f"🔴 ¡BONUS ACTIVADO! El equipo tiene {result['team_info']['total_fouls']} faltas")


def subtract_player_foul_ui(self, team_controller, listbox):
    """
    Quita una falta al jugador seleccionado.
    """
    selection = listbox.curselection()
    if not selection:
        return

    player_index = selection[0]
    player = team_controller.team.players[player_index]

    # Quitar falta (automáticamente resta del equipo también)
    result = team_controller.subtract_player_foul(player)

    # Actualizar listbox
    populate_players_listbox_ui(team_controller, listbox)

    # Actualizar estado del equipo
    team_namespace = _nameSpace_for_controller(self, team_controller)
    if hasattr(team_namespace.player, 'update_team_status'):
        team_namespace.player.update_team_status()

    # Actualizar scoreboard
    self.scoreboard_window.update_label_players(player, team_controller)
    self.scoreboard_window.update_fouls_labels()

    print(f"➖ Falta quitada a {player.name}: {player.foul}/5 faltas")


def suspend_player_ui(self, team_controller, listbox):
    """
    Suspende manualmente al jugador seleccionado.
    """
    selection = listbox.curselection()
    if not selection:
        return

    player_index = selection[0]
    player = team_controller.team.players[player_index]

    team_controller.suspend_player(player)

    # Actualizar listbox
    populate_players_listbox_ui(team_controller, listbox)

    # Actualizar scoreboard
    self.scoreboard_window.update_label_players(player, team_controller)

    print(f"🚫 {player.name} suspendido manualmente")


def unsuspend_player_ui(self, team_controller, listbox):
    """
    Reactiva al jugador suspendido.
    """
    selection = listbox.curselection()
    if not selection:
        return

    player_index = selection[0]
    player = team_controller.team.players[player_index]

    team_controller.unsuspend_player(player)

    # Actualizar listbox
    populate_players_listbox_ui(team_controller, listbox)

    # Actualizar scoreboard
    self.scoreboard_window.update_label_players(player, team_controller)

    print(f"✅ {player.name} reactivado")


def set_player_active_ui(self, team_controller, listbox, is_active):
    """
    Cambia el estado activo/inactivo del jugador seleccionado.

    Args:
        is_active (bool): True para titular (activo), False para no titular (inactivo)
    """
    selection = listbox.curselection()
    if not selection:
        return

    player_index = selection[0]
    player = team_controller.team.players[player_index]

    # Cambiar estado
    player.is_active = is_active

    # Actualizar listbox
    populate_players_listbox_ui(team_controller, listbox)

    # Actualizar scoreboard (refrescar toda la lista con colores correctos)
    self.scoreboard_window.update_label_players(player, team_controller)

    status_text = "Titular (Activo)" if is_active else "No Titular (Inactivo)"
    print(f"{'✓' if is_active else '○'} {player.name} marcado como {status_text}")


def remove_player_ui(self, team_controller, listbox):
    """
    Elimina el jugador seleccionado.
    """
    selection = listbox.curselection()
    if not selection:
        return

    player_index = selection[0]
    player = team_controller.team.players[player_index]
    
    # Confirmar eliminación
    if not messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar a {player.name} (#{player.jersey_number})?"):
        return

    # Eliminar
    team_controller.remove_player(player.jersey_number)

    # Actualizar listbox
    populate_players_listbox_ui(team_controller, listbox)

    # Actualizar combo
    team_namespace = _nameSpace_for_controller(self, team_controller)
    from gui.control_panel.ui_components.ui_teams import update_player_combo
    update_player_combo(team_namespace, team_controller)

    # Actualizar scoreboard
    self.scoreboard_window.refresh_player_list(team_controller)

    print(f"🗑 {player.name} eliminado")

