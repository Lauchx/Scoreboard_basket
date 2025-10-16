from tkinter import ttk 
def setup_ui_control_home_team_match(self):
    self.parent.frames.match.home_team = ttk.LabelFrame(self.parent.frames.match, text=self.home_team_controller.team.name)
    self.parent.frames.match.home_team.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
def setup_ui_home_team(self):
    print(self.parent)
    self.parent.home_team.labelFrame = ttk.LabelFrame(self.parent.frames.teams, text="Equipo Local")
    self.parent.home_team.labelFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.parent.home_team.labelFrame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.parent.home_team.entry.name = ttk.Entry(self.parent.home_team.labelFrame)
    self.parent.home_team.entry.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    ttk.Button(self.parent.home_team.labelFrame, text="Actualizar Nombre:", command=lambda: update_home_team_name(self)).grid(row=0, column=6, columnspan=2, padx=5, pady=5, sticky="nsew")
    self.parent.home_team.labelFrame.grid_columnconfigure(1, weight=1)
def update_home_team_name(self):
    new_home_team_name = self.parent.home_team.entry.name.get()
    self.parent.match_state_controller.home_team_controller.change_name(new_home_team_name) 
    self.parent.scoreboard_window.update_team_names_labels()
    self.parent.frames.match.home_team.config(text=self.home_team_controller.team.name)
