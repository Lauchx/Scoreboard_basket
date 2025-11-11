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
        ttk.Button(self.parent.home_team.frames.match.labelFrame, text=f"Sumar Punto", command=lambda: self.add_point(self, self.home_team_controller)).grid(row=1, column=2)
        ttk.Button(self.parent.away_team.frames.match.labelFrame, text=f"Sumar Punto", command=lambda: self.add_point(self, self.away_team_controller)).grid(row=1, column=2)
        ttk.Button(self.parent.home_team.frames.match.labelFrame, text=f"Restar Punto", command=lambda: self.substract_point(self, self.home_team_controller)).grid(row=2, column=2)
        ttk.Button(self.parent.away_team.frames.match.labelFrame, text=f"Restar Punto", command=lambda: self.substract_point(self, self.away_team_controller)).grid(row=2, column=2)
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
    
    # Team name controls
    ttk.Label(team_simple_name_space.frames.team.labelFrame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    team_simple_name_space.frames.team.entry.name = ttk.Entry(team_simple_name_space.frames.team.labelFrame)
    team_simple_name_space.frames.team.entry.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    team_simple_name_space.frames.team.labelFrame.grid_columnconfigure(1, weight=1)
    ttk.Button(team_simple_name_space.frames.team.labelFrame, text="Actualizar Nombre:", command=lambda: update_team_name(self, team_simple_name_space, team_controller)).grid(row=0, column=6, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    # Player management frame
    player_frame = ttk.LabelFrame(team_simple_name_space.frames.team.labelFrame, text="Gestión de Jugadores")
    player_frame.grid(row=1, column=0, columnspan=8, padx=5, pady=5, sticky="nsew")
    
    # Player combo box
    team_simple_name_space.frames.team.combobox.players = ttk.Combobox(player_frame, width=15, state="readonly")
    team_simple_name_space.frames.team.combobox.players.grid(row=0, column=0, padx=5, pady=5)
    
    # Delete player button
    ttk.Button(player_frame, text="Eliminar Jugador", 
              command=lambda: delete_player(self, team_simple_name_space, team_controller)).grid(row=0, column=1, padx=5, pady=5)
              
    # Toggle active status button  
    ttk.Button(player_frame, text="Cambiar Estado", 
              command=lambda: toggle_player_active(self, team_simple_name_space, team_controller)).grid(row=0, column=2, padx=5, pady=5)
              
    # Update combo box with current players
    update_player_combo(team_simple_name_space, team_controller)
    
def update_team_name(self, team_simple_name_space, team_controller):
    new_team_name = team_simple_name_space.frames.team.entry.name.get()
    team_controller.change_name(new_team_name)
    self.parent.scoreboard_window.update_team_names_labels()
    ##self.parent.frames.match.home_team.config(text=self.away_team_controller.team.name)

def update_player_combo(team_simple_name_space, team_controller):
    """Update the combo box with current player numbers"""
    team_simple_name_space.frames.team.combobox.players['values'] = team_controller.get_player_numbers()
    
def get_selected_player_number(team_simple_name_space):
    """Get the jersey number from selected player in combo box"""
    selected = team_simple_name_space.frames.team.combobox.players.get()
    if selected:
        return int(selected.replace('#', ''))
    return None

def delete_player(self, team_simple_name_space, team_controller):
    """Delete selected player from team"""
    jersey_number = get_selected_player_number(team_simple_name_space)
    print(f"Número seleccionado para borrar: {jersey_number}")
    
    if jersey_number is not None:
        print(f"Jugadores antes de borrar: {[p.jersey_number for p in team_controller.team.players]}")
        
        # Remove from team model
        team_controller.remove_player(jersey_number)
        
        print(f"Jugadores después de borrar: {[p.jersey_number for p in team_controller.team.players]}")
        
        # Update combo box and clear selection
        update_player_combo(team_simple_name_space, team_controller)
        team_simple_name_space.frames.team.combobox.players.set('')
        
        # Update scoreboard
        self.parent.scoreboard_window.refresh_player_list(team_controller)

def toggle_player_active(self, team_simple_name_space, team_controller):
    """Toggle active status of selected player"""
    jersey_number = get_selected_player_number(team_simple_name_space)
    if jersey_number is not None:
        # Use the controller to toggle the player's active state (ensures model consistency)
        team_controller.toggle_player_active(jersey_number)

        # Reflect the change in the UI var (if present)
        for player in team_controller.team.players:
            if int(player.jersey_number) == jersey_number:
                try:
                    team_simple_name_space.player.is_active_var.set(player.is_active)
                except Exception:
                    # If the namespace var isn't available, ignore silently
                    pass
                break

        # Update scoreboard view
        self.parent.scoreboard_window.refresh_player_list(team_controller)
