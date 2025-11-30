import tkinter as tk

#main
from gui.control_panel.gui_control_panel import Gui_control_panel

from styles import apply_general_styles

def main():
    main_window = tk.Tk()
    apply_general_styles()
    console_window = Gui_control_panel(main_window)
    # Lanzar ventana de test como segunda ventana, compartiendo el match_state_controller
    #test_window = tk.Toplevel(main_window)
   
    main_window.mainloop()

if __name__ == "__main__":
    main()