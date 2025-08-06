from tkinter import ttk


class ui_teams:
    def __init__(self, parent):
        self.parent = parent    
    def setup_ui_teams(self):
        setup_ui_home_team(self)
        setup_ui_away_team(self)


def setup_ui_home_team(self):
    self.parent.frames.home_team = ttk.LabelFrame(self.parent.frames.teams, text="Equipo Local")
    self.parent.frames.home_team.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.parent.frames.home_team, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.parent.entry.home_team.name = ttk.Entry(self.parent.frames.home_team)
    self.parent.entry.home_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    ttk.Button(self.parent.frames.home_team, text="Actualizar Nombre:", command=lambda: update_home_team_name(self.parent)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    self.parent.frames.home_team.grid_columnconfigure(1, weight=1)

def setup_ui_away_team(self):
    self.parent.frames.away_team = ttk.LabelFrame(self.parent.frames.teams, text="Equipo Visitante")
    self.parent.frames.away_team.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.parent.frames.away_team, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    self.parent.entry.away_team.name = ttk.Entry(self.parent.frames.away_team)
    self.parent.entry.away_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    self.parent.frames.away_team.grid_columnconfigure(1, weight=1)
    ttk.Button(self.parent.frames.away_team, text="Actualizar Nombre:", command=lambda: update_away_team_name(self.parent)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
def update_home_team_name(self):
    new_home_team_name = self.entry.home_team.name.get()
    self.match_state_controller.home_team_controller.change_name(new_home_team_name) 
    self.scoreboard_window.update_team_names_labels()
    self.frames.match.home_team.config(text=self.match_state_controller.home_team_controller.team.name)
    
def update_away_team_name(self):
    new_away_team_name = self.entry.away_team.name.get() 
    self.match_state_controller.away_team_controller.change_name(new_away_team_name)
    self.scoreboard_window.update_team_names_labels()