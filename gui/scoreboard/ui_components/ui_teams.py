
from tkinter import ttk, Tk as tk
def create_names_labels(self, team_labels, team_name):

        team_labels.name = ttk.Label(self.root, text=team_name, style="Teams_name.TLabel")
        team_labels.name.grid(row=1, column=0, padx=20)


def create_logos_labels(self):
        self.labels.home_team.logo = tk.Label(self.root, bg="black")
        self.labels.home_team.logo.grid(row=0, column=0, padx=10, pady=5)

        self.labels.away_team.logo = tk.Label(self.root, bg="black")
        self.labels.away_team.logo.grid(row=0, column=2, padx=10, pady=5)
def create_points_labels(self):
        self.labels.home_team.points = tk.Label(self.root, text=self.match_state.home_team.points, font=("Arial", 80), fg="orange", bg="black")
        self.labels.home_team.points.grid(row=2, column=0)
        self.labels.away_team.points = tk.Label(self.root, text=self.match_state.away_team.points, font=("Arial", 80), fg="orange", bg="black")
        self.labels.away_team.points.grid(row=2, column=2)

