import tkinter as tk
from tkinter import ttk
from controller.match_state_controller import Match_state_controller
from controller.team_controller import Team_controller
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from types import SimpleNamespace
from model.team import Team
from gui.control_panel.ui_components.ui_teams import ui_teams
from gui.control_panel.ui_components.ui_logo import buttons_logo
from gui.control_panel.ui_components.ui_possession import toggle_possession
from gui.control_panel.ui_components.ui_time import setup_time_panel, setup_timer_buttons, manage_timer
from gui.control_panel.ui_components.ui_quarter import setup_quarter_panel
from gui.control_panel.ui_components.ui_fouls import setup_fouls_panel
from gui.control_panel.ui_components.ui_action_center import setup_action_panel
from gui.control_panel.ui_components.ui_left_panel import setup_left_panel
from controller.joystick_controller import JoystickController
from gui.control_panel.ui_components.ui_joystick import setup_joystick_ui, update_joystick_info
from gui.control_panel.ui_components.ui_color_customization import setup_color_customization_ui
from gui.control_panel.styles_control_panel import apply_styles_control_panel_test
from gui.control_panel.ui_components.ui_timeouts import setup_timeout_controls



class Gui_control_panel():
    def __init__(self, root):
        self.root = root
        self.root.title("Consola de Control")
        self.root.configure(bg="#F5F5F5") 
        self.root.minsize(800,300)

        # Aplicar estilos personalizados al panel de control
        apply_styles_control_panel_test()
        
        simpleNamespace_forUi(self)
        self.home_team_controller = Team_controller(Team("","Equipo Local",0,0,[],3))
        self.away_team_controller = Team_controller(Team("","Equipo Visitante",0,0,[],3))
        self.match_state_controller = Match_state_controller(self.home_team_controller,self.away_team_controller,900,900,"Home",1)
        """
            match_state_controller.match_sate(Match_state): Object Match_state share with Gui_scoreboard.
        """
        
        # Compatibilidad para componentes que esperan main_panel (como gui_left_control_panel)
        self.main_panel = self

        # Inicializar JoystickController con sistema de mapeo abstracto
        self.joystick_controller = JoystickController(on_disconnect_callback=lambda:update_joystick_info(self))


        # La configuración de botones ahora se maneja a través del sistema abstracto
        # No necesitamos button_config aquí, se usa action_config con botones abstractos

        setup_joystick_callbacks(self)

        initialize_gui_scoreboard(self)
        setup_ui(self)

        # Configurar controles de timeouts para ambos equipos
        setup_timeout_controls(self, self.home_team, self.home_team_controller, self.frames.match.right_frame)
        setup_timeout_controls(self, self.away_team, self.away_team_controller, self.frames.match.right_frame)

        # Configurar limpieza al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    def on_closing(self):
        # Función que se ejecuta al cerrar la aplicación. Limpiar joystick controller. Evita dejar procesos colgados (ya que usa Hilos).
        if hasattr(self, 'joystick_controller'):
            self.joystick_controller.cleanup()
        self.root.destroy()


def simpleNamespace_forUi(self):
    self.frames = SimpleNamespace()
    self.frames.match = SimpleNamespace() # Initialize match namespace
    self.button = SimpleNamespace()
    self.away_team = SimpleNamespace(frames=SimpleNamespace(team=SimpleNamespace(),match=SimpleNamespace()), player=SimpleNamespace(), timeout_vars=[])
    self.home_team = SimpleNamespace(frames=SimpleNamespace(team=SimpleNamespace(),match=SimpleNamespace()), player=SimpleNamespace(), timeout_vars=[])
    self.match = SimpleNamespace(entry= SimpleNamespace(), time=SimpleNamespace())
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

def initialize_gui_scoreboard(self):

    self.scoreboard_window = Gui_scoreboard(tk.Toplevel(self.root),self.match_state_controller.match_state)
    # Agregar referencia al control panel para actualizar colores de jugadores
    self.scoreboard_window.control_panel = self

def setup_ui(self):
    self.is_active_timer = None
    
    # Configuración del grid raíz (1/6 izquierda, 5/6 derecha)
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_columnconfigure(1, weight=7)

    # Panel Izquierdo (Jugadores y Equipos)
    setup_left_panel(self)

    # Panel Derecho (Partido)
    self.frames.match.right_frame = ttk.Frame(self.root, style="PanelTest.TFrame")
    self.frames.match.right_frame.grid(row=0, column=1, sticky="nsew")
    
    # Configurar grid 3x3
    for r in range(3):
        self.frames.match.right_frame.grid_rowconfigure(r, weight=1, uniform='rightgrid')
    for c in range(3):
        self.frames.match.right_frame.grid_columnconfigure(c, weight=1, uniform='rightgrid')

    # Fila 0
    setup_time_panel(self, self.frames.match.right_frame)
    setup_timer_buttons(self, self.frames.match.right_frame)
    setup_quarter_panel(self, self.frames.match.right_frame)

    # Fila 1
    self.ui_teams = ui_teams(self)
    self.ui_teams.setup_ui_teams() # Configura Score Panels
    setup_action_panel(self, self.frames.match.right_frame)

    # Fila 2
    setup_fouls_panel(self, self.frames.match.right_frame)

def setup_joystick_callbacks(self):
    """
    Configura las funciones callback que se ejecutarán cuando se presionen botones del joystick.
    Conecta cada acción del joystick con las funciones correspondientes del marcador.
    """
    # Callbacks para sumar puntos (1 punto cada vez)
    self.joystick_controller.set_callback('home_add_point', lambda: self.ui_teams.add_point(self.home_team_controller, self.home_team.score_label))
    self.joystick_controller.set_callback('away_add_point', lambda: self.ui_teams.add_point(self.away_team_controller, self.away_team.score_label))

    # Callbacks para restar puntos
    self.joystick_controller.set_callback('home_subtract_point', lambda: self.ui_teams.substract_point(self.home_team_controller, self.home_team.score_label))
    self.joystick_controller.set_callback('away_subtract_point', lambda: self.ui_teams.substract_point(self.away_team_controller, self.away_team.score_label))

    # Callbacks para control de tiempo
    self.joystick_controller.set_callback('manage_timer', lambda: manage_timer(self))
    self.joystick_controller.set_callback('change_possession', lambda: toggle_possession(self))


if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_control_panel(root)  # Sin pantalla pública en modo independiente
    root.mainloop()


# def recover_lost_window(self):
"""
    Funcion para recuperar ventana. Se necesitan guardar TODOS valores del match_state para que funcione correctamente. 
"""
#     tk.Button(self.frames.teams, text="Recuperar tablero", command=lambda:initialize_gui_scoreboard(self)).grid(row=6,column=6)
