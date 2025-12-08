"""
Módulo de integración para aplicar el diseño moderno al scoreboard.

Este módulo permite activar/desactivar fácilmente el diseño moderno profesional
sin modificar el código original del scoreboard.

Uso:
    En gui_scoreboard.py, importar y usar:
    
    from gui.scoreboard.apply_modern_design import apply_modern_design
    
    # En __init__ de Gui_scoreboard, reemplazar:
    # apply_styles()
    # por:
    # apply_modern_design(self)
"""

from gui.scoreboard.modern_style import ScoreboardModernStyle
from gui.scoreboard.ui_components.ui_teams_modern import (
    create_names_labels_modern,
    create_logos_labels_modern, 
    create_points_labels_modern,
    teams_labels_grid_configure
)
from gui.scoreboard.ui_components.ui_time_modern import create_time_labels_modern
from gui.scoreboard.ui_components.ui_match_modern import (
    create_quarter_labels_modern,
    create_possession_labels_modern,
    setup_ui_match_modern
)
from gui.scoreboard.ui_components.ui_players_modern import create_players_labels_modern
from gui.scoreboard.ui_components.ui_timeouts_modern import create_timeout_indicators_modern


def apply_modern_design(scoreboard_instance):
    """
    Aplica el diseño moderno completo al scoreboard.

    Esta función reemplaza las funciones de creación de UI originales
    por sus versiones modernas, sin alterar la lógica del scoreboard.

    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    # Crear e inicializar el sistema de estilos modernos
    modern_style = ScoreboardModernStyle(scoreboard_instance.root)

    # Guardar referencia al estilo para uso posterior
    scoreboard_instance.modern_style = modern_style

    # Conectar el scoreboard con el sistema de estilos para actualizaciones dinámicas
    modern_style.set_scoreboard_instance(scoreboard_instance)

    # Configurar fondo de la ventana principal
    scoreboard_instance.root.configure(bg=modern_style.COLORS['bg_primary'])

    return modern_style


def setup_ui_modern(scoreboard_instance):
    """
    Configura el UI con diseño moderno (reemplaza setup_ui original).
    COMPLETAMENTE RESPONSIVE - todos los elementos se escalan con la ventana.

    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    # Configurar grid de la ventana principal (responsive)
    # Columnas de equipos (0 y 2) tienen peso para jugadores
    # Columna central (1) tiene peso menor pero flexible
    scoreboard_instance.root.grid_columnconfigure(0, weight=3)  # Equipo local
    scoreboard_instance.root.grid_columnconfigure(1, weight=2)  # Centro - FLEXIBLE (sin minsize fijo)
    scoreboard_instance.root.grid_columnconfigure(2, weight=3)  # Equipo visitante

    scoreboard_instance.root.grid_rowconfigure(0, weight=1)
    scoreboard_instance.root.grid_rowconfigure(1, weight=0)

    # Crear componentes del panel central con estilo moderno
    setup_ui_match_modern(scoreboard_instance)
    create_time_labels_modern(scoreboard_instance)
    create_quarter_labels_modern(scoreboard_instance, scoreboard_instance.modern_style)

    # Importar y crear grilla de faltas y BONUS
    from gui.scoreboard.ui_components.ui_fouls_modern import create_fouls_grid_modern
    create_fouls_grid_modern(scoreboard_instance, scoreboard_instance.modern_style)

    # Crear posesión (ahora va después de las faltas, solo flecha)
    create_possession_labels_modern(scoreboard_instance)


