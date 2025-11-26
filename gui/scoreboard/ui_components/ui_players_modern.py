"""
Componente UI moderno para la lista de jugadores en el scoreboard.
Diseño profesional con colores diferenciados para jugadores activos/inactivos.
"""

import tkinter as tk


def create_players_labels_modern(team_simple_name_space, is_home_team, modern_style):
    """
    Crea el Listbox de jugadores con estilo moderno y responsivo.
    El tamaño del texto se ajusta según el tamaño del Listbox.
    
    Args:
        team_simple_name_space: Namespace del equipo
        is_home_team: True si es equipo local, False si es visitante
        modern_style: Instancia de ScoreboardModernStyle para obtener configuración
    """
    # Obtener configuración de estilo
    listbox_config = modern_style.get_player_listbox_config()
    
    # Crear Listbox con configuración moderna
    team_simple_name_space.labels.players = tk.Listbox(
        team_simple_name_space.frames,
        **listbox_config
    )
    
    # Posicionamiento según equipo
    col = 0 if is_home_team else 2
    padding = (0, 15) if is_home_team else (15, 0)
    
    team_simple_name_space.labels.players.grid(
        row=0, 
        column=col, 
        rowspan=3, 
        sticky="nsew", 
        padx=padding, 
        pady=5
    )
    
    # Vincular evento de redimensionamiento para ajustar tamaño de fuente dinámicamente
    def adjust_font_size(event):
        """Ajusta el tamaño de la fuente según el tamaño disponible del Listbox"""
        listbox = team_simple_name_space.labels.players
        
        # Calcular altura disponible en píxeles (restando padding interno)
        available_height = event.height - 4  # Restar padding interno
        available_width = event.width - 4    # Restar padding horizontal
        
        # Calcular número de elementos visibles
        num_items = listbox.size()
        if num_items == 0 or available_height <= 0 or available_width <= 0:
            return
        
        # Altura disponible por ítem
        height_per_item = available_height / max(num_items, 1)
        
        # Calcular tamaño de fuente basado en la altura disponible
        # Factor 0.35 asegura que se reduzca significativamente cuando se achica el label
        new_font_size = max(6, int(height_per_item * 0.35))
        
        # Limitar el tamaño máximo a 14 píxeles para evitar que sea demasiado grande
        new_font_size = min(new_font_size, 14)
        
        # Obtener fuente actual
        font_family = modern_style.FONTS['display'][0] if hasattr(modern_style, 'FONTS') else 'Arial'
        
        # Aplicar nueva fuente con el tamaño calculado
        try:
            listbox.config(font=(font_family, new_font_size))
        except:
            pass
    
    # Vincular el evento Configure al Listbox
    team_simple_name_space.labels.players.bind('<Configure>', adjust_font_size)

