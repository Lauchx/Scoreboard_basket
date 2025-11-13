from tkinter import ttk

def apply_styles_control_panel_test():
    style = ttk.Style()
    # Tema visual base 
    for theme in ("xpnative","clam", "alt", "default", "vista"):
        try:
            style.theme_use(theme)
            break
        except Exception:
            pass
    # Fondo general de paneles principales
    style.configure("PanelTest.TFrame", background="#e0e0e0")         # Fondo general
    style.configure("PanelTestLeft.TFrame", background="#f0f0f0")     # Panel lateral izquierdo
    # Panel de tiempo (cronómetro principal)
    style.configure("PanelTestTime.TFrame", borderwidth=2, relief="ridge", padding=6)
    style.configure("PanelTestTime.TLabel", font=("Arial", 72, "bold"), foreground="red", background="black")  # Aumentado para responsividad
    style.configure("PanelTestTimeTitle.TLabel", font=("Arial", 18, "bold"), foreground="white", background="black")  # Aumentado
    # Pestañas (Notebook)
    style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
    style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=8)
    
    # Pestañas internas (más pequeñas para Local/Visitante)
    style.configure("Compact.TNotebook", background="#f0f0f0", borderwidth=0)
    style.configure("Compact.TNotebook.Tab", font=("Arial", 9, "bold"), padding=4)
    # Botones de control del tiempo (Iniciar, Pausar, Reiniciar)
    style.configure("ControlPanel.Button.TButton", font=("Arial", 12, "bold"), padding=8)
    """  style.map("ControlPanel.Button.TButton",
                background=[('disabled', '#dddddd')],
                foreground=[('disabled', '#888888')]) """
    # Botones pequeños auxiliares (+ / -) 
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
    # Contador de cuarto (cuadro con número y título)
    style.configure("PanelTestQuarter.TFrame", borderwidth=1, relief="ridge", padding=4)
    style.configure("PanelTestQuarterTitle.TLabel", font=("Arial", 10, "bold"))  # Título del cuarto
    style.configure("PanelTestQuarter.TLabel", font=("Arial", 60, "bold"))       # Número del cuarto
 
    # Puntos de local y visitante
    style.configure("PanelTestScore.TFrame", background="black", borderwidth=2, relief="ridge", padding=6)

    style.configure("PanelTestScoreTitle.TLabel",
                font=("Arial", 18, "bold"),
                foreground="white",
                background="black")

    style.configure("PanelTestScore.TLabel",
                font=("Arial", 64, "bold"),
                foreground="white",
                background="black")
    
    # Panel de faltas (local y visitante)
    style.configure("PanelFouls.TFrame",
        borderwidth=1,
        relief="ridge",
        padding=4
    )

    style.configure("PanelFoulsTitle.TLabel",
        font=("Arial", 10, "bold"),
        foreground="black",
        background="#e0e0e0"
    )

    style.configure("PanelFouls.TLabel",
        font=("Arial", 60, "bold"),
        foreground="black",
    )
    
    # Botón borrar faltas
    style.configure("ControlPanel.ClearFouls.TButton",
        font=("Arial", 12, "bold"),
        padding=8
    )

    style.map("ControlPanel.ClearFouls.TButton",
        foreground=[('active', 'white')],
        background=[('active', '#4CAF50'), ('!active', '#2E7D32')],
    )

    style.map("ControlPanel.ClearFouls.TButton",
        background=[('disabled', '#dddddd')],
        foreground=[('disabled', '#888888')],
    )

### ESTILOS LEFT ##
    # Estilos escalables para panel izquierdo (Jugadores y Equipos)
    style.configure("PlayerForm.TLabel",
        font=("Arial", 9),
        foreground="black",
        background="#f0f0f0"
    )

    style.configure("PlayerForm.TEntry",
        font=("Arial", 9),
        padding=2
    )

    style.configure("PlayerForm.TCombobox",
        font=("Arial", 9),
        padding=1
    )

    style.configure("PlayerForm.TButton",
        font=("Arial", 9, "bold"),
        padding=3
    )

    style.map("PlayerForm.TButton",
        foreground=[('active', 'white')],
        background=[('active', '#1976D2'), ('!active', '#1565C0')],
    )

    style.map("PlayerForm.TButton",
        background=[('disabled', '#cccccc')],
        foreground=[('disabled', '#888888')],
    )

    # Estilo compacto para Treeview de jugadores
    style.configure("Compact.Treeview",
        font=("Arial", 8),
        rowheight=16
    )
    style.configure("Compact.Treeview.Heading",
        font=("Arial", 8, "bold")
    )