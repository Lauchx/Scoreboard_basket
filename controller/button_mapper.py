"""
Button Mapper - Sistema abstracto de mapeo de botones para diferentes tipos de controladores.

Este módulo proporciona una capa de abstracción que permite manejar diferentes tipos
de mandos (Xbox, PlayStation, etc.) sin importar los números específicos de los botones.
"""

from enum import Enum
from typing import Dict, Optional

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

class ButtonMapper:
    """
    Clase principal que maneja el mapeo entre botones abstractos y números físicos
    según el tipo de controlador detectado.
    """

    def __init__(self):
        self.controller_type = ControllerType.UNKNOWN
        self.current_mapping: Dict[AbstractButton, int] = {}

        # Mapeos predefinidos para cada tipo de controlador
        self.controller_mappings = {
            ControllerType.XBOX: {
                AbstractButton.LEFT_BUMPER: 4,      # LB
                AbstractButton.RIGHT_BUMPER: 5,     # RB
                AbstractButton.ACTION_BOTTOM: 0,    # A
                AbstractButton.ACTION_RIGHT: 1,     # B
                AbstractButton.ACTION_LEFT: 2,      # X
                AbstractButton.ACTION_TOP: 3,       # Y
                AbstractButton.START: 7,            # Start
                AbstractButton.SELECT: 6,           # Back
            },
            ControllerType.PLAYSTATION: {
                AbstractButton.LEFT_BUMPER: 4,      # L1
                AbstractButton.RIGHT_BUMPER: 5,     # R1
                AbstractButton.ACTION_BOTTOM: 0,    # X
                AbstractButton.ACTION_RIGHT: 1,     # O
                AbstractButton.ACTION_LEFT: 2,      # □
                AbstractButton.ACTION_TOP: 3,       # △
                AbstractButton.START: 7,            # Options
                AbstractButton.SELECT: 6,           # Share
            }
        }

        # Nombres descriptivos para mostrar en la UI
        self.button_display_names = {
            ControllerType.XBOX: {
                AbstractButton.LEFT_BUMPER: "LB",
                AbstractButton.RIGHT_BUMPER: "RB",
                AbstractButton.ACTION_BOTTOM: "A",
                AbstractButton.ACTION_RIGHT: "B",
                AbstractButton.ACTION_LEFT: "X",
                AbstractButton.ACTION_TOP: "Y",
                AbstractButton.START: "Start",
                AbstractButton.SELECT: "Back",
            },
            ControllerType.PLAYSTATION: {
                AbstractButton.LEFT_BUMPER: "L1",
                AbstractButton.RIGHT_BUMPER: "R1",
                AbstractButton.ACTION_BOTTOM: "X",
                AbstractButton.ACTION_RIGHT: "O",
                AbstractButton.ACTION_LEFT: "□",
                AbstractButton.ACTION_TOP: "△",
                AbstractButton.START: "Options",
                AbstractButton.SELECT: "Share",
            }
        }

    def detect_controller_type(self, controller_name: str) -> ControllerType:
        """
        Detecta el tipo de controlador basado en el nombre del dispositivo.

        Args:
            controller_name (str): Nombre del controlador detectado por pygame

        Returns:
            ControllerType: Tipo de controlador detectado
        """
        controller_name_lower = controller_name.lower()

        # Patrones comunes para Xbox
        xbox_patterns = ['xbox', 'xinput', 'microsoft']
        # Patrones comunes para PlayStation
        playstation_patterns = ['playstation', 'dualshock', 'dual sense', 'sony']

        if any(pattern in controller_name_lower for pattern in xbox_patterns):
            self.controller_type = ControllerType.XBOX
        elif any(pattern in controller_name_lower for pattern in playstation_patterns):
            self.controller_type = ControllerType.PLAYSTATION
        else:
            self.controller_type = ControllerType.UNKNOWN

        self._update_current_mapping()
        return self.controller_type

    def set_controller_type(self, controller_type: ControllerType):
        """
        Establece manualmente el tipo de controlador.

        Args:
            controller_type (ControllerType): Tipo de controlador a establecer
        """
        self.controller_type = controller_type
        self._update_current_mapping()

    def _update_current_mapping(self):
        """Actualiza el mapeo actual basado en el tipo de controlador"""
        if self.controller_type in self.controller_mappings:
            self.current_mapping = self.controller_mappings[self.controller_type].copy()
        else:
            # Si no se reconoce el controlador, usar mapeo genérico (Xbox como default)
            self.current_mapping = self.controller_mappings[ControllerType.XBOX].copy()

    def get_physical_button(self, abstract_button: AbstractButton) -> Optional[int]:
        """
        Obtiene el número de botón físico correspondiente a un botón abstracto.

        Args:
            abstract_button (AbstractButton): Botón abstracto

        Returns:
            Optional[int]: Número de botón físico o None si no está mapeado
        """
        return self.current_mapping.get(abstract_button)

    def get_abstract_button(self, physical_button: int) -> Optional[AbstractButton]:
        """
        Obtiene el botón abstracto correspondiente a un número de botón físico.

        Args:
            physical_button (int): Número de botón físico

        Returns:
            Optional[AbstractButton]: Botón abstracto o None si no está mapeado
        """
        for abstract_btn, physical_btn in self.current_mapping.items():
            if physical_btn == physical_button:
                return abstract_btn
        return None

    def get_display_name(self, abstract_button: AbstractButton) -> str:
        """
        Obtiene el nombre para mostrar del botón según el tipo de controlador.

        Args:
            abstract_button (AbstractButton): Botón abstracto

        Returns:
            str: Nombre para mostrar del botón
        """
        if self.controller_type in self.button_display_names:
            return self.button_display_names[self.controller_type].get(abstract_button, str(abstract_button.value))
        return str(abstract_button.value)

    def get_available_buttons(self) -> Dict[AbstractButton, str]:
        """
        Obtiene todos los botones disponibles con sus nombres para mostrar.

        Returns:
            Dict[AbstractButton, str]: Diccionario de botones abstractos y sus nombres
        """
        if self.controller_type in self.button_display_names:
            return self.button_display_names[self.controller_type]
        # fallback a nombres genéricos
        return {btn: btn.value.replace('_', ' ').title() for btn in AbstractButton}

    def create_action_mapping(self, action_config: Dict[str, AbstractButton]) -> Dict[int, str]:
        """
        Crea un mapeo de acciones a botones físicos.

        Args:
            action_config (Dict[str, AbstractButton]): Configuración de acciones con botones abstractos

        Returns:
            Dict[int, str]: Mapeo de botones físicos a acciones
        """
        physical_mapping = {}
        for action, abstract_button in action_config.items():
            physical_button = self.get_physical_button(abstract_button)
            if physical_button is not None:
                physical_mapping[physical_button] = action
        return physical_mapping

    def get_controller_info(self) -> Dict[str, str]:
        """
        Obtiene información del controlador actual.

        Returns:
            Dict[str, str]: Información del controlador
        """
        return {
            'type': self.controller_type.value,
            'display_name': self.controller_type.value.title(),
            'mapped_buttons': len(self.current_mapping)
        }

# Configuración por defecto de acciones del marcador
DEFAULT_SCOREBOARD_ACTIONS = {
    'home_add_point': AbstractButton.LEFT_BUMPER,
    'away_add_point': AbstractButton.RIGHT_BUMPER,
    'home_subtract_point': AbstractButton.ACTION_LEFT,
    'away_subtract_point': AbstractButton.ACTION_TOP,
    'manage_timer': AbstractButton.ACTION_BOTTOM,
    'pause_timer': AbstractButton.SELECT,
    'resume_timer': AbstractButton.START,
}

def create_button_mapper(controller_name: str = None, controller_type: ControllerType = ControllerType.XBOX) -> ButtonMapper:
    """
    Función de utilidad para crear un ButtonMapper con detección automática o manual.

    Args:
        controller_name (str, optional): Nombre del controlador para detección automática
        controller_type (ControllerType): Tipo de controlador manual (usado si no se puede detectar)

    Returns:
        ButtonMapper: Instancia configurada del ButtonMapper
    """
    mapper = ButtonMapper()

    if controller_name:
        mapper.detect_controller_type(controller_name)
    else:
        mapper.set_controller_type(controller_type)

    return mapper