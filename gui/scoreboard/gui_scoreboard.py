import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
# from PIL import Image, ImageTk
# import os -- Revisar uso.
from gui.scoreboard.styles_scoreboard import apply_styles
from gui.scoreboard.ui_components.ui_time  import create_time_labels
from gui.scoreboard.ui_components.ui_teams  import create_names_labels, create_logos_labels, create_points_labels, teams_labels_grid_configure
from gui.scoreboard.ui_components.ui_players import create_players_labels
from gui.scoreboard.ui_components.ui_match import create_possession_labels,create_quarter_labels, setup_ui_match
class Gui_scoreboard:
    def __init__(self, root, match_state):
        """
        Args:
            home_team (Team): Objeto Team compartido con Gui_control_panel.
            away_team (Team): Objeto Team compartido con Gui_control_panel.
        """
        self.root = root
        apply_styles()
        self.root.title("Scoreboard")
        #self.root.minsize(800,500) ### Checkear en varios dispositivos - Los números no son correctos del todo 
        self.root.configure(bg="black")
        simpleNamespace_forUi(self)
        self.match_state = match_state
        setup_ui(self)
        if not hasattr(self, "labels"):
            self.labels = SimpleNamespace(home_team=SimpleNamespace(),
                                     away_team=SimpleNamespace(),
                                     match=SimpleNamespace())
        self.home_team_labels = _nameSpace_entry_for_controller(self, self.match_state.home_team.name)
        self.away_team_labels =_nameSpace_entry_for_controller(self, self.match_state.away_team.name)
        # create_quarter_labels(self, home_team_labels)
        # create_possession_labels(self, home_team_labels)
        # create_players_labels(self, home_team_labels)
        creates_home_team(self)
        creates_away_team(self)
    # Updates labels functions
    def update_team_logo_label(self):
        self.labels.home_team.logo.config(image=self.match_state.home_team.logo)
        self.labels.away_team.logo.config(image=self.match_state.away_team.logo)
    def update_points_labels(self):
        self.labels.home_team.points.config(text=str(self.match_state.home_team.points))
        self.labels.away_team.points.config(text=str(self.match_state.away_team.points))

    def update_time_labels(self):
        minutes = self.match_state.seconds_match_time // 60
        seconds = self.match_state.seconds_match_time % 60
        self.labels.match.time.config(text=f"{minutes:02}:{seconds:02}")

    def update_possession_labels(self, possession):
        self.labels.match.possession.config(text=possession)   

    def update_team_names_labels(self):
        self.labels.home_team.name.config(text=self.match_state.home_team.name)
        self.labels.away_team.name.config(text=self.match_state.away_team.name)

    def update_quarter_labels(self, number):
        self.match_state.quarter += number
        self.labels.match.quarter.config(text=f"Cuarto: {self.match_state.quarter}")

    def update_possession_labels(self):
        current_possesion = self.match_state.possession
        if current_possesion == "Away":
            self.match_state.possession = "Home"
            new_possesion = "⇦"  
            self.labels.match.possession.config(text=str(new_possesion))
        else:
            self.match_state.possession = "Away"
            new_possesion = "⇨" 
            self.labels.match.possession.config(text=str(new_possesion))
    def update_label_players(self, player_jersey_number,player_name, team_name): 
        if team_name == self.match_state.home_team.name:
            self.labels.home_team.players.insert(tk.END, f"{player_jersey_number} - {player_name}")
        else:
            self.labels.away_team.players.insert(tk.END, f"{player_jersey_number} - {player_name}")

def simpleNamespace_forUi(self):
        self.labels = SimpleNamespace(home_team=SimpleNamespace(),away_team=SimpleNamespace(),match=SimpleNamespace())
        self.frames = SimpleNamespace(teams=SimpleNamespace())
# Create functions labels

def _nameSpace_entry_for_controller(self, team_name) -> SimpleNamespace:
    if team_name == self.match_state.home_team.name:
        return self.labels.home_team
    return self.labels.away_team

def setup_ui(self):
    for column in range(3):
        self.root.grid_columnconfigure(column, weight=1, uniform="scoreboard")

    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_rowconfigure(1, weight=0)

    setup_ui_match(self)
    create_time_labels(self)
    create_possession_labels(self)
    create_quarter_labels(self)

def creates_home_team(self):
    self.frames.teams.home_team = ttk.Frame(self.root, style="home_team.TFrame", padding=(20, 15))
    self.frames.teams.home_team.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
    #ui_team
    teams_labels_grid_configure(self.frames.teams.home_team)
    create_names_labels(self.frames.teams.home_team, self.labels.home_team, self.match_state.home_team.name)
    create_logos_labels(self.frames.teams.home_team, self.labels.home_team)
    create_points_labels(self.frames.teams.home_team, self.labels.home_team, self.match_state.home_team.points)
    #ui_players
    create_players_labels(self.frames.teams.home_team, self.labels.home_team, True)
   

def creates_away_team(self):
    self.frames.teams.away_team = ttk.Frame(self.root, padding=(20, 15))
    self.frames.teams.away_team.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=20)
    #ui_team
    teams_labels_grid_configure(self.frames.teams.away_team)
    create_names_labels(self.frames.teams.away_team, self.labels.away_team, self.match_state.away_team.name)
    create_logos_labels(self.frames.teams.away_team, self.labels.away_team)
    create_points_labels(self.frames.teams.away_team, self.labels.away_team, self.match_state.away_team.points)
    #ui_players
    create_players_labels(self.frames.teams.away_team, self.labels.away_team, False)