import tkinter as tk
from tkinter import ttk
from controller.match_state_controller import Match_state_controller
from controller.team_controller import Team_controller
# from gui.control_panel.ui_components.ui_teams.away_team.ui_away_team_players import setup_away_team_players
# from gui.control_panel.ui_components.ui_teams.home_team.delete import buttons_players
from gui.control_panel.ui_components.ui_players import setup_away_team_players
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from types import SimpleNamespace
from model.team import Team
from gui.control_panel.ui_components.ui_teams.ui_teams import ui_teams
from gui.control_panel.ui_components.ui_logo import buttons_logo 
from gui.control_panel.ui_components.ui_possession import buttons_change_possesion
from gui.control_panel.ui_components.ui_time import setup_ui_control_time_match, buttons_for_match_time



class Gui_control_panel():
    def __init__(self, root):
        self.root = root
        self.root.title("Consola de Control")
        self.root.configure(bg="gray")  
        self.root.minsize(800,300)
        simpleNamespace_forUi(self)
        self.home_team_controller = Team_controller(Team("","Equipo Local",0,0,[],3))
        self.away_team_controller = Team_controller(Team("","Equipo Visitante",0,0,[],3))
        self.match_state_controller = Match_state_controller(self.home_team_controller,self.away_team_controller,900,"Home",1)
        """
            match_state_controller.match_sate(Match_state): Object Match_state share with Gui_scoreboard.
        """
        initialize_gui_scoreboard(self)
        setup_ui(self)

        ui_team_funtions(self)

        setup_ui_control_time_match(self)
        buttons_for_match_time(self)

        buttons_logo(self)

        buttons_change_possesion(self)
        #buttons_players(self)
        #setup_away_team_players(self)
        ##start_timer(self)
        setup_teams_players(self)
        
        
def simpleNamespace_forUi(self):
    self.entry = SimpleNamespace()
    self.entry.home_team = SimpleNamespace()
    self.entry.away_team = SimpleNamespace()
    self.entry.match = SimpleNamespace()
    self.frames = SimpleNamespace()
    self.combobox = SimpleNamespace()
    self.combobox.home_team = SimpleNamespace()
    self.combobox.away_team = SimpleNamespace()
def setup_teams_players(self):
    setup_away_team_players(self, self.home_team_controller)
    setup_away_team_players(self, self.away_team_controller)

def initialize_gui_scoreboard(self):
    self.scoreboard_window = Gui_scoreboard(tk.Toplevel(self.root),self.match_state_controller.match_state)

def setup_ui(self):
    self.notebook = ttk.Notebook(self.root)
    self.notebook.grid(row=0, column=0, sticky="nsew")

    self.frames.teams = ttk.Frame(self.notebook)
    self.notebook.add(self.frames.teams, text="Equipos")

    self.frames.match = ttk.Frame(self.notebook)
    self.notebook.add(self.frames.match, text="Partido", sticky="nsew")

    grid_config(self)
    
def ui_team_funtions(self):
    self.ui_teams = ui_teams(self)
    self.ui_teams.setup_ui_teams()
    self.ui_teams.buttons_points()

def grid_config(self):
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)

    self.frames.teams.grid_rowconfigure(0, weight=1)
    self.frames.teams.grid_columnconfigure(0, weight=1)
    self.frames.teams.grid_columnconfigure(1, weight=1)

    self.frames.match.grid_rowconfigure(0, weight=1)
    self.frames.match.grid_columnconfigure(0, weight=1)
    self.frames.match.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_control_panel(root, None)  # Sin pantalla pública en modo independiente
    root.mainloop()