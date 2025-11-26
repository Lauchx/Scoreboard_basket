"""
Componente UI para controlar los timeouts (tiempos muertos) en el panel de control.
Permite al operador marcar timeouts como usados/disponibles y reiniciarlos.
"""

from tkinter import ttk
import tkinter as tk


def setup_timeout_controls(parent_instance, team_simple_namespace, team_controller, parent_frame):
    """
    Crea los controles de timeouts para un equipo.
    
    Args:
        parent_instance: Instancia de Gui_control_panel
        team_simple_namespace: SimpleNamespace del equipo
        team_controller: Controlador del equipo
        parent_frame: Frame padre donde colocar los controles
    """
    # Determinar columna basado en el equipo (0 para local, 2 para visitante)
    column = 0 if team_controller == parent_instance.home_team_controller else 2
    
    # Crear un LabelFrame para los controles de timeout
    timeout_frame = ttk.LabelFrame(
        parent_frame,
        text=f"Tiempos Muertos",
        padding=(5, 5)
    )
    # Colocar en la fila 3 (debajo de faltas)
    timeout_frame.grid(row=3, column=column, padx=5, pady=5, sticky="ew")
    
    # Configurar grid del frame
    timeout_frame.grid_columnconfigure(0, weight=1)
    timeout_frame.grid_columnconfigure(1, weight=1)
    timeout_frame.grid_columnconfigure(2, weight=1)
    timeout_frame.grid_columnconfigure(3, weight=1)
    
    # Etiqueta informativa
    info_label = ttk.Label(
        timeout_frame,
        text="Marcar timeouts usados:",
        font=("Arial", 9, "bold")
    )
    info_label.grid(row=0, column=0, columnspan=4, pady=(0, 5), sticky="w")
    
    # Crear 3 checkbuttons para los 3 timeouts
    team_simple_namespace.timeout_vars = []
    team_simple_namespace.timeout_checkbuttons = []
    
    for i in range(3):
        # Variable para el checkbutton (True = usado, False = disponible)
        var = tk.BooleanVar(value=False)
        team_simple_namespace.timeout_vars.append(var)
        
        # Crear checkbutton
        checkbutton = ttk.Checkbutton(
            timeout_frame,
            text=f"TO {i+1}",
            variable=var,
            command=lambda idx=i, tc=team_controller, pi=parent_instance: toggle_timeout(idx, tc, pi)
        )
        checkbutton.grid(row=1, column=i, padx=5, pady=5, sticky="w")
        team_simple_namespace.timeout_checkbuttons.append(checkbutton)
    
    # Botón para reiniciar todos los timeouts
    reset_button = ttk.Button(
        timeout_frame,
        text="Reiniciar Todos",
        command=lambda tc=team_controller, pi=parent_instance, tsn=team_simple_namespace: reset_all_timeouts(tc, pi, tsn)
    )
    reset_button.grid(row=1, column=3, padx=5, pady=5, sticky="e")
    
    # Etiqueta de información de periodo
    period_info = ttk.Label(
        timeout_frame,
        text=get_timeout_period_info(team_controller),
        font=("Arial", 8),
        foreground="gray"
    )
    period_info.grid(row=2, column=0, columnspan=4, pady=(5, 0), sticky="w")
    team_simple_namespace.timeout_period_info = period_info
    
    print(f"[OK] Controles de timeout creados para {team_controller.team.name}")


def toggle_timeout(timeout_index, team_controller, parent_instance):
    """
    Alterna el estado de un timeout (usado <-> disponible).
    
    Args:
        timeout_index: Índice del timeout (0, 1, o 2)
        team_controller: Controlador del equipo
        parent_instance: Instancia de Gui_control_panel
    """
    # Alternar el estado en el modelo
    success = team_controller.toggle_timeout(timeout_index)
    
    if success:
        # Actualizar el scoreboard
        parent_instance.scoreboard_window.update_timeout_labels()
        
        # Actualizar la información del periodo
        update_timeout_period_info(parent_instance, team_controller)
        
        # Obtener el estado actual
        is_used = team_controller.team.timeout_manager.is_timeout_used(timeout_index)
        status = "usado" if is_used else "disponible"
        print(f"✅ Timeout {timeout_index + 1} de {team_controller.team.name} marcado como {status}")
    else:
        print(f"⚠️ No se pudo cambiar el estado del timeout {timeout_index + 1}")


