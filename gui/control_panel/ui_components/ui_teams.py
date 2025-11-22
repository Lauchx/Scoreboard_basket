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
        """Crea los botones de puntos en la parte superior de cada LabelFrame de equipo."""
        # Botones para equipo local (HOME)
        ttk.Button(
            self.parent.home_team.frames.match.labelFrame,
            text="➕ Sumar Punto",
            command=lambda: self.add_point(self.home_team_controller)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            self.parent.home_team.frames.match.labelFrame,
            text="➖ Restar Punto",
            command=lambda: self.substract_point(self.home_team_controller)
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botones para equipo visitante (AWAY)
        ttk.Button(
            self.parent.away_team.frames.match.labelFrame,
            text="➕ Sumar Punto",
            command=lambda: self.add_point(self.away_team_controller)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            self.parent.away_team.frames.match.labelFrame,
            text="➖ Restar Punto",
            command=lambda: self.substract_point(self.away_team_controller)
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    # Points Functions
    def add_point(self, team_controller):
        team_controller.add_point()
        self.parent.scoreboard_window.update_points_labels()

    def substract_point(self, team_controller):
        team_controller.substract_point()
        self.parent.scoreboard_window.update_points_labels()



def setup_ui_control_team(self,team_simple_name_space, team_name, colum):
    team_simple_name_space.frames.match.labelFrame = ttk.LabelFrame(self.parent.frames.match, text=team_name)
    # sticky="new" (sin 's') para que no se expanda verticalmente, solo horizontalmente
    # pady reducido para que quede pegado a los botones
    team_simple_name_space.frames.match.labelFrame.grid(row=0, column=colum, padx=10, pady=(10, 5), sticky="new")

def setup_ui_team(self, team_simple_name_space,team_controller,column):
    print(team_controller.team.name)
    team_simple_name_space.frames.team.labelFrame = ttk.LabelFrame(self.parent.frames.teams, text=f"{team_controller.team.name}")
    team_simple_name_space.frames.team.labelFrame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
    ttk.Label(team_simple_name_space.frames.team.labelFrame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Crear Entry con valor inicial del nombre del equipo
    # Limitar a 12 caracteres máximo usando validatecommand
    vcmd = (self.parent.root.register(lambda text: len(text) <= 12), '%P')
    team_simple_name_space.frames.team.entry.name = ttk.Entry(
        team_simple_name_space.frames.team.labelFrame,
        validate='key',
        validatecommand=vcmd
    )
    team_simple_name_space.frames.team.entry.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    # Insertar el nombre actual del equipo como placeholder (truncado a 12 caracteres)
    initial_name = team_controller.team.name[:12] if len(team_controller.team.name) > 12 else team_controller.team.name
    team_simple_name_space.frames.team.entry.name.insert(0, initial_name)

    team_simple_name_space.frames.team.labelFrame.grid_columnconfigure(1, weight=1)
    ttk.Button(team_simple_name_space.frames.team.labelFrame, text="Actualizar Nombre:", command=lambda: update_team_name(self, team_simple_name_space, team_controller)).grid(row=0, column=6, columnspan=2, padx=5, pady=5, sticky="nsew")
    
def update_team_name(self, team_simple_name_space, team_controller):
    new_team_name = team_simple_name_space.frames.team.entry.name.get()
    team_controller.change_name(new_team_name)
    self.parent.scoreboard_window.update_team_names_labels()
    ##self.parent.frames.match.home_team.config(text=self.away_team_controller.team.name)

