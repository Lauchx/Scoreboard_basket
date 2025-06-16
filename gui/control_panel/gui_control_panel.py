import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os
# from logic import (actualizar_nombres, cambiar_puntaje, iniciar_timer, pausar_timer, reset_timer,
#                    reset_poseesion, sumar_cuarto, restar_cuarto, agregar_jugador, falta_jugador)
from joystick import iniciar_joystick
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from team.model.entity.team import Team


class Gui_control_panel:
    def __init__(self, root,):
        """
        Args:
            home_team (Team): Object Team share with Gui_scoreboard.
            away_team (Team): Object Team share with Gui_scoreboard.
        """
        self.root = root
        self.root.title("Consola de Control")
        self.root.configure(bg="gray")  
        # Guardar referencia a la pantalla pública
        self.home_team = Team()
        self.away_team = Team()

        self.setup_ui()
        # Inicializar joystick
        #iniciar_joystick(self)
    def initialize_gui_scoreboard(self):
        scoreboard_window = Gui_scoreboard(tk.Toplevel(self),self.home_team, self.away_team)      

    def setup_ui(self):
        """Configura la interfaz de control sin marcador."""
        self.frame = tk.Frame(self.root, bg="gray", relief=tk.RAISED)
        self.frame.pack(padx=20, pady=20)
        # Nombres de equipos
        tk.Label(self.frame, text="Nombre Equipo 1:", bg="gray").grid(row=0, column=0, sticky="ew")
        self.nombre_equipo1 = tk.Entry(self.frame)
        self.nombre_equipo1.grid(row=0, column=1)
        tk.Button(self.frame, text="Cargar Logo", command=lambda: self.cargar_logo(1)).grid(row=0, column=2)

        tk.Label(self.frame, text="Nombre Equipo 2:").grid(row=1, column=0)
        self.nombre_equipo2 = tk.Entry(self.frame)
        self.nombre_equipo2.grid(row=1, column=1)
        tk.Button(self.frame, text="Cargar Logo", command=lambda: self.cargar_logo(2)).grid(row=1, column=2)

        tk.Button(self.frame, text="Actualizar Nombres", command=lambda: actualizar_nombres(self)).grid(row=2, column=2)

        # Botones de puntaje
        for i, puntos in enumerate([1, 2, 3]):
            tk.Button(self.frame, text=f"+{puntos} Equipo 1", command=lambda p=puntos: cambiar_puntaje(self, 1, p)).grid(row=3+i, column=0)
            tk.Button(self.frame, text=f"+{puntos} Equipo 2", command=lambda p=puntos: cambiar_puntaje(self, 2, p)).grid(row=3+i, column=1)

        tk.Button(self.frame, text="-1 Equipo 1", command=lambda: cambiar_puntaje(self, 1, -1)).grid(row=6, column=0)
        tk.Button(self.frame, text="-1 Equipo 2", command=lambda: cambiar_puntaje(self, 2, -1)).grid(row=6, column=1)

        # Botones de control de cuarto
        tk.Label(self.frame, text="Cuarto:").grid(row=7, column=0)
        tk.Button(self.frame, text="-", command=lambda: restar_cuarto(self)).grid(row=7, column=1)
        tk.Button(self.frame, text="+", command=lambda: sumar_cuarto(self)).grid(row=7, column=2)

        # Botones de control del tiempo
        tk.Label(self.frame, text="Tiempo (mm:ss):").grid(row=8, column=0)
        self.tiempo_entry = tk.Entry(self.frame)
        self.tiempo_entry.insert(0, "15:00")
        self.tiempo_entry.grid(row=8, column=1)

        tk.Button(self.frame, text="Iniciar", command=lambda: iniciar_timer(self)).grid(row=9, column=0)
        tk.Button(self.frame, text="Pausar", command=lambda: pausar_timer(self)).grid(row=9, column=1)
        tk.Button(self.frame, text="Reset", command=lambda: reset_timer(self)).grid(row=9, column=2)

        tk.Button(self.frame, text="Reset 24s", command=lambda: reset_poseesion(self)).grid(row=10, column=1)

    def cargar_logo(self, equipo):
        """Carga el logo del equipo desde 'assets/'."""
        ruta = filedialog.askopenfilename(title="Seleccionar logo", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
        if ruta:
            try:
                nombre_archivo = f"equipo{equipo}_logo.png"
                destino = os.path.join("assets", nombre_archivo)
                os.makedirs("assets", exist_ok=True)
                os.replace(ruta, destino)

                imagen = Image.open(destino)
                imagen = imagen.resize((100, 100), Image.LANCZOS)
                logo = ImageTk.PhotoImage(imagen)
                if equipo == 1:
                    self.logo1 = logo
                else:
                    self.logo2 = logo

                # Reflejar los logos en la pantalla pública
                if equipo == 1:
                    self.pantalla_publico.logo1_label.config(image=self.logo1)
                else:
                    self.pantalla_publico.logo2_label.config(image=self.logo2)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConsolaTanteador(root, None)  # Sin pantalla pública en modo independiente
    root.mainloop()