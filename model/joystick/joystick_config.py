"""
Configuración por defecto de acciones del joystick para el marcador.
Este módulo contiene las configuraciones predefinidas de acciones.
"""

from .joystick_types import AbstractButton

# Configuración por defecto de acciones del marcador
DEFAULT_SCOREBOARD_ACTIONS = {
    'home_add_point': AbstractButton.LEFT_BUMPER,
    'away_add_point': AbstractButton.RIGHT_BUMPER,
    'home_subtract_point': AbstractButton.ACTION_LEFT,
    'away_subtract_point': AbstractButton.ACTION_TOP,
    'manage_timer': AbstractButton.START,
    'change_possession': AbstractButton.SELECT,
    'home_add_team_foul': AbstractButton.DPAD_LEFT,
    'away_add_team_foul': AbstractButton.DPAD_RIGHT,
    'home_subtract_team_foul': AbstractButton.DPAD_UP,
    'away_subtract_team_foul': AbstractButton.DPAD_DOWN,
}