from tkinter import ttk

def apply_styles_control_panel_test():
    style = ttk.Style()
    # ─────────────────────────────────────────────
    # Tema visual base 
    # ─────────────────────────────────────────────
    for theme in ("clam", "alt", "default", "vista"):
        try:
            style.theme_use(theme)
            break
        except Exception:
            pass
    # ─────────────────────────────────────────────
    # Fondo general de paneles principales
    # ─────────────────────────────────────────────
    style.configure("PanelTest.TFrame", background="#e0e0e0")         # Fondo general
    style.configure("PanelTestLeft.TFrame", background="#f0f0f0")     # Panel lateral izquierdo
    # ─────────────────────────────────────────────
    # Panel de tiempo (cronómetro principal)
    # ─────────────────────────────────────────────
    style.configure("PanelTestTime.TFrame", borderwidth=2, relief="ridge", padding=6)
    style.configure("PanelTestTime.TLabel", font=("Arial", 64, "bold"), foreground="red", background="black")  # Número grande
    style.configure("PanelTestTimeTitle.TLabel", font=("Arial", 16, "bold"), foreground="white", background="black")  # Título
    # ─────────────────────────────────────────────
    # Pestañas (Notebook)
    # ─────────────────────────────────────────────
    style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
    style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=8)
    # ─────────────────────────────────────────────
    # Botones de control del tiempo (Iniciar, Pausar, Reiniciar)
    # ─────────────────────────────────────────────
    style.configure("ControlPanel.Button.TButton", font=("Arial", 12, "bold"), padding=8)
    style.map("ControlPanel.Button.TButton",
              foreground=[('active', 'white')],
              background=[('active', '#4CAF50'), ('!active', '#2E7D32')])
    style.map("ControlPanel.Button.TButton",
              background=[('disabled', '#dddddd')],
              foreground=[('disabled', '#888888')])
    # ─────────────────────────────────────────────
    # Botones pequeños auxiliares (+ / -) 
    # ─────────────────────────────────────────────
    style.configure("ControlPanel.Plus.TButton",
                    font=("Arial", 10, "bold"),
                    padding=4,
                    foreground="black",
                    background="#69E36D") 

    style.configure("ControlPanel.Minus.TButton",
                    font=("Arial", 10, "bold"),
                    padding=4,
                    foreground="black",
                    background="#FB8484") 
    # ─────────────────────────────────────────────
    # Contador de cuarto (cuadro con número y título)
    # ─────────────────────────────────────────────
    style.configure("PanelTestQuarter.TFrame", borderwidth=1, relief="ridge", padding=4)
    style.configure("PanelTestQuarterTitle.TLabel", font=("Arial", 10, "bold"))  # Título del cuarto
    style.configure("PanelTestQuarter.TLabel", font=("Arial", 60, "bold"))       # Número del cuarto
    # ─────────────────────────────────────────────
    # Puntos de local y vigilante (pueden tener su propio frame)
    # ─────────────────────────────────────────────
    