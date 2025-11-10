"""
Componentes UI modernos para información del partido (cuarto, posesión).
Diseño profesional tipo NBA/FIBA.
"""

from tkinter import ttk


def create_quarter_labels_modern(self):
    """
    Crea el label del cuarto/período con estilo moderno.
    
    Args:
        self: Instancia de Gui_scoreboard
    """
    self.match.labels.quarter = ttk.Label(
        self.frames.match,
        text=f"Cuarto: {self.match_state.quarter}",
        style="Quarter.TLabel"
    )
    self.match.labels.quarter.grid(row=1, column=0, sticky="nsew", pady=(10, 0))


def create_possession_labels_modern(self):
    """
    Crea los labels de posesión con estilo moderno (flecha grande + texto).
    
    Args:
        self: Instancia de Gui_scoreboard
    """
    # Flecha de posesión (grande, estilo neón)
    self.match.labels.possesion = ttk.Label(
        self.frames.match, 
        text="-", 
        style="Possession.TLabel"
    )
    self.match.labels.possesion.grid(row=2, column=0, sticky="nsew")
    
    # Texto "POSESION"
    self.match.labels.possesion_text = ttk.Label(
        self.frames.match,
        text="POSESIÓN",
        style="PossessionText.TLabel"
    )
    self.match.labels.possesion_text.grid(row=3, column=0, sticky="nsew", pady=(10, 0))


def setup_ui_match_modern(self):
    """
    Configura el frame central del partido con estilo moderno.
    
    Args:
        self: Instancia de Gui_scoreboard
    """
    self.frames.match = ttk.Frame(self.root, style="CenterPanel.TFrame", padding=(20, 15))
    self.frames.match.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
    
    # Configurar grid responsive
    self.frames.match.grid_columnconfigure(0, weight=1)
    
    # Pesos de las filas: tiempo (2), cuarto (1), posesión (3), texto posesión (1)
    row_weights = (2, 1, 3, 1)
    for index, weight in enumerate(row_weights):
        self.frames.match.grid_rowconfigure(index, weight=weight)

