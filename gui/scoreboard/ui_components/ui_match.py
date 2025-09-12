from tkinter import ttk

def create_quarter_labels(self):
        self.labels.match.quarter = ttk.Label(self.frames.match, text=str(f"Cuarto: {self.match_state.quarter}"), font=("Arial", 30))
        self.labels.match.quarter.grid(row=1, column=0, sticky="nsew")

def create_possession_labels(self):
        self.labels.match.possession = ttk.Label(self.frames.match, text="⇦", font=("Arial", 200))
        self.labels.match.possession.grid(row=2, column=0, sticky="nsew")

        self.labels.match.poseesion_text = ttk.Label(self.frames.match, text="POSESIÓN", font=("Arial", 30))
        self.labels.match.poseesion_text.grid(row=3, column=0, sticky="nsew")
def setup_ui_match(self):
        self.frames.match = ttk.Frame(self.root)
        self.frames.match.grid(row=0, column=1, sticky="nsew")
        for c in range(2):
                self.frames.match.grid_columnconfigure(c, weight=1)
                self.frames.match.grid_rowconfigure(c,weight=1)
        
