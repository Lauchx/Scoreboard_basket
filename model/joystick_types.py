"""
Enums y tipos de datos para controladores de joystick.
Este módulo contiene las definiciones de tipos de controladores y botones abstractos.
"""

from enum import Enum

class ControllerType(Enum):
    """Tipos de controladores soportados"""
    XBOX = "xbox"
    PLAYSTATION = "playstation"
    UNKNOWN = "unknown"

class AbstractButton(Enum):
    """Botones abstractos independientes del tipo de controlador"""
    # Bumpers/Triggers superiores
    LEFT_BUMPER = "left_bumper"      # LB (Xbox) / L1 (PlayStation)
    RIGHT_BUMPER = "right_bumper"    # RB (Xbox) / R1 (PlayStation)

    # Botones de acción principales
    ACTION_BOTTOM = "action_bottom"  # A (Xbox) / X (PlayStation)
    ACTION_RIGHT = "action_right"    # B (Xbox) / O (PlayStation)
    ACTION_LEFT = "action_left"      # X (Xbox) / □ (PlayStation)
    ACTION_TOP = "action_top"        # Y (Xbox) / △ (PlayStation)

    # Botones de sistema
    START = "start"                  # Start/Options
    SELECT = "select"                # Back/Share

    # D-Pad
    DPAD_UP = "dpad_up"
    DPAD_DOWN = "dpad_down"
    DPAD_LEFT = "dpad_left"
    DPAD_RIGHT = "dpad_right"