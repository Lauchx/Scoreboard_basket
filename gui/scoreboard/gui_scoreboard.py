import tkinter as tk
from types import SimpleNamespace
class Gui_scoreboard:
    def __init__(self, root, home_team, away_team ):
        """
        Args:
            home_team (Team): Objeto Team compartido con Gui_control_panel.
            away_team (Team): Objeto Team compartido con Gui_control_panel.
        """
        self.root = root
        self.root.title("Scoreboard")
        self.root.configure(bg="black")
        simpleNamespace_forUi(self)
        self.home_team = home_team
        self.away_team = away_team
        self.match.quarter = 1
        create_logos_labels(self)
        create_names_labels(self)
        create_time_labels(self)
        create_points_labels(self)
        create_quarter_labels(self)
        create_possession_labels(self)
    # Updates labels functions
    def update_points_labels(self):
        self.labels.home_team.points.config(text=str(self.home_team.points))
        self.labels.away_team.points.config(text=str(self.away_team.points))
    def update_time_labels(self, time):
        self.labels.match.time.config(text=str(time))
    def update_possession_labels(self, possession):
        self.labels.match.possession.config(text=possession)    
    def update_team_names_labels(self):
        self.labels.home_team.name.config(text=self.home_team.name)
        self.labels.away_team.name.config(text=self.away_team.name)
    def update_quarter_labels(self, number):
        self.match.quarter += number
        self.labels.match.quarter.config(text=f"Cuarto: {self.match.quarter}")
    def update_possession_labels(self):
        current_possesion = self.labels.match.possession["text"]
        new_possesion = "<-" if current_possesion == "->" else "->"
        self.labels.match.possession.config(text=str(new_possesion))
def simpleNamespace_forUi(self):
        self.labels = SimpleNamespace()
        self.labels.home_team = SimpleNamespace()
        self.labels.away_team = SimpleNamespace()
        self.labels.match = SimpleNamespace()
        self.match = SimpleNamespace()
# Create functions labels
def get_time_match(self):
      return float(self.labels.match.time)
def create_names_labels(self):
        self.labels.home_team.name = tk.Label(self.root, text=self.home_team.name, font=("Arial", 40, "bold"), fg="white", bg="black")
        self.labels.home_team.name.grid(row=1, column=0, padx=20)

        self.labels.away_team.name = tk.Label(self.root, text=self.away_team.name, font=("Arial", 40, "bold"), fg="white", bg="black")
        self.labels.away_team.name.grid(row=1, column=2, padx=20)
def create_logos_labels(self):
        self.labels.home_team.logo = tk.Label(self.root, bg="black")
        self.labels.home_team.logo.grid(row=0, column=0, padx=10, pady=5)

        self.labels.away_team.logo = tk.Label(self.root, bg="black")
        self.labels.away_team.logo.grid(row=0, column=2, padx=10, pady=5)
def create_time_labels(self):
        self.labels.match.time = tk.Label(self.root, text="15:00", font=("Arial", 60), fg="white", bg="black")
        self.labels.match.time.grid(row=0, column=1)
    
def create_points_labels(self):
        self.labels.home_team.points = tk.Label(self.root, text=self.home_team.points, font=("Arial", 80), fg="orange", bg="black")
        self.labels.home_team.points.grid(row=2, column=0)
        self.labels.away_team.points = tk.Label(self.root, text=self.away_team.points, font=("Arial", 80), fg="orange", bg="black")
        self.labels.away_team.points.grid(row=2, column=2)
    
def create_quarter_labels(self):
        self.labels.match.quarter = tk.Label(self.root, text=str(f"Cuarto: {self.match.quarter}"), font=("Arial", 30), fg="white", bg="black")
        self.labels.match.quarter.grid(row=1, column=1)

def create_possession_labels(self):
        self.labels.match.possession = tk.Label(self.root, text="->", font=("Arial", 50), fg="red", bg="black")
        self.labels.match.possession.grid(row=2, column=1)

        self.labels.match.poseesion_text = tk.Label(self.root, text="POSESIÓN", font=("Arial", 30), fg="white", bg="black")
        self.labels.match.poseesion_text.grid(row=3, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_scoreboard(root)
    root.mainloop()