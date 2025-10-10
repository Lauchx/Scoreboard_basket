import tkinter as tk
from tkinter import ttk
from controller.match_state_controller import Match_state_controller
from controller.team_controller import Team_controller
# from gui.control_panel.ui_components.ui_teams.away_team.ui_away_team_players import setup_away_team_players
# from gui.control_panel.ui_components.ui_teams.home_team.delete import buttons_players
from gui.control_panel.ui_components.ui_players import setup_team_players
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from types import SimpleNamespace
from model.team import Team
from gui.control_panel.ui_components.ui_teams import ui_teams
from gui.control_panel.ui_components.ui_logo import buttons_logo 
from gui.control_panel.ui_components.ui_possession import buttons_change_possesion
from gui.control_panel.ui_components.ui_time import setup_ui_control_time_match, buttons_for_match_time, manage_timer, pause_resume_timer, change_text_button_timer, manage_timer
from controller.joystick_controller import JoystickController
from gui.control_panel.ui_components.ui_joystick import setup_joystick_ui



class Gui_control_panel():
    def __init__(self, root):
        self.root = root
        self.root.title("Consola de Control")
        self.root.configure(bg="gray")  
        self.root.minsize(800,300)
        simpleNamespace_forUi(self)
        self.home_team_controller = Team_controller(Team("","Equipo Local",0,0,[],3))
        self.away_team_controller = Team_controller(Team("","Equipo Visitante",0,0,[],3))
        self.match_state_controller = Match_state_controller(self.home_team_controller,self.away_team_controller,900,900,"Home",1)
        """
            match_state_controller.match_sate(Match_state): Object Match_state share with Gui_scoreboard.
        """

        # Inicializar JoystickController
        self.joystick_controller = JoystickController()

        # Inicializar configuración de botones por defecto
        self.button_config = {
            'home_add_point': 4,
            'away_add_point': 5,
            'home_subtract_point': 2,
            'away_subtract_point': 3,
            'manage_timer': 7,
            'pause_timer': 0,
            'resume_timer': 1
        }

        setup_joystick_callbacks(self)

        initialize_gui_scoreboard(self)
        setup_ui(self)

        ui_team_funtions(self)

        setup_ui_control_time_match(self)
        buttons_for_match_time(self)

        home_team_name_space = _nameSpace_team_for_controller(self, self.home_team_controller)
        away_team_name_space = _nameSpace_team_for_controller(self, self.away_team_controller)
        buttons_logo(self, self.home_team_controller, home_team_name_space)
        buttons_logo(self, self.away_team_controller, away_team_name_space)

        buttons_change_possesion(self)
        setup_teams_players(self)
        setup_joystick_ui(self)

        # Configurar limpieza al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    def on_closing(self):
        # Función que se ejecuta al cerrar la aplicación. Limpiar joystick controller. Evita dejar procesos colgados (ya que usa Hilos).
        if hasattr(self, 'joystick_controller'):
            self.joystick_controller.cleanup()
        self.root.destroy()


def simpleNamespace_forUi(self):
    self.frames = SimpleNamespace()
    self.button = SimpleNamespace()
    self.away_team = SimpleNamespace(frames=SimpleNamespace(team=SimpleNamespace(),match=SimpleNamespace()), player=SimpleNamespace())
    self.home_team = SimpleNamespace(frames=SimpleNamespace(team=SimpleNamespace(),match=SimpleNamespace()), player=SimpleNamespace())
    self.match = SimpleNamespace(entry= SimpleNamespace())
    set_atributes_simpleNamespace_shared(self.away_team.frames.team)
    set_atributes_simpleNamespace_shared(self.away_team.frames.match)
    set_atributes_simpleNamespace_shared(self.home_team.frames.team)
    set_atributes_simpleNamespace_shared(self.home_team.frames.match)

def set_atributes_simpleNamespace_shared(namespace):
    setattr(namespace,"entry", SimpleNamespace())
    setattr(namespace,"checkbutton", SimpleNamespace())
    setattr(namespace,"combobox", SimpleNamespace())

def _nameSpace_team_for_controller(self, team_controller) -> SimpleNamespace:
    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
        return self.home_team
    return self.away_team

def setup_teams_players(self):
    setup_team_players(self, self.home_team_controller)
    setup_team_players(self, self.away_team_controller)

def initialize_gui_scoreboard(self):
    self.scoreboard_window = Gui_scoreboard(tk.Toplevel(self.root),self.match_state_controller.match_state)

def setup_ui(self):
    self.is_active_timer = None
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

def setup_joystick_callbacks(self):
    """
    Configura las funciones callback que se ejecutarán cuando se presionen botones del joystick.
    Conecta cada acción del joystick con las funciones correspondientes del marcador.
    """
    # Callbacks para sumar puntos (1 punto cada vez)
    self.joystick_controller.set_callback('home_add_point', lambda: self.ui_teams.add_point(self.home_team_controller))
    self.joystick_controller.set_callback('away_add_point', lambda: self.ui_teams.add_point(self.away_team_controller))

    # Callbacks para restar puntos
    self.joystick_controller.set_callback('home_subtract_point', lambda: self.ui_teams.substract_point(self.home_team_controller))
    self.joystick_controller.set_callback('away_subtract_point', lambda: self.ui_teams.substract_point(self.away_team_controller))

    # Callbacks para control de tiempo
    self.joystick_controller.set_callback('manage_timer', lambda: manage_timer(self))
    #self.joystick_controller.set_callback('pause_timer', lambda: manage_timer(self))
    self.joystick_controller.set_callback('resume_timer', lambda: manage_timer(self))


if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_control_panel(root, None)  # Sin pantalla pública en modo independiente
    root.mainloop()