from tkinter import ttk


class ui_teams:
    def __init__(self, parent):
        print(parent)
        self.parent = parent 
        self.home_team_controller = self.parent.match_state_controller.home_team_controller   
        self.away_team_controller = self.parent.match_state_controller.away_team_controller
    def setup_ui_teams(self):
        setup_ui_home_team(self)
        setup_ui_away_team(self)
        setup_ui_control_home_team_match(self)
        setup_ui_control_away_team_match(self)
    def buttons_points(self):
        ttk.Button(self.parent.frames.match.home_team, text=f"Sumar Punto", command=lambda: add_point(self, self.home_team_controller)).grid(row=1, column=2)
        ttk.Button(self.parent.frames.match.away_team, text=f"Sumar Punto", command=lambda: add_point(self, self.away_team_controller)).grid(row=1, column=2)
        ttk.Button(self.parent.frames.match.home_team, text=f"Restar Punto", command=lambda: substract_point(self, self.home_team_controller)).grid(row=2, column=2)
        ttk.Button(self.parent.frames.match.away_team, text=f"Restar Punto", command=lambda: substract_point(self, self.away_team_controller)).grid(row=2, column=2)

# ui functions
def setup_ui_control_home_team_match(self):
    self.parent.frames.match.home_team = ttk.LabelFrame(self.parent.frames.match, text=self.home_team_controller.team.name)
    self.parent.frames.match.home_team.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
def setup_ui_control_away_team_match(self):
    self.parent.frames.match.away_team = ttk.LabelFrame(self.parent.frames.match, text=self.away_team_controller.team.name)
    self.parent.frames.match.away_team.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

def setup_ui_home_team(self):
    self.parent.frames.home_team = ttk.LabelFrame(self.parent.frames.teams, text="Equipo Local")
    self.parent.frames.home_team.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.parent.frames.home_team, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.parent.entry.home_team.name = ttk.Entry(self.parent.frames.home_team)
    self.parent.entry.home_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    ttk.Button(self.parent.frames.home_team, text="Actualizar Nombre:", command=lambda: update_home_team_name(self)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    self.parent.frames.home_team.grid_columnconfigure(1, weight=1)

def setup_ui_away_team(self):
    self.parent.frames.away_team = ttk.LabelFrame(self.parent.frames.teams, text="Equipo Visitante")
    self.parent.frames.away_team.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.parent.frames.away_team, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    self.parent.entry.away_team.name = ttk.Entry(self.parent.frames.away_team)
    self.parent.entry.away_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    self.parent.frames.away_team.grid_columnconfigure(1, weight=1)
    ttk.Button(self.parent.frames.away_team, text="Actualizar Nombre:", command=lambda: update_away_team_name(self)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
def update_home_team_name(self):
    new_home_team_name = self.parent.entry.home_team.name.get()
    self.parent.match_state_controller.home_team_controller.change_name(new_home_team_name) 
    self.parent.scoreboard_window.update_team_names_labels()
    self.parent.frames.match.home_team.config(text=self.home_team_controller.team.name)
    
def update_away_team_name(self):
    new_away_team_name = self.parent.entry.away_team.name.get() 
    self.parent.match_state_controller.away_team_controller.change_name(new_away_team_name)
    self.parent.scoreboard_window.update_team_names_labels()
    self.parent.frames.match.home_team.config(text=self.away_team_controller.team.name)

# points Functions

def add_point(self, team_controller):
    team_controller.add_point()
    self.parent.scoreboard_window.update_points_labels()

def substract_point(self, team_controller):
    team_controller.substract_point()
    self.parent.scoreboard_window.update_points_labels()
