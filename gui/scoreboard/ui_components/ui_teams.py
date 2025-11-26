import tkinter as tk
from tkinter import ttk

def create_names_labels(team_frame, team_labels, team_name):
    team_labels.name = ttk.Label(team_frame, text=team_name, style="Teams_name.TLabel")
    team_labels.name.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="nsew")

def create_logos_labels(team_frame, team_labels):
    # Usar tk.Label para centrar el logo correctamente
    team_labels.logo = tk.Label(team_frame, bg='black', anchor='center')
    team_labels.logo.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

def create_points_labels(team_frame, team_labels, points_team):
    team_labels.points = ttk.Label(team_frame, text=points_team, font=("Arial", 80), anchor="center")
    team_labels.points.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="nsew")

def teams_labels_grid_configure(team_frame):
#       column_weights = {0: 2, 1: 3, 2: 2}
#       for column, weight in column_weights.items():
#         team_frame.grid_columnconfigure(column, weight=weight, uniform="team")
        for column in range(3):
                team_frame.grid_columnconfigure(column, weight=1)
        for row in range(3):
                team_frame.grid_rowconfigure(row, weight=1)