def reset_all_timeouts(team_controller, parent_instance, team_simple_namespace):
    """
    Reinicia todos los timeouts de un equipo.
    
    Args:
        team_controller: Controlador del equipo
        parent_instance: Instancia de Gui_control_panel
        team_simple_namespace: SimpleNamespace del equipo
    """
    # Reiniciar en el modelo
    team_controller.reset_timeouts()
    
    # Actualizar los checkbuttons
    for var in team_simple_namespace.timeout_vars:
        var.set(False)
    
    # Actualizar el scoreboard
    parent_instance.scoreboard_window.update_timeout_labels()
    
    # Actualizar la información del periodo
    update_timeout_period_info(parent_instance, team_controller)
    
    print(f"✅ Todos los timeouts de {team_controller.team.name} reiniciados")


def get_timeout_period_info(team_controller):
    """
    Obtiene el texto informativo sobre los timeouts del periodo actual.
    
    Args:
        team_controller: Controlador del equipo
        
    Returns:
        str: Texto informativo
    """
    info = team_controller.get_timeout_display_info()
    quarter = team_controller.team.timeout_manager.current_quarter
    
    if quarter <= 2:
        period_name = f"1ª mitad (Q{quarter})"
    elif quarter <= 4:
        period_name = f"2ª mitad (Q{quarter})"
    else:
        period_name = f"Overtime {quarter - 4}"
    
    return f"{period_name}: {info['available']}/{info['max_allowed']} disponibles"


def update_timeout_period_info(parent_instance, team_controller):
    """
    Actualiza la etiqueta de información del periodo.
    
    Args:
        parent_instance: Instancia de Gui_control_panel
        team_controller: Controlador del equipo
    """
    # Determinar qué namespace usar
    if team_controller.team.name == parent_instance.match_state_controller.home_team_controller.team.name:
        team_namespace = parent_instance.home_team
    else:
        team_namespace = parent_instance.away_team
    
    # Actualizar el label si existe
    if hasattr(team_namespace, 'timeout_period_info'):
        new_text = get_timeout_period_info(team_controller)
        team_namespace.timeout_period_info.config(text=new_text)


def update_timeout_controls_for_quarter(parent_instance, new_quarter):
    """
    Actualiza los controles de timeout cuando cambia el cuarto.
    Actualiza el gestor de timeouts y la información mostrada.
    
    Args:
        parent_instance: Instancia de Gui_control_panel
        new_quarter: Número del nuevo cuarto
    """
    # Actualizar ambos equipos
    for team_controller in [parent_instance.home_team_controller, parent_instance.away_team_controller]:
        # Actualizar el cuarto en el timeout manager
        team_controller.update_timeout_quarter(new_quarter)
        
        # Actualizar la información del periodo
        update_timeout_period_info(parent_instance, team_controller)
    
    # Actualizar el scoreboard
    parent_instance.scoreboard_window.update_timeout_labels()
    
    print(f"✅ Controles de timeout actualizados para cuarto {new_quarter}")


def sync_timeout_checkbuttons(parent_instance):
    """
    Sincroniza los checkbuttons con el estado actual de los timeouts.
    Útil después de reiniciar o cambiar de cuarto.
    
    Args:
        parent_instance: Instancia de Gui_control_panel
    """
    # Sincronizar equipo local
    if hasattr(parent_instance.home_team, 'timeout_vars'):
        home_states = parent_instance.home_team_controller.get_timeout_states()
        for i, is_used in enumerate(home_states):
            if i < len(parent_instance.home_team.timeout_vars):
                parent_instance.home_team.timeout_vars[i].set(is_used)
    
    # Sincronizar equipo visitante
    if hasattr(parent_instance.away_team, 'timeout_vars'):
        away_states = parent_instance.away_team_controller.get_timeout_states()
        for i, is_used in enumerate(away_states):
            if i < len(parent_instance.away_team.timeout_vars):
                parent_instance.away_team.timeout_vars[i].set(is_used)

