import tkinter as tk
from gui.control_panel.gui_control_panel import Gui_control_panel
def main():
    main_window =tk.Tk()
    
    console_window = Gui_control_panel(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    main()