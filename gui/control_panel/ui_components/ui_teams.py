from tkinter import ttk

class ui_teams:
    def __init__(self, parent):
        # Se inicializa con parent, ya que a diferencia de los otros componentes este es una clase. Parent en este caso es gui_control_panel.py
        self.parent = parent 
        self.home_team_controller = self.parent.match_state_controller.home_team_controller   
        self.away_team_controller = self.parent.match_state_controller.away_team_controller
    def setup_ui_teams(self):
        setup_ui_team(self, self.parent.home_team, self.home_team_controller, 0 ) ## El numero es la column que toma el LabelFrame - Mejorar. 
        setup_ui_team(self, self.parent.away_team, self.away_team_controller, 1 ) 
        setup_ui_control_team(self,self.parent.home_team, self.home_team_controller.team.name, 0) 
        setup_ui_control_team(self,self.parent.away_team, self.away_team_controller.team.name, 1)
    def buttons_points(self):
        ttk.Button(self.parent.home_team.frames.match.labelFrame, text=f"Sumar Punto", command=lambda: add_point(self, self.home_team_controller)).grid(row=1, column=2)
        ttk.Button(self.parent.away_team.frames.match.labelFrame, text=f"Sumar Punto", command=lambda: add_point(self, self.away_team_controller)).grid(row=1, column=2)
        ttk.Button(self.parent.home_team.frames.match.labelFrame, text=f"Restar Punto", command=lambda: substract_point(self, self.home_team_controller)).grid(row=2, column=2)
        ttk.Button(self.parent.away_team.frames.match.labelFrame, text=f"Restar Punto", command=lambda: substract_point(self, self.away_team_controller)).grid(row=2, column=2)

# Points Functions
def add_point(self, team_controller):
    team_controller.add_point()
    self.parent.scoreboard_window.update_points_labels()
def substract_point(self, team_controller):
    team_controller.substract_point()
    self.parent.scoreboard_window.update_points_labels()

def setup_ui_control_team(self,team_simple_name_space, team_name, colum):
    team_simple_name_space.frames.match.labelFrame = ttk.LabelFrame(self.parent.frames.match, text=team_name)
    team_simple_name_space.frames.match.labelFrame.grid(row=1, column=colum, padx=10, pady=10, sticky="nsew")

def setup_ui_team(self, team_simple_name_space,team_controller,column):
    print(team_controller.team.name)
    team_simple_name_space.frames.team.labelFrame = ttk.LabelFrame(self.parent.frames.teams, text=f"{team_controller.team.name}")
    team_simple_name_space.frames.team.labelFrame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
    ttk.Label(team_simple_name_space.frames.team.labelFrame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    team_simple_name_space.frames.team.entry.name = ttk.Entry(team_simple_name_space.frames.team.labelFrame)
    team_simple_name_space.frames.team.entry.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    team_simple_name_space.frames.team.labelFrame.grid_columnconfigure(1, weight=1)
    ttk.Button(team_simple_name_space.frames.team.labelFrame, text="Actualizar Nombre:", command=lambda: update_team_name(self, team_simple_name_space, team_controller)).grid(row=0, column=6, columnspan=2, padx=5, pady=5, sticky="nsew")
    
def update_team_name(self, team_simple_name_space, team_controller):
    new_team_name = team_simple_name_space.frames.team.entry.name.get()
    team_controller.change_name(new_team_name)
    self.parent.scoreboard_window.update_team_names_labels()
    ##self.parent.frames.match.home_team.config(text=self.away_team_controller.team.name)

