"""
Modelo de datos para el mapeo de botones de joystick.
Este módulo contiene la lógica de datos para mapear botones abstractos a botones físicos.
"""

from typing import Dict, Optional
from .joystick_types import ControllerType, AbstractButton

class ButtonMapping:
    """
    Modelo de datos puro para el mapeo entre botones abstractos y números físicos.

    Este modelo solo contiene datos y getters (consultas puras).
    Toda la lógica de modificación está en el controller.
    """

    def __init__(self):
        self.controller_type = ControllerType.UNKNOWN
        self.current_mapping: Dict[AbstractButton, int] = {}

        # Datos estáticos: mapeos predefinidos para cada tipo de controlador
        self.CONTROLLER_MAPPINGS = {
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
                AbstractButton.LEFT_BUMPER: 10,     # L1
                AbstractButton.RIGHT_BUMPER: 11,    # R1
                AbstractButton.ACTION_BOTTOM: 14,    # X
                AbstractButton.ACTION_RIGHT: 13,     # O
                AbstractButton.ACTION_LEFT: 15,      # □
                AbstractButton.ACTION_TOP: 12,       # △
                AbstractButton.START: 3,            # Options
                AbstractButton.SELECT: 0,           # Share
            }
        }

        # Datos estáticos: nombres descriptivos para mostrar en la UI
        self.BUTTON_DISPLAY_NAMES = {
            ControllerType.XBOX: {
                AbstractButton.LEFT_BUMPER: "LB",
                AbstractButton.RIGHT_BUMPER: "RB",
                AbstractButton.ACTION_BOTTOM: "A",
                AbstractButton.ACTION_RIGHT: "B",
                AbstractButton.ACTION_LEFT: "X",
                AbstractButton.ACTION_TOP: "Y",
                AbstractButton.START: "Start",
                AbstractButton.SELECT: "Select",
            },
            ControllerType.PLAYSTATION: {
                AbstractButton.LEFT_BUMPER: "L1",
                AbstractButton.RIGHT_BUMPER: "R1",
                AbstractButton.ACTION_BOTTOM: "X",
                AbstractButton.ACTION_RIGHT: "O",
                AbstractButton.ACTION_LEFT: "□",
                AbstractButton.ACTION_TOP: "△",
                AbstractButton.START: "Start",
                AbstractButton.SELECT: "Share",
            }
        }

# =======================================================================
# MÉTODOS GETTERS PUROS (solo consultas, no modifican estado)
# =======================================================================

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
    
    def get_abstract_button_from_display(self, display_name: str) -> Optional[AbstractButton]:
      """Obtiene el AbstractButton a partir del display name"""
      if self.controller_type in self.BUTTON_DISPLAY_NAMES:
          for abstract_btn, display in self.BUTTON_DISPLAY_NAMES[self.controller_type].items():
              if display == display_name:
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
        if self.controller_type in self.BUTTON_DISPLAY_NAMES:
            return self.BUTTON_DISPLAY_NAMES[self.controller_type].get(abstract_button, str(abstract_button.value))
        return str(abstract_button.value)

    def get_available_buttons(self) -> Dict[AbstractButton, str]:
        """
        Obtiene todos los botones disponibles con sus nombres para mostrar.

        Returns:
            Dict[AbstractButton, str]: Diccionario de botones abstractos y sus nombres
        """
        if self.controller_type in self.BUTTON_DISPLAY_NAMES:
            return self.BUTTON_DISPLAY_NAMES[self.controller_type]
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