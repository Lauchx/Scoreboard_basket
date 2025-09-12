import tkinter as tk
def create_players_labels(team_frame, team_label, is_home_team):
        team_label.players = tk.Listbox(team_frame, font=("Arial", 10)) 
        if is_home_team:
                team_label.players.grid(row=1,column=0, sticky="nsew")
        else:
                team_label.players.grid(row=1,column=3, sticky="nsew")


