
import tkinter as tk
from tkinter import ttk
from gui.control_panel.styles_control_panel_test import apply_styles_control_panel_test
# UI-only test panel: no functional imports (placeholders kept for reference)


class Gui_control_panel_test:
    def __init__(self, root, match_state_controller, main_panel=None):
        self.root = root
        self.root.title("ControlPanelTest")
        self.root.configure(bg="white")
        self.root.minsize(900, 600)
        self.match_state_controller = match_state_controller
        # Referencia al panel principal (opcional). Si se provee, delegamos control del timer allí.
        self.main_panel = main_panel
        # Aplicar estilos personalizados
        apply_styles_control_panel_test()

        # Configurar el grid para dividir la ventana en 1/6 y 5/6
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=7)

        # Frame izquierdo (1/6): panel de jugadores con pestañas
        self.left_frame = ttk.Frame(self.root, style="PanelTestLeft.TFrame")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Agregar notebook (pestañas)
        self.notebook = ttk.Notebook(self.left_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Pestaña Jugadores
        self.tab_jugadores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_jugadores, text="Jugadores")

        # Pestaña Ajustes
        self.tab_ajustes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ajustes, text="Ajustes")

        # Frame derecho (5/6): consola principal
        self.right_frame = ttk.Frame(self.root, style="PanelTest.TFrame")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Dividir right_frame en 2 filas y 6 columnas
        for r in range(2):
            self.right_frame.grid_rowconfigure(r, weight=1)
        for c in range(6):
            self.right_frame.grid_columnconfigure(c, weight=1)

        # Panel de cuarto simple (visible, esquina superior derecha del right_frame)
        self.quarter_panel = ttk.Frame(self.right_frame, style="PanelTestQuarter.TFrame")
        self.quarter_panel.grid(row=0, column=5, sticky="ne", padx=10, pady=10)
        self.quarter_panel_title = ttk.Label(self.quarter_panel, text="CUARTO", style="PanelTestQuarterTitle.TLabel")
        self.quarter_panel_title.pack(side="top", pady=(2, 0))
        self.quarter_panel_label = ttk.Label(
            self.quarter_panel,
            text=str(getattr(self.match_state_controller.match_state, 'quarter', 1)),
            style="PanelTestQuarter.TLabel",
        )
        self.quarter_panel_label.pack(side="top", pady=(0, 4))

        # botones - y + horizontales
        qbtns = ttk.Frame(self.quarter_panel)
        qbtns.pack(side="top")
        # Placeholders: no funcionalidad, pueden enlazarse más tarde
        self.quarter_minus_btn = ttk.Button(qbtns, text='-', width=3, style="ControlPanel.Small.TButton", command=lambda: None)
        self.quarter_plus_btn = ttk.Button(qbtns, text='+', width=3, style="ControlPanel.Small.TButton", command=lambda: None)
        self.quarter_minus_btn.pack(side='left', padx=4)
        self.quarter_plus_btn.pack(side='left', padx=4)

        # Contenedor del tiempo (esquina superior izquierda) - visual gestionada por ttk style
        self.time_container = ttk.Frame(self.right_frame, style="PanelTestTime.TFrame")
        self.time_container.grid(row=0, column=0, sticky="nw", padx=10, pady=10, rowspan=1, columnspan=1)

        # Contador de cuarto dentro del contenedor de tiempo (esquina superior derecha del tiempo)
        self.quarter_container = ttk.Frame(self.time_container, style="PanelTestQuarter.TFrame")
        # Usamos place para posicionar en la esquina superior derecha dentro del time_container
        self.quarter_container.place(relx=1.0, x=-10, y=6, anchor='ne')
        self.quarter_title = ttk.Label(self.quarter_container, text="CUARTO", style="PanelTestQuarterTitle.TLabel")
        self.quarter_title.pack(side="top", padx=6, pady=(2, 0))
        self.quarter_label = ttk.Label(
            self.quarter_container,
            text=str(getattr(self.match_state_controller.match_state, 'quarter', 1)),
            style="PanelTestQuarter.TLabel",
        )
        self.quarter_label.pack(side="top", padx=6, pady=(0, 2))

        # Botones + / - alineados horizontalmente debajo del cuarto (dentro del mismo contenedor)
        btns_frame = ttk.Frame(self.quarter_container)
        btns_frame.pack(side="top", pady=(4, 2))
        # Placeholders in time container
        self.btn_quarter_minus = ttk.Button(btns_frame, text="-", width=3, style="ControlPanel.Small.TButton", command=lambda: None)
        self.btn_quarter_plus = ttk.Button(btns_frame, text="+", width=3, style="ControlPanel.Small.TButton", command=lambda: None)
        self.btn_quarter_minus.pack(side="left", padx=4)
        self.btn_quarter_plus.pack(side="left", padx=4)

        # Label 'TIEMPO' arriba del tiempo (usando ttk.Label y estilo)
        self.label_tiempo = ttk.Label(self.time_container, text="TIEMPO", style="PanelTestTimeTitle.TLabel")
        self.label_tiempo.pack(side="top", fill="x", pady=(2, 0), ipady=0)

        # Label de tiempo sincronizado (usando ttk.Label y estilo)
        self.time_label = ttk.Label(self.time_container, text="00:00", style="PanelTestTime.TLabel")
        self.time_label.pack(side="top", pady=(0, 2), ipady=0)
        # Estado local del timer para este panel de prueba
        self._is_active_timer = False

        # Botones a la derecha del tiempo (Iniciar, Pausar, Reiniciar)
        # Se colocan en una columna al lado del contenedor de tiempo y se centran horizontalmente
        self.button_container = ttk.Frame(self.right_frame, style="ControlPanel.Stack.TFrame")
        self.button_container.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Marco interno para centrar los botones verticalmente
        self.buttons_inner = ttk.Frame(self.button_container, style="ControlPanel.Stack.TFrame")
        # Usamos pack con fill=None y anchor center para centrar verticalmente
        self.buttons_inner.pack(anchor="center", pady=10)
        # Botones (estilos definidos en styles_control_panel_test)
        # Usamos un único botón que actúa como Iniciar/Pausar/Reanudar
        # Botones visuales sin funcionalidad
        self.btn_iniciar = ttk.Button(self.buttons_inner, text="Iniciar", style="ControlPanel.Button.TButton", command=lambda: None)
        self.btn_reiniciar = ttk.Button(self.buttons_inner, text="Reiniciar", style="ControlPanel.Button.TButton", command=lambda: None)

        # Empaquetar verticalmente con separación
        self.btn_iniciar.pack(side="top", pady=6, fill='x')
        self.btn_reiniciar.pack(side="top", pady=6, fill='x')

        # UI-only: set static initial labels (no periodic updates)
        self.update_time_label()

    def update_time_label(self, force=False):
        # UI-only: set labels once from match_state if present, no recurring timers
        try:
            if getattr(self, 'time_label', None) and getattr(self.match_state_controller, 'match_state', None):
                seconds_left = getattr(self.match_state_controller.match_state, 'seconds_time_left', 0)
                minutes = seconds_left // 60
                seconds = seconds_left % 60
                self.time_label.config(text=f"{minutes:02}:{seconds:02}")
        except Exception:
            pass
        # Actualizar cuarto visuales si existen
        try:
            quarter = getattr(self.match_state_controller.match_state, 'quarter', None)
            if quarter is not None and getattr(self, 'quarter_label', None):
                self.quarter_label.config(text=str(quarter))
            if quarter is not None and getattr(self, 'quarter_panel_label', None):
                self.quarter_panel_label.config(text=str(quarter))
        except Exception:
            pass

    # Acciones vinculadas a los botones: intentan delegar en el controller si existen, sino actúan como placeholders
    def start_action(self):
        # UI-only placeholder: no functionality
        return

    def pause_action(self):
        pass

    def reset_action(self):
        # UI-only placeholder: no functionality
        return

    def _timer_tick(self):
        # UI-only: timer logic removed — placeholder for future hookup
        return

    def _quarter_plus(self):
        # UI-only placeholder
        return

    def _quarter_minus(self):
        # UI-only placeholder
        return

if __name__ == "__main__":
    # Create a minimal stub match_state_controller so the UI can be run standalone for design review
    class _StubMatchState:
        def __init__(self):
            self.seconds_time_left = 0
            self.quarter = 1

    class _StubController:
        def __init__(self):
            self.match_state = _StubMatchState()

    root = tk.Tk()
    stub = _StubController()
    app = Gui_control_panel_test(root, stub)
    root.mainloop()
