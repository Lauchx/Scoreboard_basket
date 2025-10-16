from tkinter import ttk

def create_time_labels(self):
    minutes = self.match_state.seconds_time_left // 60

    seconds = self.match_state.seconds_time_left % 60
    self.match.labels.time = ttk.Label(
        self.frames.match,
        text=f"{minutes:02}:{seconds:02}",
        font=("Arial", 60),
        background="blue",
    )
    self.match.labels.time.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
    # Asegurar que self.labels.match.time apunte al label correcto
    if hasattr(self, 'labels') and hasattr(self.labels, 'match'):
        self.labels.match.time = self.match.labels.time
