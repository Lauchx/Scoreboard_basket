from tkinter import ttk
class ui_teams:
    def __init__(self, parent):
        self.parent = parent 
        self.home_team_controller = self.parent.match_state_controller.home_team_controller   
        self.away_team_controller = self.parent.match_state_controller.away_team_controller

    def setup_ui_teams(self):
        # Configurar paneles de puntuación en el grid 3x3 (Fila 1)
        self.setup_score_panel("local", 0, "LOCAL", self.parent.home_team, self.home_team_controller)
        self.setup_score_panel("visitor", 2, "VISITANTE", self.parent.away_team, self.away_team_controller)

    def setup_score_panel(self, team_type, column, title, team_namespace, team_controller):
        panel = ttk.Frame(self.parent.frames.match.right_frame, style="PanelTestScore.TFrame")
        panel.grid(row=1, column=column, sticky="nsew", padx=6, pady=6)
        panel.grid_rowconfigure(0, weight=0)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_rowconfigure(2, weight=0)
        panel.grid_columnconfigure(0, weight=1)

        ttk.Label(panel, text=title, style="PanelTestScoreTitle.TLabel", anchor="center").grid(row=0, column=0, sticky="ew", pady=(2, 0))

        # Label de puntuación
        points = team_controller.team.points
        score_label = ttk.Label(panel, text=str(points), style="PanelTestScore.TLabel", anchor="center")
        score_label.grid(row=1, column=0, sticky="nsew", pady=(6, 4))
        
        # Guardar referencia en el namespace para actualizaciones
        team_namespace.score_label = score_label

        # Botones de puntos
        buttons_frame = ttk.Frame(panel)
        buttons_frame.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        buttons_inner = ttk.Frame(buttons_frame)
        buttons_inner.pack(anchor="center")

        ttk.Button(buttons_inner, text='-', width=3, style="ControlPanel.Minus.TButton", command=lambda: self.substract_point(team_controller, score_label)).pack(side='left', padx=4)
        ttk.Button(buttons_inner, text='+', width=3, style="ControlPanel.Plus.TButton", command=lambda: self.add_point(team_controller, score_label)).pack(side='left', padx=4)



    def add_point(self, team_controller, score_label):
        team_controller.add_point()
        self.update_score_label(score_label, team_controller)
        self.parent.scoreboard_window.update_points_labels()

    def substract_point(self, team_controller, score_label):
        team_controller.substract_point()
        self.update_score_label(score_label, team_controller)
        self.parent.scoreboard_window.update_points_labels()

    def update_score_label(self, score_label, team_controller):
        if score_label.winfo_exists():
            score_label.config(text=str(team_controller.team.points))

    def buttons_points(self):
        # Deprecated: functionality moved to setup_score_panel
        pass

def update_player_combo(team_simple_name_space, team_controller):
    """
    Actualiza el combobox de selección de dorsal, eliminando los números ya usados.
    """
    if hasattr(team_simple_name_space.frames.team.combobox, 'jerseyNumber'):
        used_numbers = [int(p.jersey_number) for p in team_controller.team.players]
        available_numbers = [str(i) for i in range(100) if i not in used_numbers]
        team_simple_name_space.frames.team.combobox.jerseyNumber['values'] = available_numbers

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
    from tkinter import messagebox

    # Límite máximo de titulares
    MAX_STARTERS = 5

    jersey_number = get_selected_player_number(team_simple_name_space)
    if jersey_number is not None:
        # Buscar el jugador
        target_player = None
        for player in team_controller.team.players:
            if int(player.jersey_number) == jersey_number:
                target_player = player
                break

        if target_player is None:
            return

        # Validar límite de titulares si se va a activar
        if not target_player.is_active:  # Va a pasar a activo
            current_starters = sum(1 for p in team_controller.team.players if p.is_active)
            if current_starters >= MAX_STARTERS:
                messagebox.showwarning(
                    "Límite de titulares",
                    "Solo pueden haber 5 titulares al mismo tiempo."
                )
                return

        # Use the controller to toggle the player's active state (ensures model consistency)
        team_controller.toggle_player_active(jersey_number)

        # Reflect the change in the UI var (if present)
        try:
            team_simple_name_space.player.is_active_var.set(target_player.is_active)
        except Exception:
            # If the namespace var isn't available, ignore silently
            pass

        # Update scoreboard view
        self.parent.scoreboard_window.refresh_player_list(team_controller)
