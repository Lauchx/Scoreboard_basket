import tkinter as tk
from tkinter import Image, filedialog, messagebox, ttk
# from PIL import Image, ImageTk
import os
from controller.match_state_controller import Match_state_controller
from controller.team_controller import Team_controller
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from types import SimpleNamespace
from model.team import Team
##from model.time.match_time import Match_time


class Gui_control_panel:
    def __init__(self, root):
        self.root = root
        self.root.title("Consola de Control")
        self.root.configure(bg="gray")  
        simpleNamespace_forUi(self)
        home_team_controller = Team_controller(Team("","Equipo Local",0,0,[],3))
        away_team_controller = Team_controller(Team("","Equipo Visitante",0,0,[],3))
        ###match_time = Match_time(15,0) # 15 minutos de tiempo de juego (No debe estar hardcodeado)
       ### self.match_state = Match_state_controller(home_team_controller,away_team_controller,match_time,"Home")
        self.match_state_controller = Match_state_controller(home_team_controller,away_team_controller,"Home",1)

        """
            home_team (Team): Object Team share with Gui_scoreboard.
            away_team (Team): Object Team share with Gui_scoreboard.
        """
        initialize_gui_scoreboard(self)
        setup_ui(self)
        setup_ui_home_team(self)
        setup_ui_away_team(self)
        buttons_points(self)
        buttons_logo(self)
        buttons_change_possesion(self)
        #change_time(self)
        
def simpleNamespace_forUi(self):
        self.entry = SimpleNamespace()
        self.entry.home_team = SimpleNamespace()
        self.entry.away_team = SimpleNamespace()
        self.match = SimpleNamespace()
        self.notebooks =SimpleNamespace()
        self.frames = SimpleNamespace()

def initialize_gui_scoreboard(self):
    self.scoreboard_window = Gui_scoreboard(tk.Toplevel(self.root),self.match_state_controller.match_state)
def setup_ui(self):
    self.notebooks.teams = ttk.Notebook(self.root)
    self.notebooks.teams.grid(row=0, column=0, sticky="nsew")
    self.frames.teams = ttk.Frame(self.notebooks.teams)
    self.notebooks.teams.add(self.frames.teams, text="Equipos")

    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.frames.teams.grid_rowconfigure(0, weight=1)
    self.frames.teams.grid_columnconfigure(0, weight=1)
    self.frames.teams.grid_columnconfigure(1, weight=1)