def creates_home_team_modern(scoreboard_instance):
    """
    Crea el panel del equipo local con diseño moderno.

    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    from tkinter import ttk

    # Crear frame con estilo moderno (padding reducido para dar más espacio a jugadores)
    scoreboard_instance.home_team.frames = ttk.Frame(
        scoreboard_instance.root,
        style="HomeTeam.TFrame",
        padding=(10, 10)  # Reducido de (20, 15) a (10, 10)
    )
    scoreboard_instance.home_team.frames.grid(
        row=0, column=0, sticky="nsew", padx=(10, 5), pady=10  # Reducido padding
    )
    
    # Configurar grid para equipo local
    teams_labels_grid_configure(scoreboard_instance.home_team.frames, is_home_team=True)
    
    # Crear componentes UI con estilo moderno
    create_names_labels_modern(
        scoreboard_instance.home_team.frames,
        scoreboard_instance.labels.home_team,
        scoreboard_instance.match_state.home_team.name
    )
    create_logos_labels_modern(
        scoreboard_instance.home_team.frames,
        scoreboard_instance.labels.home_team
    )
    create_points_labels_modern(
        scoreboard_instance.home_team.frames,
        scoreboard_instance.labels.home_team,
        scoreboard_instance.match_state.home_team.points,
        scoreboard_instance.modern_style
    )
    
    # Crear lista de jugadores con estilo moderno
    create_players_labels_modern(
        scoreboard_instance.home_team,
        True,  # is_home_team
        scoreboard_instance.modern_style
    )

    # Crear indicadores de timeouts (3 círculos debajo del puntaje)
    create_timeout_indicators_modern(
        scoreboard_instance.home_team.frames,
        scoreboard_instance.labels.home_team,
        scoreboard_instance.modern_style
    )


def creates_away_team_modern(scoreboard_instance):
    """
    Crea el panel del equipo visitante con diseño moderno.

    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
    """
    from tkinter import ttk

    # Crear frame con estilo moderno (padding reducido para dar más espacio a jugadores)
    scoreboard_instance.away_team.frames = ttk.Frame(
        scoreboard_instance.root,
        style="AwayTeam.TFrame",
        padding=(10, 10)  # Reducido de (20, 15) a (10, 10)
    )
    scoreboard_instance.away_team.frames.grid(
        row=0, column=2, sticky="nsew", padx=(5, 10), pady=10  # Reducido padding
    )
    
    # Configurar grid para equipo visitante
    teams_labels_grid_configure(scoreboard_instance.away_team.frames, is_home_team=False)
    
    # Crear componentes UI con estilo moderno
    create_names_labels_modern(
        scoreboard_instance.away_team.frames,
        scoreboard_instance.labels.away_team,
        scoreboard_instance.match_state.away_team.name
    )
    create_logos_labels_modern(
        scoreboard_instance.away_team.frames,
        scoreboard_instance.labels.away_team
    )
    create_points_labels_modern(
        scoreboard_instance.away_team.frames,
        scoreboard_instance.labels.away_team,
        scoreboard_instance.match_state.away_team.points,
        scoreboard_instance.modern_style
    )
    
    # Crear lista de jugadores con estilo moderno
    create_players_labels_modern(
        scoreboard_instance.away_team,
        False,  # is_home_team
        scoreboard_instance.modern_style
    )

    # Crear indicadores de timeouts (3 círculos debajo del puntaje)
    create_timeout_indicators_modern(
        scoreboard_instance.away_team.frames,
        scoreboard_instance.labels.away_team,
        scoreboard_instance.modern_style
    )


def get_foul_circles(foul_count):
    """
    Genera la representación visual de faltas con 5 círculos pequeños.

    Args:
        foul_count: Número de faltas del jugador (0-5)

    Returns:
        str: 5 círculos pequeños, encendidos (●) o apagados (○)
    """
    # Limitar a 5 faltas máximo
    fouls = min(foul_count, 5)
    # Círculos pequeños Unicode (más compactos que emojis)
    on = "●"   # Círculo negro relleno (U+25CF)
    off = "○"  # Círculo blanco vacío (U+25CB)
    return (on * fouls) + (off * (5 - fouls))


def update_label_players_modern(scoreboard_instance, player, team_controller):
    """
    Actualiza la lista COMPLETA de jugadores con colores modernos para activos/inactivos/suspendidos.
    NO inserta nuevos jugadores, sino que refresca toda la lista.

    Formato de visualización:
    - num - nombre    ⚪⚪⚪⚪⚪  (círculos de faltas)

    Colores:
    - Verde: Jugador activo en cancha
    - Blanco: Jugador inactivo (en banca)
    - Rojo: Jugador suspendido (5 faltas o falta antideportiva)

    Args:
        scoreboard_instance: Instancia de Gui_scoreboard
        player: Objeto Player (no usado, se mantiene por compatibilidad)
        team_controller: Controlador del equipo
    """
    import tkinter as tk
    from gui.scoreboard.gui_scoreboard import _nameSpace_team_for_controller

    team_simple_name_space = _nameSpace_team_for_controller(
        scoreboard_instance,
        team_controller.team.name
    )

    # Limpiar la lista actual
    team_simple_name_space.labels.players.delete(0, tk.END)

    # Reconstruir la lista completa con todos los jugadores
    for player_obj in team_controller.team.players:
        # Generar círculos de faltas (5 indicadores)
        foul_circles = get_foul_circles(player_obj.foul)

        # Formato: num - nombre    ⚪⚪⚪⚪⚪
        player_text = f"{player_obj.jersey_number} - {player_obj.name}  {foul_circles}"
        team_simple_name_space.labels.players.insert(tk.END, player_text)

        index = team_simple_name_space.labels.players.size() - 1

        # Determinar color según estado del jugador
        if player_obj.is_suspended:
            # ROJO: Jugador suspendido (5 faltas o falta antideportiva)
            color = '#FF0000'
        elif player_obj.is_active:
            # VERDE: Jugador activo en cancha
            color = scoreboard_instance.modern_style.get_active_player_color()
        else:
            # BLANCO: Jugador inactivo (en banca)
            color = scoreboard_instance.modern_style.get_inactive_player_color()

        team_simple_name_space.labels.players.itemconfig(index, {'fg': color})

