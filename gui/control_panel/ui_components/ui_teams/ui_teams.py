from tkinter import ttk

from gui.control_panel.ui_components.ui_teams.ui_away_team import setup_ui_away_team, setup_ui_control_away_team_match
from gui.control_panel.ui_components.ui_teams.ui_home_team import setup_ui_control_home_team_match, setup_ui_home_team


class ui_teams:
    def __init__(self, parent):
        # Se inicializa con parent, ya que a diferencia de los otros componentes este es una clase. Parent en este caso es gui_control_panel.py
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

# Points Functions
def add_point(self, team_controller):
    team_controller.add_point()
    self.parent.scoreboard_window.update_points_labels()
def substract_point(self, team_controller):
    team_controller.substract_point()
    self.parent.scoreboard_window.update_points_labels()