from tkinter import ttk, Tk as tk
def create_players_labels(self):
        self.labels.match.players = tk.Listbox(self.root, font=("Arial", 10), fg="red") 
        self.labels.match.players.grid(row=1,column=0)
