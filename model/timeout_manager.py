"""
Gestor de tiempos muertos (timeouts) de básquetbol.
Implementa las reglas de timeouts por periodo.

Reglas configuradas:
- Primera mitad (cuartos 1-2): 3 timeouts disponibles
- Segunda mitad (cuartos 3-4): 3 timeouts disponibles
- Overtime (cuarto 5+): 1 timeout adicional por periodo extra
- Cada timeout dura 1 minuto
"""


class TimeoutManager:
    """
    Gestiona los timeouts de un equipo según las reglas oficiales de básquetbol.
    
    Attributes:
        max_timeouts (int): Número máximo de timeouts que se pueden mostrar (3)
        used_timeouts (list): Lista de booleanos indicando qué timeouts están usados
        current_quarter (int): Cuarto actual del partido
    """
    
    MAX_DISPLAY_TIMEOUTS = 3  # Siempre mostramos 3 círculos
    
    def __init__(self, current_quarter=1):
        """
        Inicializa el gestor de timeouts.
        
        Args:
            current_quarter (int): Cuarto inicial del partido (default: 1)
        """
        self.current_quarter = current_quarter
        # Lista de 3 booleanos: True = usado, False = disponible
        self.used_timeouts = [False, False, False]
    
    def get_available_count(self):
        """
        Retorna cuántos timeouts están disponibles (no usados).
        
        Returns:
            int: Número de timeouts disponibles
        """
        return self.used_timeouts.count(False)
    
    def get_used_count(self):
        """
        Retorna cuántos timeouts han sido usados.
        
        Returns:
            int: Número de timeouts usados
        """
        return self.used_timeouts.count(True)
    
    def get_max_allowed_for_period(self):
        """
        Retorna el número máximo de timeouts permitidos según el periodo actual.

        Returns:
            int: Número máximo de timeouts permitidos

        Reglas:
            - Cuartos 1-2 (primera mitad): 3 timeouts
            - Cuartos 3-4 (segunda mitad): 3 timeouts
            - Cuarto 5+ (overtime): 1 timeout por periodo extra
        """
        if self.current_quarter <= 2:
            # Primera mitad: 3 timeouts
            return 3
        elif self.current_quarter <= 4:
            # Segunda mitad: 3 timeouts
            return 3
        else:
            # Overtime: 1 timeout por periodo extra
            return 1
    
    def can_use_timeout(self, timeout_index):
        """
        Verifica si se puede usar un timeout específico.
        
        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)
            
        Returns:
            bool: True si se puede usar, False si no
        """
        if timeout_index < 0 or timeout_index >= self.MAX_DISPLAY_TIMEOUTS:
            return False
        
        # No se puede usar si ya está usado
        if self.used_timeouts[timeout_index]:
            return False
        
        # Verificar que no se exceda el límite del periodo
        max_allowed = self.get_max_allowed_for_period()
        used_count = self.get_used_count()
        
        return used_count < max_allowed
    
    def use_timeout(self, timeout_index):
        """
        Marca un timeout como usado.
        
        Args:
            timeout_index (int): Índice del timeout a usar (0, 1, o 2)
            
        Returns:
            bool: True si se usó exitosamente, False si no se pudo usar
        """
        if not self.can_use_timeout(timeout_index):
            return False
        
        self.used_timeouts[timeout_index] = True
        return True
    
    def restore_timeout(self, timeout_index):
        """
        Marca un timeout como disponible (restaura un timeout usado).
        Útil para correcciones del operador.
        
        Args:
            timeout_index (int): Índice del timeout a restaurar (0, 1, o 2)
            
        Returns:
            bool: True si se restauró exitosamente, False si el índice es inválido
        """
        if timeout_index < 0 or timeout_index >= self.MAX_DISPLAY_TIMEOUTS:
            return False
        
        self.used_timeouts[timeout_index] = False
        return True
    
    def toggle_timeout(self, timeout_index):
        """
        Alterna el estado de un timeout (usado <-> disponible).
        
        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)
            
        Returns:
            bool: True si se cambió el estado, False si no se pudo
        """
        if timeout_index < 0 or timeout_index >= self.MAX_DISPLAY_TIMEOUTS:
            return False
        
        if self.used_timeouts[timeout_index]:
            # Está usado, restaurarlo
            return self.restore_timeout(timeout_index)
        else:
            # Está disponible, intentar usarlo
            return self.use_timeout(timeout_index)
    
    def is_timeout_used(self, timeout_index):
        """
        Verifica si un timeout específico está usado.
        
        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)
            
        Returns:
            bool: True si está usado, False si está disponible o índice inválido
        """
        if timeout_index < 0 or timeout_index >= self.MAX_DISPLAY_TIMEOUTS:
            return False
        
        return self.used_timeouts[timeout_index]
    
    def is_timeout_available(self, timeout_index):
        """
        Verifica si un timeout específico está disponible para usar.

        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)

        Returns:
            bool: True si está disponible, False si está usado o índice inválido
        """
        if timeout_index < 0 or timeout_index >= self.MAX_DISPLAY_TIMEOUTS:
            return False

        return not self.used_timeouts[timeout_index]

    def is_timeout_allowed_in_period(self, timeout_index):
        """
        Verifica si un timeout específico está permitido en el periodo actual.
        Un timeout puede estar disponible (no usado) pero no permitido si excede
        el límite del periodo.

        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)

        Returns:
            bool: True si está permitido en este periodo, False si no
        """
        if timeout_index < 0 or timeout_index >= self.MAX_DISPLAY_TIMEOUTS:
            return False

        max_allowed = self.get_max_allowed_for_period()
        # El timeout está permitido si su índice es menor que el máximo permitido
        return timeout_index < max_allowed
    
    def reset_for_period(self, new_quarter):
        """
        Reinicia los timeouts para un nuevo periodo.
        
        Args:
            new_quarter (int): Número del nuevo cuarto
            
        Comportamiento:
            - Cuartos 1-2: Reinicia todos los timeouts al cambiar de cuarto
            - Cuartos 3-4: Reinicia todos los timeouts al cambiar de cuarto
            - Overtime: Reinicia todos los timeouts en cada periodo extra
        """
        old_quarter = self.current_quarter
        self.current_quarter = new_quarter
        
        # Reiniciar timeouts al cambiar de periodo
        # En básquetbol, los timeouts se reinician en cada mitad y en cada overtime
        if old_quarter <= 2 and new_quarter == 3:
            # Cambio de primera a segunda mitad
            self.used_timeouts = [False, False, False]
        elif new_quarter >= 5:
            # Overtime: reiniciar en cada periodo extra
            self.used_timeouts = [False, False, False]
        elif (old_quarter == 1 and new_quarter == 2) or (old_quarter == 3 and new_quarter == 4):
            # Dentro de la misma mitad, los timeouts NO se reinician
            pass
        else:
            # Cualquier otro cambio de cuarto
            self.used_timeouts = [False, False, False]
    
    def reset_all(self):
        """
        Reinicia completamente todos los timeouts (para nuevo partido).
        """
        self.used_timeouts = [False, False, False]
        self.current_quarter = 1
    
    def get_timeout_states(self):
        """
        Retorna el estado de todos los timeouts.
        
        Returns:
            list: Lista de 3 booleanos (True = usado, False = disponible)
        """
        return self.used_timeouts.copy()
    
    def get_timeout_visual_state(self, timeout_index):
        """
        Retorna el estado visual de un timeout para la UI.

        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)

        Returns:
            str: Estado visual del timeout:
                - 'used': Timeout ya usado (rojo)
                - 'available': Timeout disponible y permitido en este periodo (verde)
                - 'not_allowed': Timeout no permitido en este periodo (gris)
        """
        if timeout_index < 0 or timeout_index >= self.MAX_DISPLAY_TIMEOUTS:
            return 'not_allowed'

        # Si está usado, mostrar como usado (rojo)
        if self.used_timeouts[timeout_index]:
            return 'used'

        # Si no está usado, verificar si está permitido en este periodo
        if self.is_timeout_allowed_in_period(timeout_index):
            return 'available'
        else:
            return 'not_allowed'

    def get_display_info(self):
        """
        Retorna información para mostrar en la UI.

        Returns:
            dict: Diccionario con información de display:
                - 'states': Lista de estados [True/False]
                - 'available': Número de timeouts disponibles
                - 'used': Número de timeouts usados
                - 'max_allowed': Máximo permitido en este periodo
                - 'can_use_more': Si se pueden usar más timeouts
        """
        max_allowed = self.get_max_allowed_for_period()
        used = self.get_used_count()

        return {
            'states': self.get_timeout_states(),
            'available': self.get_available_count(),
            'used': used,
            'max_allowed': max_allowed,
            'can_use_more': used < max_allowed
        }

