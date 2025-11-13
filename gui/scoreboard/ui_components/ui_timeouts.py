"""
Componente UI para los timeouts (tiempos muertos) en el scoreboard original.
Muestra 3 círculos debajo del puntaje de cada equipo que cambian de color según disponibilidad.
"""

import tkinter as tk
from tkinter import ttk


def create_timeout_indicators(team_frame, team_labels):
    """
    Crea los indicadores visuales de timeouts (3 círculos) con estilo original.
    
    Args:
        team_frame: Frame del equipo donde se colocarán los indicadores
        team_labels: SimpleNamespace con los labels del equipo
    """
    # Crear un frame contenedor para los 3 círculos de timeout
    timeout_frame = ttk.Frame(team_frame, style="TFrame")
    timeout_frame.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")
    
    # Configurar el grid del frame de timeouts para centrar los círculos
    timeout_frame.grid_columnconfigure(0, weight=1)  # Espacio izquierdo
    timeout_frame.grid_columnconfigure(1, weight=0)  # Círculo 1
    timeout_frame.grid_columnconfigure(2, weight=0)  # Círculo 2
    timeout_frame.grid_columnconfigure(3, weight=0)  # Círculo 3
    timeout_frame.grid_columnconfigure(4, weight=1)  # Espacio derecho
    
    # Crear lista para almacenar los canvas de los círculos
    team_labels.timeout_circles = []
    
    # Colores para el diseño original
    bg_color = 'black'
    available_color = '#FF0000'  # Rojo
    used_color = '#808080'  # Gris
    
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
    
    print(f"✅ Indicadores de timeout creados (3 círculos) - diseño original")


def update_timeout_indicators(team_labels, timeout_states):
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
            # Timeout usado: gris
            color = circle_info['used_color']
        else:
            # Timeout disponible: rojo
            color = circle_info['available_color']
        
        # Actualizar el color del círculo
        canvas.itemconfig(circle_id, fill=color)

