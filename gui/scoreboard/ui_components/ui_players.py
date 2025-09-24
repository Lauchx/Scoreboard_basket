import tkinter as tk

def create_players_labels(team_simple_name_space, is_home_team):
    team_simple_name_space.labels.players = tk.Listbox(team_simple_name_space.frames, font=("Arial", 10))
    col = 0 if is_home_team else 2
    padding = (0, 15) if is_home_team else (15, 0)
    team_simple_name_space.labels.players.grid(row=0, column=col, rowspan=3, sticky="nsew", padx=padding, pady=5)
