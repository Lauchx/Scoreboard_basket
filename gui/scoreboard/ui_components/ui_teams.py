from tkinter import ttk

def create_names_labels(team_frame, team_labels, team_name):
        team_labels.name = ttk.Label(team_frame, text=team_name, style="Teams_name.TLabel")
        team_labels.name.grid(row=1, column=1, padx=20, sticky="nsew")

def create_logos_labels(team_frame, team_labels):
        team_labels.logo = ttk.Label(team_frame)
        team_labels.logo.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

def create_points_labels(team_frame, team_labels, points_team):
        team_labels.points = ttk.Label(team_frame, text=points_team, font=("Arial", 80))
        team_labels.points.grid(row=2, column=1, sticky="nsew")

def teams_labels_grid_configure(team_frame):
        for c in range(4):
                team_frame.grid_columnconfigure(c, weight=1)