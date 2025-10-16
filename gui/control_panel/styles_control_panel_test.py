from tkinter import ttk

def apply_styles_control_panel_test():
    style = ttk.Style()
    # Fondo de los frames
    style.configure("PanelTest.TFrame", background="#e0e0e0")
    style.configure("PanelTestLeft.TFrame", background="#f0f0f0")
    # Pestañas
    style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
    style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=8)
    # Label de tiempo
    style.configure("PanelTestTime.TLabel", font=("Arial", 36, "bold"), foreground="red", background="black")
    style.configure("PanelTestTimeTitle.TLabel", font=("Arial", 12, "bold"), foreground="white", background="black")
    # Otros estilos reutilizables aquí
