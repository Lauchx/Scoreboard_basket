import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
from model.player import Player

def setup_team_players(self, team_controller):
    team_simple_name_space = _nameSpace_for_controller(self,team_controller) ### Llama al name space del equipo correspondiente
    team_simple_name_space.player.name_var   = tk.StringVar(value="")
    team_simple_name_space.player.jerseyNumber_var = tk.StringVar(value="")
    team_simple_name_space.player.is_active_var = tk.BooleanVar(value=False)
    #team_simple_name_space.player.options = [True, False]
    button_add_player(self, team_controller, team_simple_name_space)
    entry_players(team_simple_name_space)

def entry_players(team_simple_name_space):
    ttk.Label(team_simple_name_space.labelFrame, text="Nombre del jugador:").grid(row=4, column=0)
    team_simple_name_space.entry.player_name = ttk.Entry(team_simple_name_space.labelFrame, textvariable=team_simple_name_space.player.name_var)
    team_simple_name_space.entry.player_name.grid(row=4, column=1)
    ttk.Label(team_simple_name_space.labelFrame, text="Dorsal:").grid(row=4, column=2, sticky="w")
    team_simple_name_space.combobox.jerseyNumber = ttk.Combobox(team_simple_name_space.labelFrame, state="readonly", values=[str(i) for i in range(100)], textvariable=team_simple_name_space.player.jerseyNumber_var, width=5)
    team_simple_name_space.combobox.jerseyNumber.current(0) 
    team_simple_name_space.combobox.jerseyNumber.grid(row=4, column=4, sticky="w")

    team_simple_name_space.checkbutton = ttk.Checkbutton(team_simple_name_space.labelFrame, text="Titutlar", 
                                                         command=lambda:is_active_change(team_simple_name_space))
    team_simple_name_space.checkbutton.grid(row=4, column=5, sticky="w")


def is_active_change(team_simple_name_space): 
    is_active =team_simple_name_space.player.is_active_var.get()
    team_simple_name_space.player.is_active_var.set(not is_active)
    print(not is_active)

def button_add_player(self, team_controller, team_simple_name_space):
    ttk.Button(team_simple_name_space.labelFrame, text=f"Añadir jugador", command=lambda: add_player(self, team_controller, team_simple_name_space)).grid(row=4, column=6)

def add_player(self, team_controller, team_simple_name_space):
    # llamaría al metodo del team_contorler que se encarga de agregar el jugador
    # team_controller.add_player()
    player_name = team_simple_name_space.player.name_var.get()
    player_jersey_number = team_simple_name_space.player.jerseyNumber_var.get()
    player_is_active = team_simple_name_space.player.is_active_var.get()
    player = Player(player_name,player_jersey_number,player_is_active) 
    team_controller.add_player_in_team(player)
    team_controller.show_team_players()
    self.scoreboard_window.update_label_players(player, team_controller)

def _nameSpace_for_controller(self, team_controller) -> SimpleNamespace:
    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
        return self.home_team
    return self.away_team

# def _nameSpace_combobox_for_controller(self, team_controller) -> SimpleNamespace:
#     if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
#         return self.combobox.home_team
#     return self.combobox.away_team
# def _nameSpace_frame_for_controller(self, team_controller) -> SimpleNamespace:
#     if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
#         return self.frames.home_team
#     return self.frames.away_team

        
