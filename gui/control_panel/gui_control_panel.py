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
from gui.control_panel.ui_components.ui_time import setup_ui_control_time_match, buttons_for_match_time, manage_timer, pause_resume_timer, change_text_button_timer
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
            'start_timer': 7,
            'pause_timer': 0,
            'resume_timer': 1
        }

        setup_joystick_callbacks(self)

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

        # Configurar interfaz del joystick
        setup_joystick_ui(self)

        # Configurar limpieza al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Función que se ejecuta al cerrar la aplicación"""
        print("🚪 Cerrando aplicación...")

        # Limpiar joystick controller
        if hasattr(self, 'joystick_controller'):
            self.joystick_controller.cleanup()

        # Cerrar ventana
        self.root.destroy()

    def add_points_home(self, points):
        """Suma puntos al equipo local"""
        for _ in range(points):
            self.home_team_controller.add_point()
        self.scoreboard_window.update_points_labels()
        print(f"🏠 +{points} puntos equipo local (Total: {self.home_team_controller.team.points})")

    def add_points_away(self, points):
        """Suma puntos al equipo visitante"""
        for _ in range(points):
            self.away_team_controller.add_point()
        self.scoreboard_window.update_points_labels()
        print(f"🚗 +{points} puntos equipo visitante (Total: {self.away_team_controller.team.points})")

    def subtract_points_home(self):
        """Resta un punto al equipo local"""
        if self.home_team_controller.team.points > 0:
            self.home_team_controller.substract_point()
            self.scoreboard_window.update_points_labels()
            print(f"🏠 -1 punto equipo local (Total: {self.home_team_controller.team.points})")

    def subtract_points_away(self):
        """Resta un punto al equipo visitante"""
        if self.away_team_controller.team.points > 0:
            self.away_team_controller.substract_point()
            self.scoreboard_window.update_points_labels()
            print(f"🚗 -1 punto equipo visitante (Total: {self.away_team_controller.team.points})")

    def start_timer(self):
        """Inicia el cronómetro"""
        print("▶️ Iniciar cronómetro")
        # Usar la función existente manage_timer que maneja inicio/pausa
        manage_timer(self)

    def pause_timer(self):
        """Pausa el cronómetro"""
        # Solo pausar si el cronómetro está activo
        if hasattr(self, 'is_active_timer') and self.is_active_timer:
            print("⏸️ Cronómetro pausado")
            pause_resume_timer(self)
            change_text_button_timer(self)
        else:
            print("⚠️ El cronómetro ya está pausado o no iniciado")

    def resume_timer(self):
        """Reanuda el cronómetro"""
        # Solo reanudar si el cronómetro está pausado
        if hasattr(self, 'is_active_timer') and not self.is_active_timer:
            print("▶️ Cronómetro reanudado")
            pause_resume_timer(self)
            # Necesitamos importar start_timer del módulo ui_time
            from gui.control_panel.ui_components.ui_time import start_timer
            start_timer(self)
            change_text_button_timer(self)
        else:
            print("⚠️ El cronómetro ya está en funcionamiento o no está configurado")

    def change_possession(self):
        """Cambia la posesión del balón"""
        self.scoreboard_window.update_possession_labels()
        print(f"🏀 Posesión cambiada a: {self.match_state_controller.match_state.possession}")


def simpleNamespace_forUi(self):
    self.entry = SimpleNamespace()
    self.entry.home_team = SimpleNamespace()
    self.entry.away_team = SimpleNamespace()
    self.entry.match = SimpleNamespace()
    self.frames = SimpleNamespace()
    self.combobox = SimpleNamespace()
    self.combobox.home_team = SimpleNamespace()
    self.combobox.away_team = SimpleNamespace()
    self.button = SimpleNamespace()
def setup_teams_players(self):
    setup_away_team_players(self, self.home_team_controller)
    setup_away_team_players(self, self.away_team_controller)

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
    print("🎮 Configurando callbacks del joystick...")

    # Callbacks para sumar puntos (1 punto cada vez)
    self.joystick_controller.set_callback('home_add_point', lambda: self.add_points_home(1))
    self.joystick_controller.set_callback('away_add_point', lambda: self.add_points_away(1))

    # Callbacks para restar puntos
    self.joystick_controller.set_callback('home_subtract_point', lambda: self.subtract_points_home())
    self.joystick_controller.set_callback('away_subtract_point', lambda: self.subtract_points_away())

    # Callbacks para control de tiempo
    self.joystick_controller.set_callback('start_timer', lambda: self.start_timer())
    self.joystick_controller.set_callback('pause_timer', lambda: self.pause_timer())
    self.joystick_controller.set_callback('resume_timer', lambda: self.resume_timer())

    print("✅ Callbacks del joystick configurados")


if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_control_panel(root, None)  # Sin pantalla pública en modo independiente
    root.mainloop()