def setup_ui_home_team(self):
    self.frames.home_team = ttk.LabelFrame(self.frames.teams, text="Equipo Local")
    self.frames.home_team.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.frames.home_team, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.entry.home_team.name = ttk.Entry(self.frames.home_team)
    self.entry.home_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    ttk.Button(self.frames.home_team, text="Actualizar Nombre:", command=lambda: update_home_team_name(self)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    self.frames.home_team.grid_columnconfigure(1, weight=1)
    ##ttk.Button(self.frames.home_team, text="Sumar Cuarto  Visitante", command=lambda: update_team_names(self)).grid(row=2, column=3)
def setup_ui_away_team(self):
    self.frames.away_team = ttk.LabelFrame(self.frames.teams, text="Equipo Visitante")
    self.frames.away_team.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    ttk.Label(self.frames.away_team, text="Nombre Equipo 2:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.entry.away_team.name = ttk.Entry(self.frames.away_team)
    self.entry.away_team.name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    self.frames.away_team.grid_columnconfigure(1, weight=1)
    ttk.Button(self.frames.away_team, text="Actualizar Nombre:", command=lambda: update_away_team_name(self)).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    # self.frames.away_team = ttk.Frame(self.notebooks.teams)
    # self.notebooks.teams.add(self.frames.away_team, text="Equipo Visitante")

    # tk.Label(self.frames.away_team, text="Nombre Equipo 2:").grid(row=1, column=0)
    # self.entry.away_team.name = tk.Entry(self.frames.away_team)
    # self.entry.away_team.name.grid(row=1, column=1)


### team names functions 
def update_home_team_name(self):
    new_home_team_name = self.entry.home_team.name.get()
    self.match_state_controller.home_team_controller.change_name(new_home_team_name) 
    self.scoreboard_window.update_team_names_labels()
 ### logo functions    
def update_away_team_name(self):
    new_away_team_name = self.entry.away_team.name.get() 
    self.match_state_controller.away_team_controller.change_name(new_away_team_name)
    self.scoreboard_window.update_team_names_labels()
def buttons_logo(self):
    ttk.Button(self.frames.home_team, text="Cargar Logo", command=lambda: self.cargar_logo(1)).grid(row=0, column=2)
    ttk.Button(self.frames.away_team, text="Cargar Logo", command=lambda: self.cargar_logo(2)).grid(row=1, column=2)
### points functions
def buttons_points(self):
    ttk.Button(self.frames.home_team, text=f"Equipo 1 +1", command=lambda: add_point(self, self.match_state_controller.home_team_controller)).grid(row=3, column=0)
    ttk.Button(self.frames.away_team, text=f"Equipo 2 +1", command=lambda: add_point(self, self.match_state_controller.away_team_controller)).grid(row=3, column=1)

def add_point(self, team_controller):
    team_controller.add_point()
    self.scoreboard_window.update_points_labels()
### quarter functions 
def buttons_change_quarter(self):
    ttk.Label(self.frame, text="Cuarto:", bg="gray").grid(row=7, column=0)
    ttk.Button(self.frame, text="-", command=lambda: substract_quarter(self)).grid(row=7, column=1)
    ttk.Button(self.frame, text="+", command=lambda: add_quarter(self)).grid(row=7, column=2)
def add_quarter(self):
    self.scoreboard_window.update_quarter_labels(1)
def substract_quarter(self):
    self.scoreboard_window.update_quarter_labels(-1)
###  possesion functions 
def buttons_change_possesion(self):
    print("nop")
   ## tk.Button(self.frame, text="Cambiar posesión", command=lambda: toggle_possession(self)).grid(row=9, column=1)
def toggle_possession(self):
    self.scoreboard_window.update_possession_labels()
### time functions 
# def change_time(self):
#     tk.Label(self.frame, text="Tiempo (mm:ss):", bg="gray").grid(row=2, column=0)
#     self.tiempo_entry = tk.Entry(self.frame)
#     self.tiempo_entry.insert(0, "15:00")
#     self.tiempo_entry.grid(row=2, column=1)
# def buttons_for_match_time(self):
#     tk.Button(self.frame, text="Iniciar", command=lambda: start_timer(self)).grid(row=9, column=0)
#     # tk.Button(self.frame, text="Pausar", command=lambda: pausar_timer(self)).grid(row=9, column=1)
#     # tk.Button(self.frame, text="Reset", command=lambda: reset_timer(self)).grid(row=9, column=2)
#     # tk.Button(self.frame, text="Reset 24s", command=lambda: reset_poseesion(self)).grid(row=10, column=1)
# def start_timer(self):
#     time =  self.scoreboard_window.get_time_match()
    



       

# def cargar_logo(self, equipo):
#         """Carga el logo del equipo desde 'assets/'."""
#         ruta = filedialog.askopenfilename(title="Seleccionar logo", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
#         if ruta:
#             try:
#                 nombre_archivo = f"equipo{equipo}_logo.png"
#                 destino = os.path.join("assets", nombre_archivo)
#                 os.makedirs("assets", exist_ok=True)
#                 os.replace(ruta, destino)

#                 imagen = Image.open(destino)
#                 imagen = imagen.resize((100, 100), Image.LANCZOS)
#                 logo = ImageTk.PhotoImage(imagen)
#                 if equipo == 1:
#                     self.logo1 = logo
#                 else:
#                     self.logo2 = logo

#                 # Reflejar los logos en la pantalla pública
#                 if equipo == 1:
#                     self.pantalla_publico.logo1_label.config(image=self.logo1)
#                 else:
#                     self.pantalla_publico.logo2_label.config(image=self.logo2)
#             except Exception as e:
#                 messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_control_panel(root, None)  # Sin pantalla pública en modo independiente
    root.mainloop()