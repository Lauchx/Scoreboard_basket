import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
from model.player import Player

def setup_away_team_players(self, team_controller):
    if not hasattr(self, "entry"):
        self.entry = SimpleNamespace(home_team=SimpleNamespace(),
                                     away_team=SimpleNamespace(),
                                     match=SimpleNamespace())
    
    team_entry = _nameSpace_entry_for_controller(self,team_controller) ### Llama al entry del equipo correspondiente
    # Variables de Tk (no widgets)
    team_frame = _nameSpace_frame_for_controller(self,team_controller)
    self.team_entry = team_entry
    self.team_entry.player_name_var   = tk.StringVar(value="")
    team_combobox = _nameSpace_combobox_for_controller(self, team_controller)
    team_combobox.jerseyNumber_var = tk.StringVar(value="")
    button_add_player(self, team_frame, team_controller, team_entry,team_combobox)
    entry_players(team_frame, team_entry,team_combobox)

def entry_players(team_frame, team_entry, team_combobox):
        ttk.Label(team_frame, text="Nombre del jugador:").grid(row=4, column=0)
        team_entry.jerseyNumber = ttk.Entry(team_frame, textvariable=team_entry.player_name_var)
        team_entry.jerseyNumber.grid(row=4, column=1)
        ttk.Label(team_frame, text="Dorsal:").grid(row=4, column=2, sticky="w")
        
        team_combobox.jerseyNumber = ttk.Combobox(team_frame, state="readonly", values=[str(i) for i in range(100)], textvariable=team_combobox.jerseyNumber_var, width=5)
        team_combobox.jerseyNumber.current(0) 
        team_combobox.jerseyNumber.grid(row=4, column=4, sticky="w")

def button_add_player(self, team_frame, team_controller, team_entry, team_combobox):
    ttk.Button(team_frame, text=f"Añadir jugador", command=lambda: add_player(self, team_controller,team_entry,team_combobox)).grid(row=4, column=6)

def add_player(self, team_controller, team_entry, team_combobox):
    # llamaría al metodo del team_contorler que se encarga de agregar el jugador
    # team_controller.add_player()
    player_name = team_entry.player_name_var.get()
    player_jersey_number = team_combobox.jerseyNumber_var.get()
    player = Player(player_name,player_jersey_number,False) 
    team_controller.add_player_in_team(player)
    team_controller.show_team_players()
    self.scoreboard_window.update_label_players(player_jersey_number,player_name, team_controller.team.name)

def _nameSpace_entry_for_controller(self, team_controller) -> SimpleNamespace:
    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
        return self.entry.home_team
    return self.entry.away_team

def _nameSpace_combobox_for_controller(self, team_controller) -> SimpleNamespace:
    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
        return self.combobox.home_team
    return self.combobox.away_team
def _nameSpace_frame_for_controller(self, team_controller) -> SimpleNamespace:
    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
        return self.frames.home_team
    return self.frames.away_team

        
