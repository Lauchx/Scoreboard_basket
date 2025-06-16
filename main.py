import tkinter as tk
from gui.control_panel.gui_control_panel import Gui_control_panel
from team.model.entity.team import Team
def main():
    main_window =tk.Tk()
    
    console_window = Gui_control_panel(tk.Toplevel(main_window))
    main_window.mainloop()

if __name__ == "__main__":
    print(Team(), "team")
    main()