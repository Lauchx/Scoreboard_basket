"""
Componente UI moderno para los timeouts (tiempos muertos) en el scoreboard.
Muestra 3 círculos debajo del puntaje de cada equipo que cambian de color según disponibilidad.
"""

import tkinter as tk
from tkinter import ttk


def create_timeout_indicators_modern(team_frame, team_labels, modern_style):
    """
    Crea los indicadores visuales de timeouts (3 círculos) con estilo moderno.
    
    Args:
        team_frame: Frame del equipo donde se colocarán los indicadores
        team_labels: SimpleNamespace con los labels del equipo
        modern_style: Instancia de ScoreboardModernStyle con colores y tamaños
    """
    # Crear un frame contenedor para los 3 círculos de timeout
    timeout_frame = ttk.Frame(team_frame, style="Info.TFrame")
    timeout_frame.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")
    
    # Configurar el grid del frame de timeouts para centrar los círculos
    timeout_frame.grid_columnconfigure(0, weight=1)  # Espacio izquierdo
    timeout_frame.grid_columnconfigure(1, weight=0)  # Círculo 1
    timeout_frame.grid_columnconfigure(2, weight=0)  # Círculo 2
    timeout_frame.grid_columnconfigure(3, weight=0)  # Círculo 3
    timeout_frame.grid_columnconfigure(4, weight=1)  # Espacio derecho
    
    # Crear lista para almacenar los canvas de los círculos
    team_labels.timeout_circles = []
    
    # Obtener colores del modern_style
    bg_color = modern_style.COLORS['bg_team_info']
    available_color = modern_style.COLORS.get('timeout_available', '#FF0000')  # Rojo
    used_color = modern_style.COLORS.get('timeout_used', '#404040')  # Gris oscuro
    
    # Tamaño de los círculos
    circle_size = 20  # Diámetro del círculo en píxeles
    circle_spacing = 8  # Espacio entre círculos
    
    # Crear 3 círculos (timeouts)
    for i in range(3):
        # Crear un canvas para dibujar el círculo
        canvas = tk.Canvas(
            timeout_frame,
            width=circle_size,
            height=circle_size,
            bg=bg_color,
            highlightthickness=0,
            bd=0
        )
        canvas.grid(row=0, column=i+1, padx=circle_spacing, pady=5)
        
        # Dibujar el círculo (inicialmente disponible = rojo)
        circle_id = canvas.create_oval(
            2, 2,  # x1, y1
            circle_size-2, circle_size-2,  # x2, y2
            fill=available_color,
            outline='#FFFFFF',  # Borde blanco
            width=2
        )
        
        # Guardar referencia al canvas y al círculo
        team_labels.timeout_circles.append({
            'canvas': canvas,
            'circle_id': circle_id,
            'available_color': available_color,
            'used_color': used_color
        })
    
    print(f"✅ Indicadores de timeout creados (3 círculos)")


def update_timeout_indicators_modern(team_labels, timeout_states):
    """
    Actualiza el color de los círculos de timeout según su estado.
    
    Args:
        team_labels: SimpleNamespace con los labels del equipo (debe tener timeout_circles)
        timeout_states: Lista de 3 booleanos (True = usado, False = disponible)
    """
    if not hasattr(team_labels, 'timeout_circles'):
        return
    
    for i, state_used in enumerate(timeout_states):
        if i >= len(team_labels.timeout_circles):
            break
        
        circle_info = team_labels.timeout_circles[i]
        canvas = circle_info['canvas']
        circle_id = circle_info['circle_id']
        
        # Elegir color según estado
        if state_used:
            # Timeout usado: gris oscuro
            color = circle_info['used_color']
        else:
            # Timeout disponible: rojo
            color = circle_info['available_color']
        
        # Actualizar el color del círculo
        canvas.itemconfig(circle_id, fill=color)


def setup_timeout_ui_modern(scoreboard_instance):
    """
    Configura la UI de timeouts para ambos equipos en el scoreboard moderno.
    
    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    # Crear indicadores para equipo local
    home_frame = scoreboard_instance.frames.home_team
    create_timeout_indicators_modern(
        home_frame,
        scoreboard_instance.labels.home_team,
        scoreboard_instance.modern_style
    )
    
    # Crear indicadores para equipo visitante
    away_frame = scoreboard_instance.frames.away_team
    create_timeout_indicators_modern(
        away_frame,
        scoreboard_instance.labels.away_team,
        scoreboard_instance.modern_style
    )
    
    # Actualizar con el estado inicial
    update_timeout_display(scoreboard_instance)


def update_timeout_display(scoreboard_instance):
    """
    Actualiza la visualización de timeouts para ambos equipos.
    
    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    # Actualizar equipo local
    home_states = scoreboard_instance.match_state.home_team.timeout_manager.get_timeout_states()
    update_timeout_indicators_modern(scoreboard_instance.labels.home_team, home_states)
    
    # Actualizar equipo visitante
    away_states = scoreboard_instance.match_state.away_team.timeout_manager.get_timeout_states()
    update_timeout_indicators_modern(scoreboard_instance.labels.away_team, away_states)

