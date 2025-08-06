from tkinter import ttk
def buttons_change_possesion(self):
    ttk.Button(self.frames.match.time, text="Cambiar posesión", command=lambda: toggle_possession(self)).grid(row=2, column=4)

def toggle_possession(self):
    self.scoreboard_window.update_possession_labels()