import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace

def setup_away_team_players(self, team_controller, team_frame):
    if not hasattr(self, "entry"):
        self.entry = SimpleNamespace(home_team=SimpleNamespace(),
                                     away_team=SimpleNamespace(),
                                     match=SimpleNamespace())
    else:
        team_entry = _nameSpace_entry_for_controller(self,team_controller)
        # Variables de Tk (no widgets)
        self.combobox.player.jerseyNumber_var = tk.StringVar(value="")
        team_entry.player_name_var   = tk.StringVar(value="")
        ##team_entry.jersey_number_var = ttk.StringVar(value="")

        button_add_player(self, team_frame, team_controller, team_entry)
        entry_players(self, team_frame, team_entry)

def entry_players(self, team_frame, team_entry):
        ttk.Label(team_frame, text="Nombre del jugador:").grid(row=4, column=0)
        team_entry.jerseyNumber = ttk.Entry(team_frame, textvariable=team_entry.player_name_var)
        team_entry.jerseyNumber.grid(row=4, column=1)
        ttk.Label(team_frame, text="Dorsal:").grid(row=4, column=2, sticky="w")
        self.combobox.player.jerseyNumber = ttk.Combobox(team_frame, state="readonly", values=[str(i) for i in range(100)], textvariable=self.combobox.player.jerseyNumber_var, width=5)
        self.combobox.player.jerseyNumber.current(0) 
        self.combobox.player.jerseyNumber.grid(row=4, column=4, sticky="w")

def button_add_player(self, team_frame, team_controller, team_entry):
    ttk.Button(team_frame, text=f"Añadir jugador", command=lambda: add_player(self,team_controller,team_entry)).grid(row=4, column=6)

def add_player(self,team_controller, team_entry):
    # llamaría al metodo del team_contorler que se encarga de agregar el jugador
    # team_controller.add_player()
    print(team_entry.player_name_var.get())
    print(self.combobox.player.jerseyNumber_var.get())

def _nameSpace_entry_for_controller(self, team_controller) -> SimpleNamespace:
    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
        return self.entry.home_team
    return self.entry.away_team