import tkinter as tk
from tkinter import Image, filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from controller.match_state_controller import Match_state_controller
from controller.team_controller import Team_controller
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from types import SimpleNamespace
from model.team import Team


class Gui_control_panel():
    def __init__(self, root):
        self.root = root
        self.root.title("Consola de Control")
        self.root.configure(bg="gray")  
        self.root.minsize(800,300)
        simpleNamespace_forUi(self)
        home_team_controller = Team_controller(Team("","Equipo Local",0,0,[],3))
        away_team_controller = Team_controller(Team("","Equipo Visitante",0,0,[],3))
        self.match_state_controller = Match_state_controller(home_team_controller,away_team_controller,900,"Home",1)
        """
            match_state_controller.match_sate(Match_state): Object Match_state share with Gui_scoreboard.
        """
        initialize_gui_scoreboard(self)
        setup_ui(self)
        setup_ui_home_team(self)
        setup_ui_away_team(self)
        setup_ui_control(self)
        buttons_points(self)
        buttons_logo(self)
        buttons_change_possesion(self)
        buttons_for_match_time(self)
    def start_timer(self):
        time_left = self.match_state_controller.match_state.seconds_match_time
        if time_left > 0:
            self.match_state_controller.match_state.seconds_match_time -= 1
            self.scoreboard_window.update_time_labels()
            self.root.after(1000, self.start_timer)   
        else:
           print("FIN")
        
def simpleNamespace_forUi(self):
        self.entry = SimpleNamespace()
        self.entry.home_team = SimpleNamespace()
        self.entry.away_team = SimpleNamespace()
        self.entry.match = SimpleNamespace()
        #self.notebooks =SimpleNamespace()
        self.frames = SimpleNamespace()

def initialize_gui_scoreboard(self):
    self.scoreboard_window = Gui_scoreboard(tk.Toplevel(self.root),self.match_state_controller.match_state)
## setup functions
def setup_ui(self):
    self.notebook = ttk.Notebook(self.root)
    self.notebook.grid(row=0, column=0, sticky="nsew")

    self.frames.teams = ttk.Frame(self.notebook)
    self.notebook.add(self.frames.teams, text="Equipos")

    self.frames.match = ttk.Frame(self.notebook)
    self.notebook.add(self.frames.match, text="Partido", sticky="nsew")

    grid_config(self)


