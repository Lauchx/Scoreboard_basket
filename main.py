import tkinter as tk
from gui.control_panel.gui_control_panel import Gui_control_panel
from gui.control_panel.gui_control_panel_test import Gui_control_panel_test
from styles import apply_general_styles

def main():
    main_window = tk.Tk()
    apply_general_styles()
    console_window = Gui_control_panel(main_window)
    # Lanzar ventana de test como segunda ventana, compartiendo el match_state_controller
    test_window = tk.Toplevel(main_window)
    test_panel = Gui_control_panel_test(test_window, console_window.match_state_controller)
    # Referencia cruzada para actualización centralizada
    # (asume que el objeto self de ui_time.py es el mismo que console_window)
    if hasattr(console_window, 'control_panel_test'):
        console_window.control_panel_test = test_panel
    else:
        setattr(console_window, 'control_panel_test', test_panel)
    main_window.mainloop()

if __name__ == "__main__":
    main()