import tkinter as tk
from tkinter import filedialog, messagebox
# from PIL import Image, ImageTk
import os
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from types import SimpleNamespace
from model.team import Team


class Gui_control_panel:
    def __init__(self, root):
        self.root = root
        self.root.title("Consola de Control")
        self.root.configure(bg="gray")  
        players = []
        self.home_team = Team("","Equipo Local",0,0,[],3)
        self.away_team = Team("","Equipo Visitante",0,0,[],3)
        """
            home_team (Team): Object Team share with Gui_scoreboard.
            away_team (Team): Object Team share with Gui_scoreboard.
        """
        initialize_gui_scoreboard(self)
        setup_ui(self)
        simpleNamespace_forUi(self)
        update_team_names_and_upload_logo(self)
        

def initialize_gui_scoreboard(self):
        self.scoreboard_window = Gui_scoreboard(tk.Toplevel(self.root),self.home_team, self.away_team)
def setup_ui(self):
        ##Configura la interfaz de control sin marcador.
        self.frame = tk.Frame(self.root, bg="gray", relief=tk.RAISED)
        self.frame.pack(padx=20, pady=20)
def simpleNamespace_forUi(self):
        self.entry = SimpleNamespace()
        self.entry.home_team = SimpleNamespace()
        self.entry.away_team = SimpleNamespace()
def update_team_names_and_upload_logo(self):
    tk.Label(self.frame, text="Nombre Equipo 1:", bg="gray").grid(row=0, column=0, sticky="ew")
    self.entry.home_team.name = tk.Entry(self.frame)
    self.home_team.name = self.entry.home_team.name.get()
    self.entry.home_team.name.grid(row=0, column=1)
    tk.Button(self.frame, text="Cargar Logo", command=lambda: self.cargar_logo(1)).grid(row=0, column=2)

    tk.Label(self.frame, text="Nombre Equipo 2:").grid(row=1, column=0)
    self.away_team.name = tk.Entry(self.frame)
    self.away_team.name.grid(row=1, column=1)
    tk.Button(self.frame, text="Cargar Logo", command=lambda: self.cargar_logo(2)).grid(row=1, column=2)
    tk.Button(self.frame, text="Actualizar Nombres", command=lambda: self.scoreboard_window.update_team_names_labels()).grid(row=2, column=2)

# def buttons_points(self):
#     for i, puntos in enumerate([1, 2, 3]):
#         tk.Button(self.frame, text=f"+{puntos} Equipo 1", command=lambda p=puntos: cambiar_puntaje(self, 1, p)).grid(row=3+i, column=0)
#         tk.Button(self.frame, text=f"+{puntos} Equipo 2", command=lambda p=puntos: cambiar_puntaje(self, 2, p)).grid(row=3+i, column=1)

#     tk.Button(self.frame, text="-1 Equipo 1", command=lambda: cambiar_puntaje(self, 1, -1)).grid(row=6, column=0)
#     tk.Button(self.frame, text="-1 Equipo 2", command=lambda: cambiar_puntaje(self, 2, -1)).grid(row=6, column=1)

# def change_quarter(self):
#     tk.Label(self.frame, text="Cuarto:").grid(row=7, column=0)
#     tk.Button(self.frame, text="-", command=lambda: restar_cuarto(self)).grid(row=7, column=1)
#     tk.Button(self.frame, text="+", command=lambda: sumar_cuarto(self)).grid(row=7, column=2)

# def change_time(self):
#     tk.Label(self.frame, text="Tiempo (mm:ss):").grid(row=8, column=0)
#     self.tiempo_entry = tk.Entry(self.frame)
#     self.tiempo_entry.insert(0, "15:00")
#     self.tiempo_entry.grid(row=8, column=1)
# def buttons_for_match_time(self):
#     tk.Button(self.frame, text="Iniciar", command=lambda: iniciar_timer(self)).grid(row=9, column=0)
#     tk.Button(self.frame, text="Pausar", command=lambda: pausar_timer(self)).grid(row=9, column=1)
#     tk.Button(self.frame, text="Reset", command=lambda: reset_timer(self)).grid(row=9, column=2)
#     tk.Button(self.frame, text="Reset 24s", command=lambda: reset_poseesion(self)).grid(row=10, column=1)




       

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