def setup_ui_home_team(self):
    self.frames.home_team = ttk.LabelFrame(self.frames.teams, text="Equipo Local")
    self.frames.home_team.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.frames.home_team, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.entry.home_team.name = ttk.Entry(self.frames.home_team)
    self.entry.home_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    ttk.Button(self.frames.home_team, text="Actualizar Nombre:", command=lambda: update_home_team_name(self)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    self.frames.home_team.grid_columnconfigure(1, weight=1)

def setup_ui_away_team(self):
    self.frames.away_team = ttk.LabelFrame(self.frames.teams, text="Equipo Visitante")
    self.frames.away_team.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.frames.away_team, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    self.entry.away_team.name = ttk.Entry(self.frames.away_team)
    self.entry.away_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    self.frames.away_team.grid_columnconfigure(1, weight=1)
    ttk.Button(self.frames.away_team, text="Actualizar Nombre:", command=lambda: update_away_team_name(self)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
def setup_ui_control(self):
    setup_ui_control_time_match(self)
    setup_ui_control_home_team_match(self)
    setup_ui_control_away_team_match(self)
    

def setup_ui_control_time_match(self):
    self.frames.match.time = ttk.LabelFrame(self.frames.match, text="Tiempo",)
    self.frames.match.time.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
    buttons_change_quarter(self)
    setup_ui_time(self)
    
def setup_ui_control_home_team_match(self):
    self.frames.match.home_team = ttk.LabelFrame(self.frames.match, text=self.match_state_controller.home_team_controller.team.name)
    self.frames.match.home_team.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

def setup_ui_control_away_team_match(self):
    self.frames.match.away_team = ttk.LabelFrame(self.frames.match, text=self.match_state_controller.home_team_controller.team.name)
    self.frames.match.away_team.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

def setup_ui_time(self):
    ttk.Label(self.frames.match.time, text="Minutos").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    self.entry.match.minutes_match_time = ttk.Entry(self.frames.match.time)
    self.entry.match.minutes_match_time.grid(row=1, column=1,sticky="nsew")
    ttk.Label(self.frames.match.time, text="Segundos").grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    self.entry.match.seconds_match_time = ttk.Entry(self.frames.match.time)
    self.entry.match.seconds_match_time.grid(row=1, column=3, sticky="nsew")
    ttk.Button(self.frames.match.time, text="Actualizar tiempo", command=lambda: change_time(self)).grid(row=1, column=4,sticky="nsew")

# grid config

def grid_config(self):
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)

    self.frames.teams.grid_rowconfigure(0, weight=1)
    self.frames.teams.grid_columnconfigure(0, weight=1)
    self.frames.teams.grid_columnconfigure(1, weight=1)

    self.frames.match.grid_rowconfigure(0, weight=1)
    self.frames.match.grid_columnconfigure(0, weight=1)
    self.frames.match.grid_columnconfigure(1, weight=1)

### team names functions 
def update_home_team_name(self):
    new_home_team_name = self.entry.home_team.name.get()
    self.match_state_controller.home_team_controller.change_name(new_home_team_name) 
    self.scoreboard_window.update_team_names_labels()
    self.frames.match.home_team.config(text=self.match_state_controller.home_team_controller.team.name)
 
def update_away_team_name(self):
    new_away_team_name = self.entry.away_team.name.get() 
    self.match_state_controller.away_team_controller.change_name(new_away_team_name)
    self.scoreboard_window.update_team_names_labels()

 ### logo functions   
def buttons_logo(self):
    ttk.Button(self.frames.home_team, text="Cargar Logo", command=lambda: upload_logo(self, self.match_state_controller.home_team_controller)).grid(row=0, column=2)
    ttk.Button(self.frames.away_team, text="Cargar Logo", command=lambda: upload_logo(self, self.match_state_controller.away_team_controller)).grid(row=0, column=2)

### points functions
def buttons_points(self):
    ttk.Button(self.frames.match.home_team, text=f"Sumar Punto", command=lambda: add_point(self, self.match_state_controller.home_team_controller)).grid(row=1, column=2)
    ttk.Button(self.frames.match.away_team, text=f"Sumar Punto", command=lambda: add_point(self, self.match_state_controller.away_team_controller)).grid(row=1, column=2)
    ttk.Button(self.frames.match.home_team, text=f"Restar Punto", command=lambda: substract_point(self, self.match_state_controller.home_team_controller)).grid(row=2, column=2)
    ttk.Button(self.frames.match.away_team, text=f"Restar Punto", command=lambda: substract_point(self, self.match_state_controller.away_team_controller)).grid(row=2, column=2)

def add_point(self, team_controller):
    team_controller.add_point()
    self.scoreboard_window.update_points_labels()

def substract_point(self, team_controller):
    team_controller.substract_point()
    self.scoreboard_window.update_points_labels()

### quarter functions 
def buttons_change_quarter(self):
    ttk.Label(self.frames.match.time, text="Cuarto:").grid(row=2, column=0, pady=5, padx=5, sticky="nsew")
    ttk.Button(self.frames.match.time, text="-", command=lambda: substract_quarter(self)).grid(row=2, column=1, sticky="nsew" )
    ttk.Button(self.frames.match.time, text="+", command=lambda: add_quarter(self)).grid(row=2, column=2, sticky="nsew")

def add_quarter(self):
    self.scoreboard_window.update_quarter_labels(1)
    
def substract_quarter(self):
    self.scoreboard_window.update_quarter_labels(-1)
###  possesion functions 
def buttons_change_possesion(self):
    ttk.Button(self.frames.match.time, text="Cambiar posesión", command=lambda: toggle_possession(self)).grid(row=2, column=4)

def toggle_possession(self):
    self.scoreboard_window.update_possession_labels()

### time functions 
def change_time(self):
     minutes = int(self.entry.match.minutes_match_time.get())
     seconds = int(self.entry.match.seconds_match_time.get())
     self.match_state_controller.match_state.seconds_match_time = (minutes * 60) + seconds
     self.scoreboard_window.update_time_labels()

def buttons_for_match_time(self):
    ttk.Button(self.frames.match.time, text="Iniciar", command=lambda: self.start_timer()).grid(row=1, column=5)
    # ttk.Button(self.frame, text="Pausar", command=lambda: pausar_timer(self)).grid(row=9, column=1)
    # ttk.Button(self.frame, text="Reset", command=lambda: reset_timer(self)).grid(row=9, column=2)
    # ttk.Button(self.frame, text="Reset 24s", command=lambda: reset_poseesion(self)).grid(row=10, column=1)


    



       

def upload_logo(self, teamController):
        """Carga el logo del equipo desde 'assets/'."""
        path = filedialog.askopenfilename(title="Seleccionar logo", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
        if path:
            try:
                file_name = f"{teamController.team.name}_logo.png"
                #image_asset_path  = os.path.join("assets", file_name)
                # os.makedirs("assets", exist_ok=True)
                # os.replace(path, image_asset_path)

                image = Image.open(path)
                image = image.resize((300, 300), Image.LANCZOS)
                logo = ImageTk.PhotoImage(image)

                teamController.change_logo(logo)
                self.scoreboard_window.update_team_logo_label()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_control_panel(root, None)  # Sin pantalla pública en modo independiente
    root.mainloop()