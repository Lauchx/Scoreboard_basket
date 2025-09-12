from tkinter import ttk, Tk as tk

def create_quarter_labels(self):
        self.labels.match.quarter = tk.Label(self.root, text=str(f"Cuarto: {self.match_state.quarter}"), font=("Arial", 30), fg="white", bg="black")
        self.labels.match.quarter.grid(row=1, column=1)

def create_possession_labels(self):
        self.labels.match.possession = tk.Label(self.root, text="⇦", font=("Arial", 200), fg="red", bg="black")
        self.labels.match.possession.grid(row=2, column=1)

        self.labels.match.poseesion_text = tk.Label(self.root, text="POSESIÓN", font=("Arial", 30), fg="white", bg="black")
        self.labels.match.poseesion_text.grid(row=3, column=1)