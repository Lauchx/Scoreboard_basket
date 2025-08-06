from tkinter import ttk
from gui.control_panel.ui_components.ui_quarter import buttons_change_quarter
def start_timer(self):
        print(self.match_state_controller.match_state.seconds_match_time)
        time_left = self.match_state_controller.match_state.seconds_match_time
        if time_left > 0:
            self.match_state_controller.match_state.seconds_match_time -= 1
            self.scoreboard_window.update_time_labels()
            self.root.after(1000, lambda: start_timer(self))   
        else:
           print("FIN")

def setup_ui_time(self):
    print(self)
    ttk.Label(self.frames.match.time, text="Minutos").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    self.entry.match.minutes_match_time = ttk.Entry(self.frames.match.time)
    self.entry.match.minutes_match_time.grid(row=1, column=1,sticky="nsew")
    ttk.Label(self.frames.match.time, text="Segundos").grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    self.entry.match.seconds_match_time = ttk.Entry(self.frames.match.time)
    self.entry.match.seconds_match_time.grid(row=1, column=3, sticky="nsew")
    ttk.Button(self.frames.match.time, text="Actualizar tiempo", command=lambda: change_time(self)).grid(row=1, column=4,sticky="nsew")

def change_time(self):
     minutes = int(self.entry.match.minutes_match_time.get())
     seconds = int(self.entry.match.seconds_match_time.get())
     self.match_state_controller.match_state.seconds_match_time = (minutes * 60) + seconds
     self.scoreboard_window.update_time_labels()

def setup_ui_control_time_match(self):
    self.frames.match.time = ttk.LabelFrame(self.frames.match, text="Tiempo",)
    self.frames.match.time.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
    buttons_change_quarter(self)
    setup_ui_time(self)


def buttons_for_match_time(self):
    ttk.Button(self.frames.match.time, text="Iniciar", command=lambda: start_timer(self)).grid(row=1, column=5)
    # ttk.Button(self.frame, text="Pausar", command=lambda: pausar_timer(self)).grid(row=9, column=1)
    # ttk.Button(self.frame, text="Reset", command=lambda: reset_timer(self)).grid(row=9, column=2)
    # ttk.Button(self.frame, text="Reset 24s", command=lambda: reset_poseesion(self)).grid(row=10, column=1)