import tkinter as tk
from tkinter import ttk

def create_time_labels(self):
    minutes = self.match_state.seconds_time_left // 60
    seconds = self.match_state.seconds_time_left % 60

    # Usar tk.Label para poder configurar width y highlightbackground
    self.match.labels.time = tk.Label(
        self.frames.match,
        text=f"{minutes:02}:{seconds:02}",
        font=("Arial", 60),
        bg="blue",
        fg="white",
        anchor="center",
        width=5,  # ANCHO FIJO: 5 caracteres para evitar que cambie de tamaño
        highlightbackground='#ffffff',  # Borde blanco
        highlightcolor='#ffffff',
        highlightthickness=2,
        relief='solid',
        borderwidth=2
    )  # {minutes:02}:{seconds:02} -> (:02) agrega dos digitos si el numero es menor a 10
    self.match.labels.time.grid(row=0, column=0, sticky="nsew", pady=(0, 10))