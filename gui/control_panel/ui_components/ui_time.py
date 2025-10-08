from tkinter import ttk
from gui.control_panel.ui_components.ui_quarter import buttons_change_quarter
def start_timer(self):  
        print(self.match_state_controller.match_state.seconds_time_left)
        time_left = self.match_state_controller.match_state.seconds_time_left
        if time_left > 0 and self.is_active_timer:
            self.match_state_controller.match_state.seconds_time_left -= 1
            self.scoreboard_window.update_time_labels()
            #self.button.start_timer.config(state="disabled") 
            self.is_active_timer = True
            self.root.after(1000, lambda: start_timer(self))  
        else:
           print("END")   

def pause_resume_timer(self):
    self.is_active_timer = not self.is_active_timer

def change_text_button_timer(self, string="Reanudar"):
    text = "Pausar" if self.is_active_timer else string
    self.button.timer.config(text=text)

def reset_timer(self):
    self.match_state_controller.match_state.seconds_time_left = self.match_state_controller.match_state.seconds_match_time
    if self.is_active_timer:
        pause_resume_timer(self)
        change_text_button_timer(self, 'Iniciar')
    self.scoreboard_window.update_time_labels()


def manage_timer(self):
    if (self.is_active_timer is not None):
        pause_resume_timer(self)  
        if self.is_active_timer:
            start_timer(self)
    else:
        self.is_active_timer = True
        start_timer(self)
    change_text_button_timer(self)
            

def setup_ui_time(self):
    print(self)
    ttk.Label(self.frames.match.time, text="Minutos").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    self.match.entry.minutes_match_time = ttk.Entry(self.frames.match.time)
    self.match.entry.minutes_match_time.grid(row=1, column=1,sticky="nsew")
    ttk.Label(self.frames.match.time, text="Segundos").grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    self.match.entry.seconds_match_time = ttk.Entry(self.frames.match.time)
    self.match.entry.seconds_match_time.grid(row=1, column=3, sticky="nsew")
    ttk.Button(self.frames.match.time, text="Actualizar tiempo", command=lambda: change_time(self)).grid(row=1, column=4,sticky="nsew")

def change_time(self):
     minutes = int(self.match.entry.minutes_match_time.get())
     seconds = int(self.match.entry.seconds_match_time.get())
     self.match_state_controller.match_state.seconds_match_time = (minutes * 60) + seconds 
     self.match_state_controller.match_state.seconds_time_left = self.match_state_controller.match_state.seconds_match_time
     self.scoreboard_window.update_time_labels()

def setup_ui_control_time_match(self):
    self.frames.match.time = ttk.LabelFrame(self.frames.match, text="Tiempo",)
    self.frames.match.time.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
    buttons_change_quarter(self)
    setup_ui_time(self)

def buttons_for_match_time(self):
    self.button.timer = ttk.Button(self.frames.match.time, text="Iniciar", command=lambda: manage_timer(self))
    self.button.timer.grid(row=1, column=5)
    self.button.reset_timer = ttk.Button(self.frames.match.time, text="Reset", command=lambda: reset_timer(self))
    self.button.reset_timer.grid(row=1, column=6)
