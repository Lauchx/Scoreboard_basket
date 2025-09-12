import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
from PIL import Image, ImageTk
import os
from gui.scoreboard.styles_scoreboard import apply_styles

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
        self.root.configure(bg="black")
        simpleNamespace_forUi(self)
        self.match_state = match_state
        if not hasattr(self, "labels"):
            self.labels = SimpleNamespace(home_team=SimpleNamespace(),
                                     away_team=SimpleNamespace(),
                                     match=SimpleNamespace())
        home_team_labels = _nameSpace_entry_for_controller(self, self.match_state.home_team.name)
        awat_team_labels =_nameSpace_entry_for_controller(self, self.match_state.away_team.name)
        create_logos_labels(self,home_team_labels)
        create_names_labels(self, home_team_labels, self.match_state.home_team.name)
        #create_time_labels(self, home_team_labels)
        create_points_labels(self, home_team_labels, self.match_state.home_team.points)
        # create_quarter_labels(self, home_team_labels)
        # create_possession_labels(self, home_team_labels)
        # create_players_labels(self, home_team_labels)
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
    def update_label_players(self, player_jersey_number,player_name): 
       # self.labels.match.players.config(text=self.match_state.home_team.players)
        self.labels.match.players.insert(tk.END, f"{player_jersey_number} - {player_name}")

def simpleNamespace_forUi(self):
        self.labels = SimpleNamespace()
        self.labels.home_team = SimpleNamespace()
        self.labels.away_team = SimpleNamespace()
        self.labels.match = SimpleNamespace()
        self.match = SimpleNamespace()
# Create functions labels

def _nameSpace_entry_for_controller(self, team_name) -> SimpleNamespace:
    if team_name == self.match_state.home_team.name:
        return self.labels.home_team
    return self.labels.away_team

def setup_ui(self):
    self.notebook = ttk.Notebook(self.root)
    self.notebook.grid(row=0, column=0, sticky="nsew")

    self.frames.teams = ttk.Frame(self.notebook)
    self.notebook.add(self.frames.teams, text="Equipos")
