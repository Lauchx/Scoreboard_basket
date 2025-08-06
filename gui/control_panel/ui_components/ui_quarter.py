from tkinter import ttk
def buttons_change_quarter(self):
    ttk.Label(self.frames.match.time, text="Cuarto:").grid(row=2, column=0, pady=5, padx=5, sticky="nsew")
    ttk.Button(self.frames.match.time, text="-", command=lambda: substract_quarter(self)).grid(row=2, column=1, sticky="nsew" )
    ttk.Button(self.frames.match.time, text="+", command=lambda: add_quarter(self)).grid(row=2, column=2, sticky="nsew")

def add_quarter(self):
    self.scoreboard_window.update_quarter_labels(1)
    
def substract_quarter(self):
    self.scoreboard_window.update_quarter_labels(-1)