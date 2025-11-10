"""
Componente UI para personalización de colores del scoreboard en tiempo real.
Permite al usuario ajustar colores según condiciones de iluminación.
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox


def setup_color_customization_ui(control_panel):
    """
    Crea la interfaz de personalización de colores en la pestaña Configuración.
    Solo se muestra si el diseño moderno está activado.

    Args:
        control_panel: Instancia de Gui_control_panel
    """
    # Verificar si el scoreboard tiene diseño moderno activado
    scoreboard = control_panel.scoreboard_window
    if not (hasattr(scoreboard, 'modern_style') and scoreboard.modern_style):
        # Si no hay diseño moderno, mostrar mensaje informativo
        info_frame = ttk.LabelFrame(
            control_panel.frames.config,
            text="ℹ️ Personalización de Colores",
            padding=(15, 10)
        )
        info_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        info_label = ttk.Label(
            info_frame,
            text="La personalización de colores solo está disponible con el diseño moderno.\n"
                 "Activa USE_MODERN_DESIGN = True en gui/scoreboard/gui_scoreboard.py",
            font=('Arial', 9, 'italic'),
            justify='center'
        )
        info_label.pack(pady=10)
        return

    # Frame principal para personalización de colores
    color_frame = ttk.LabelFrame(
        control_panel.frames.config,
        text="🎨 Personalización de Colores del Tablero",
        padding=(15, 10)
    )
    color_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    # Instrucciones
    instructions = ttk.Label(
        color_frame,
        text="Ajusta los colores del tablero según las condiciones de iluminación:",
        font=('Arial', 9, 'italic')
    )
    instructions.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")
    
    # Crear controles de color
    row = 1
    
    # === FONDOS ===
    ttk.Label(color_frame, text="FONDOS", font=('Arial', 10, 'bold')).grid(
        row=row, column=0, columnspan=4, sticky="w", pady=(5, 5)
    )
    row += 1
    
    create_color_picker(control_panel, color_frame, row, 0,
                       "Fondo Principal:", "bg_primary",
                       "Color de fondo principal del tablero")
    
    create_color_picker(control_panel, color_frame, row, 2,
                       "Fondo Panel Central:", "bg_center",
                       "Color del panel central (tiempo, posesión)")
    row += 1
    
    create_color_picker(control_panel, color_frame, row, 0,
                       "Fondo Equipo Local:", "bg_team_home",
                       "Color de fondo del equipo local")
    
    create_color_picker(control_panel, color_frame, row, 2,
                       "Fondo Equipo Visitante:", "bg_team_away",
                       "Color de fondo del equipo visitante")
    row += 1
    
    # === TEXTOS Y NÚMEROS ===
    ttk.Label(color_frame, text="TEXTOS Y NÚMEROS", font=('Arial', 10, 'bold')).grid(
        row=row, column=0, columnspan=4, sticky="w", pady=(15, 5)
    )
    row += 1
    
    create_color_picker(control_panel, color_frame, row, 0,
                       "Nombres de Equipos:", "text_primary",
                       "Color de los nombres de los equipos")
    
    create_color_picker(control_panel, color_frame, row, 2,
                       "Puntajes:", "display_score",
                       "Color de los puntajes")
    row += 1
    
    create_color_picker(control_panel, color_frame, row, 0,
                       "Reloj/Tiempo:", "display_time",
                       "Color del reloj del partido")
    
    create_color_picker(control_panel, color_frame, row, 2,
                       "Cuarto:", "accent_orange",
                       "Color del indicador de cuarto")
    row += 1
    
    # === JUGADORES ===
    ttk.Label(color_frame, text="JUGADORES", font=('Arial', 10, 'bold')).grid(
        row=row, column=0, columnspan=4, sticky="w", pady=(15, 5)
    )
    row += 1
    
    create_color_picker(control_panel, color_frame, row, 0,
                       "Jugadores Activos:", "accent_neon",
                       "Color de los jugadores en cancha")
    
    create_color_picker(control_panel, color_frame, row, 2,
                       "Jugadores Inactivos:", "text_dim",
                       "Color de los jugadores en el banco")
    row += 1
    
    # === POSESIÓN ===
    ttk.Label(color_frame, text="POSESIÓN", font=('Arial', 10, 'bold')).grid(
        row=row, column=0, columnspan=4, sticky="w", pady=(15, 5)
    )
    row += 1
    
    create_color_picker(control_panel, color_frame, row, 0,
                       "Flecha de Posesión:", "accent_neon",
                       "Color de la flecha de posesión")
    row += 1
    
    # Botones de acción
    button_frame = ttk.Frame(color_frame)
    button_frame.grid(row=row, column=0, columnspan=4, pady=(15, 5))
    
    # Botón para restaurar colores por defecto
    reset_button = ttk.Button(
        button_frame,
        text="🔄 Restaurar Colores por Defecto",
        command=lambda: reset_colors_to_default(control_panel)
    )
    reset_button.pack(side=tk.LEFT, padx=5)
    
    # Botón para aplicar cambios
    apply_button = ttk.Button(
        button_frame,
        text="✓ Aplicar Cambios",
        command=lambda: apply_color_changes(control_panel)
    )
    apply_button.pack(side=tk.LEFT, padx=5)
    
    # Configurar grid weights
    color_frame.grid_columnconfigure(0, weight=1)
    color_frame.grid_columnconfigure(1, weight=0)
    color_frame.grid_columnconfigure(2, weight=1)
    color_frame.grid_columnconfigure(3, weight=0)


def create_color_picker(control_panel, parent, row, col, label_text, color_key, tooltip):
    """
    Crea un selector de color individual.
    
    Args:
        control_panel: Instancia de Gui_control_panel
        parent: Frame padre
        row: Fila en el grid
        col: Columna en el grid
        label_text: Texto del label
        color_key: Clave del color en el diccionario COLORS
        tooltip: Texto de ayuda
    """
    # Label
    label = ttk.Label(parent, text=label_text, font=('Arial', 9))
    label.grid(row=row, column=col, sticky="w", padx=(5, 5), pady=3)
    
    # Frame para el botón de color
    color_button_frame = tk.Frame(parent, width=80, height=25, relief=tk.RAISED, borderwidth=2)
    color_button_frame.grid(row=row, column=col+1, padx=(0, 15), pady=3)
    color_button_frame.grid_propagate(False)
    
    # Obtener color actual del scoreboard
    current_color = get_current_color(control_panel, color_key)
    color_button_frame.configure(bg=current_color)
    
    # Guardar referencia al frame del botón
    if not hasattr(control_panel, 'color_buttons'):
        control_panel.color_buttons = {}
    control_panel.color_buttons[color_key] = color_button_frame
    
    # Bind para abrir selector de color
    color_button_frame.bind('<Button-1>', 
                           lambda e: open_color_picker(control_panel, color_key, color_button_frame))
    
    # Cursor de mano al pasar sobre el botón
    color_button_frame.bind('<Enter>', lambda e: color_button_frame.configure(cursor='hand2'))
    color_button_frame.bind('<Leave>', lambda e: color_button_frame.configure(cursor=''))


def get_current_color(control_panel, color_key):
    """
    Obtiene el color actual del scoreboard.
    
    Args:
        control_panel: Instancia de Gui_control_panel
        color_key: Clave del color
        
    Returns:
        String con el color en formato hexadecimal
    """
    # Verificar si el scoreboard tiene diseño moderno
    scoreboard = control_panel.scoreboard_window
    
    if hasattr(scoreboard, 'modern_style') and scoreboard.modern_style:
        return scoreboard.modern_style.COLORS.get(color_key, '#ffffff')
    
    # Colores por defecto si no hay diseño moderno
    default_colors = {
        'bg_primary': '#0A0E27',
        'bg_center': '#0d1117',
        'bg_team_home': '#1a0f0f',
        'bg_team_away': '#0f1a1a',
        'text_primary': '#ffffff',
        'display_score': '#ffffff',
        'display_time': '#00d9ff',
        'accent_orange': '#ff6b35',
        'accent_neon': '#00ff41',
        'text_dim': '#6b7a8f',
    }
    
    return default_colors.get(color_key, '#ffffff')


def open_color_picker(control_panel, color_key, color_button_frame):
    """
    Abre el selector de color y actualiza el color seleccionado.
    
    Args:
        control_panel: Instancia de Gui_control_panel
        color_key: Clave del color a cambiar
        color_button_frame: Frame del botón de color
    """
    # Obtener color actual
    current_color = color_button_frame.cget('bg')
    
    # Abrir selector de color
    color = colorchooser.askcolor(
        color=current_color,
        title=f"Seleccionar color para {color_key}"
    )
    
    if color[1]:  # Si se seleccionó un color
        new_color = color[1]
        
        # Actualizar el botón de color
        color_button_frame.configure(bg=new_color)
        
        # Actualizar el color en el scoreboard inmediatamente
        update_scoreboard_color(control_panel, color_key, new_color)


def update_scoreboard_color(control_panel, color_key, new_color):
    """
    Actualiza un color específico en el scoreboard en tiempo real.
    Funciona tanto con ttk.Label como con tk.Label.

    Args:
        control_panel: Instancia de Gui_control_panel
        color_key: Clave del color a actualizar
        new_color: Nuevo color en formato hexadecimal
    """
    scoreboard = control_panel.scoreboard_window

    # Verificar si tiene diseño moderno
    if hasattr(scoreboard, 'modern_style') and scoreboard.modern_style:
        # Actualizar el color en el diccionario
        scoreboard.modern_style.COLORS[color_key] = new_color

        # Reaplicar los estilos ttk
        scoreboard.modern_style._apply_ttk_styles()

        # Actualizar widgets tk.Label directamente (como el reloj)
        update_tk_widgets_colors(scoreboard, color_key, new_color)


def update_tk_widgets_colors(scoreboard, color_key, new_color):
    """
    Actualiza los colores de widgets tk.Label directamente.
    Esto es necesario porque tk.Label no usa ttk.Style.

    Args:
        scoreboard: Instancia de Gui_scoreboard
        color_key: Clave del color a actualizar
        new_color: Nuevo color en formato hexadecimal
    """
    # Mapeo de claves de color a widgets específicos y tipo de actualización
    # Formato: 'color_key': [(widget_path, 'fg'|'bg'), ...]
    color_widget_map = {
        'display_time': [('match.labels.time', 'fg')],  # Color de texto del reloj
        'bg_center': [('match.labels.time', 'bg')],  # Fondo del reloj
        'text_primary': [('labels.home_team.name', 'fg'), ('labels.away_team.name', 'fg')],  # Nombres
        'display_score': [('labels.home_team.points', 'fg'), ('labels.away_team.points', 'fg')],  # Puntajes
        'bg_team_home': [('frames.home_team', 'bg')],  # Fondo equipo local
        'bg_team_away': [('frames.away_team', 'bg')],  # Fondo equipo visitante
        'bg_primary': [('root', 'bg')],  # Fondo principal
    }

    # Obtener lista de widgets a actualizar
    widget_configs = color_widget_map.get(color_key, [])

    for widget_path, config_type in widget_configs:
        try:
            # Navegar por el path para obtener el widget
            widget = scoreboard
            for attr in widget_path.split('.'):
                widget = getattr(widget, attr)

            # Actualizar el color según el tipo de configuración
            if config_type == 'fg':
                # Actualizar color de texto (foreground)
                if hasattr(widget, 'configure') and hasattr(widget, 'cget'):
                    # Verificar que el widget soporte 'fg'
                    try:
                        widget.cget('fg')  # Test si tiene fg
                        widget.configure(fg=new_color)
                    except:
                        pass
            elif config_type == 'bg':
                # Actualizar color de fondo (background)
                if hasattr(widget, 'configure'):
                    widget.configure(bg=new_color)

        except (AttributeError, tk.TclError):
            # El widget no existe, no tiene el atributo, o no soporta la opción
            pass


def apply_color_changes(control_panel):
    """
    Aplica todos los cambios de color al scoreboard.

    Args:
        control_panel: Instancia de Gui_control_panel
    """
    # Los cambios ya se aplican en tiempo real, este botón es opcional
    # Podría usarse para guardar la configuración en un archivo
    messagebox.showinfo(
        "Colores Aplicados",
        "Los colores se han aplicado correctamente al tablero."
    )


def reset_colors_to_default(control_panel):
    """
    Restaura todos los colores a los valores por defecto.
    
    Args:
        control_panel: Instancia de Gui_control_panel
    """
    scoreboard = control_panel.scoreboard_window
    
    if hasattr(scoreboard, 'modern_style') and scoreboard.modern_style:
        # Colores por defecto
        default_colors = {
            'bg_primary': '#0A0E27',
            'bg_secondary': '#1a1f3a',
            'bg_center': '#0d1117',
            'bg_team_home': '#1a0f0f',
            'bg_team_away': '#0f1a1a',
            'accent_neon': '#00ff41',
            'accent_cyan': '#00d9ff',
            'accent_red': '#ff0844',
            'accent_orange': '#ff6b35',
            'accent_yellow': '#ffd700',
            'text_primary': '#ffffff',
            'text_secondary': '#b8c5d6',
            'text_dim': '#6b7a8f',
            'display_time': '#00d9ff',
            'display_score': '#ffffff',
            'display_glow': '#0088cc',
            'border_light': '#2d3748',
            'border_bright': '#4a5568',
            'shadow': '#000000',
        }
        
        # Actualizar todos los colores
        for key, value in default_colors.items():
            scoreboard.modern_style.COLORS[key] = value

            # Actualizar botones de color si existen
            if hasattr(control_panel, 'color_buttons') and key in control_panel.color_buttons:
                control_panel.color_buttons[key].configure(bg=value)

            # Actualizar widgets tk.Label directamente
            update_tk_widgets_colors(scoreboard, key, value)

        # Reaplicar estilos ttk
        scoreboard.modern_style._apply_ttk_styles()

        messagebox.showinfo(
            "Colores Restaurados",
            "Los colores han sido restaurados a los valores por defecto."
        )

