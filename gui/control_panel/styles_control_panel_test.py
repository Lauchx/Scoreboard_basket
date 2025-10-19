from tkinter import ttk

def apply_styles_control_panel_test():
    style = ttk.Style()
    # Try to use a modern theme if available (clam, alt, default to classic if not)
    for theme in ("clam", "alt", "default", "vista"):
        try:
            style.theme_use(theme)
            break
        except Exception:
            pass
    # Fondo de los frames
    style.configure("PanelTest.TFrame", background="#e0e0e0")
    style.configure("PanelTestLeft.TFrame", background="#f0f0f0")
    # Contenedor principal del tiempo - uso de ttk para centralizar apariencia
    style.configure("PanelTestTime.TFrame", background="black", borderwidth=2, relief="ridge", padding=6)
    # Pestañas
    style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
    style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=8)
    # Label de tiempo (más grande)
    style.configure("PanelTestTime.TLabel", font=("Arial", 64, "bold"), foreground="red", background="black")
    style.configure("PanelTestTimeTitle.TLabel", font=("Arial", 16, "bold"), foreground="white", background="black")
    # Otros estilos reutilizables aquí
    # Botones de control del tiempo (Iniciar, Pausar, Reiniciar)
    style.configure("ControlPanel.Button.TButton", font=("Arial", 12, "bold"), padding=8)
    style.map("ControlPanel.Button.TButton",
              foreground=[('active', 'white')],
              background=[('active', '#4CAF50'), ('!active', '#2E7D32')])
    # Botón pequeño para operaciones auxiliares (ej. + / -)
    style.configure("ControlPanel.Small.TButton", font=("Arial", 10, "bold"), padding=4)
    style.map("ControlPanel.Small.TButton",
              foreground=[('active', 'white')],
              background=[('active', '#1976D2'), ('!active', '#1565C0')])
    # Apariencia para botones deshabilitados (visual-only mode)
    style.map("ControlPanel.Button.TButton",
              background=[('disabled', '#dddddd')],
              foreground=[('disabled', '#888888')])
    # Estilo para botones apilados (centro) - sin fondo negro para que se vea el estilo ttk
    style.configure("ControlPanel.Stack.TFrame", background="")
    # Estilo para el contador de cuarto (cuadro pequeño)
    style.configure("PanelTestQuarter.TFrame", background="black", borderwidth=1, relief="ridge", padding=4)
    style.configure("PanelTestQuarterTitle.TLabel", font=("Arial", 10, "bold"), foreground="white", background="black")
    # Mostrar el número de cuarto un poco más grande
    style.configure("PanelTestQuarter.TLabel", font=("Arial", 28, "bold"), foreground="white", background="black")
