from tkinter import ttk
def setup_ui_control_away_team_match(self):
    self.parent.frames.match.away_team = ttk.LabelFrame(self.parent.frames.match, text=self.away_team_controller.team.name)
    self.parent.frames.match.away_team.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

def setup_ui_away_team(self):
    self.parent.away_team.labelFrame = ttk.LabelFrame(self.parent.frames.teams, text="Equipo Visitante")
    self.parent.away_team.labelFrame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.parent.away_team.labelFrame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    self.parent.away_team.entry.name = ttk.Entry(self.parent.away_team.labelFrame)
    self.parent.away_team.entry.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    self.parent.away_team.labelFrame.grid_columnconfigure(1, weight=1)
    ttk.Button(self.parent.away_team.labelFrame, text="Actualizar Nombre:", command=lambda: update_away_team_name(self)).grid(row=0, column=6, columnspan=2, padx=5, pady=5, sticky="nsew")
    
def update_away_team_name(self):
    new_away_team_name = self.parent.entry.away_team.name.get() 
    self.parent.match_state_controller.away_team_controller.change_name(new_away_team_name)
    self.parent.scoreboard_window.update_team_names_labels()
    self.parent.frames.match.home_team.config(text=self.away_team_controller.team.name)