
import tkinter as tk
from tkinter import ttk
from gui.control_panel.styles_control_panel_test import apply_styles_control_panel_test



class Gui_control_panel_test:
    def __init__(self, root, match_state_controller):
        self.root = root
        self.root.title("ControlPanelTest")
        self.root.configure(bg="white")
        self.root.minsize(900, 600)
        self.match_state_controller = match_state_controller
        # Aplicar estilos personalizados
        apply_styles_control_panel_test()

        # Configurar el grid para dividir la ventana en 1/6 y 5/6
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=7)

        # Frame izquierdo (1/6): panel de jugadores con pestañas
        self.left_frame = ttk.Frame(self.root, style="PanelTestLeft.TFrame")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Agregar notebook (pestañas)
        self.notebook = ttk.Notebook(self.left_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Pestaña Jugadores
        self.tab_jugadores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_jugadores, text="Jugadores")

        # Pestaña Ajustes
        self.tab_ajustes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ajustes, text="Ajustes")

        # Frame derecho (5/6): consola principal
        self.right_frame = ttk.Frame(self.root, style="PanelTest.TFrame")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Dividir right_frame en 2 filas y 6 columnas
        for r in range(2):
            self.right_frame.grid_rowconfigure(r, weight=1)
        for c in range(6):
            self.right_frame.grid_columnconfigure(c, weight=1)

        # Contenedor del tiempo (esquina superior izquierda)
        self.time_container = tk.Frame(self.right_frame, bg="black", bd=2, relief="ridge")
        self.time_container.grid(row=0, column=0, sticky="nw", padx=10, pady=10, rowspan=1, columnspan=1)

        # Label 'TIEMPO' arriba del tiempo (usando ttk.Label y estilo)
        self.label_tiempo = ttk.Label(self.time_container, text="TIEMPO", style="PanelTestTimeTitle.TLabel")
        self.label_tiempo.pack(side="top", fill="x", pady=(2,0), ipady=0)

        # Label de tiempo sincronizado (usando ttk.Label y estilo)
        self.time_label = ttk.Label(self.time_container, text="00:00", style="PanelTestTime.TLabel")
        self.time_label.pack(side="top", pady=(0,2), ipady=0)
        self.update_time_label()

    def update_time_label(self, force=False):
        seconds_left = self.match_state_controller.match_state.seconds_time_left
        minutes = seconds_left // 60
        seconds = seconds_left % 60
        self.time_label.config(text=f"{minutes:02}:{seconds:02}")
        if not force:
            self.root.after(500, self.update_time_label)

if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_control_panel_test(root)
    root.mainloop()
