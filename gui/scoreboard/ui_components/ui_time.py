from tkinter import ttk

def create_time_labels(self):
        minutes = self.match_state.seconds_match_time // 60

        seconds = self.match_state.seconds_match_time % 60
        self.labels.match.time = ttk.Label(self.frames.match, text=f"{minutes:02}:{seconds:02}", font=("Arial", 60)) ## {minutes:02}:{seconds:02} (:02) agrega dos digitos si el numero es menor a 10
        self.labels.match.time.grid(row=0, column=1, sticky="nsew")  
