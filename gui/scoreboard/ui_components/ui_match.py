from tkinter import ttk

def create_quarter_labels(self):
    self.labels.match.quarter = ttk.Label(
        self.frames.match,
        text=str(f"Cuarto: {self.match_state.quarter}"),
        font=("Arial", 30),
    )
    self.labels.match.quarter.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

def create_possession_labels(self):
    self.labels.match.possession = ttk.Label(self.frames.match, text="-", font=("Arial", 200))
    self.labels.match.possession.grid(row=2, column=0, sticky="nsew")

    self.labels.match.poseesion_text = ttk.Label(
        self.frames.match,
        text="POSESION",
        font=("Arial", 30),
    )
    self.labels.match.poseesion_text.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

def setup_ui_match(self):
    self.frames.match = ttk.Frame(self.root, padding=(20, 15))
    self.frames.match.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
    self.frames.match.grid_columnconfigure(0, weight=1)
    row_weights = (2, 1, 3, 1)
    for index, weight in enumerate(row_weights):
        self.frames.match.grid_rowconfigure(index, weight=weight)
