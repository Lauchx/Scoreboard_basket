"""
Gestor de faltas de equipo para básquetbol.
Maneja el contador de faltas por cuarto y el estado de BONUS del equipo.
"""


class FoulManager:
    """
    Gestiona las faltas de equipo y el estado de BONUS según las reglas oficiales.

    Reglas:
    - Cada cuarto tiene su propio contador de faltas de equipo
    - Al llegar a 5 faltas en un cuarto, el equipo entra en BONUS
    - En BONUS, cada falta adicional concede tiro libre
    - Al cambiar de cuarto, el contador se resetea y el BONUS se desactiva
    - Las faltas individuales de jugadores NO se resetean
    - Las faltas de equipo mostradas no pueden superar 5
    - Se debe registrar primero la falta de equipo antes de asignarla a un jugador

    Attributes:
        team_fouls_this_quarter (int): Contador de faltas del equipo en el cuarto actual (máximo 5 para display)
        player_fouls_this_quarter (int): Contador de faltas asignadas a jugadores en este cuarto
        is_bonus (bool): Estado de BONUS del equipo
        current_quarter (int): Cuarto actual del partido
    """

    # Constantes
    BONUS_THRESHOLD = 5  # Número de faltas para entrar en BONUS
    MAX_DISPLAY_FOULS = 5  # Máximo de faltas mostradas en el tablero

    def __init__(self, current_quarter=1):
        """
        Inicializa el gestor de faltas.

        Args:
            current_quarter (int): Cuarto inicial del partido (default: 1)
        """
        self.current_quarter = current_quarter
        self.team_fouls_this_quarter = 0
        self.player_fouls_this_quarter = 0  # Tracking de faltas asignadas a jugadores en este cuarto
        self.is_bonus = False

    def add_team_foul(self):
        """
        Suma una falta al contador del equipo en el cuarto actual.
        El contador mostrado no puede superar 5 faltas.
        Activa el BONUS si se alcanza el umbral.

        Returns:
            dict: Información sobre el cambio con:
                - 'total_fouls': Total de faltas del equipo en este cuarto (máximo 5)
                - 'is_bonus': Si el equipo está en BONUS
                - 'bonus_activated': Si se activó el BONUS con esta falta
                - 'at_limit': Si ya se alcanzó el límite de 5 faltas
        """
        # No permitir sumar más de 5 faltas de equipo para el display
        if self.team_fouls_this_quarter >= self.MAX_DISPLAY_FOULS:
            return {
                'total_fouls': self.team_fouls_this_quarter,
                'is_bonus': self.is_bonus,
                'bonus_activated': False,
                'at_limit': True
            }

        self.team_fouls_this_quarter += 1
        bonus_activated = False
        if self.team_fouls_this_quarter >= self.BONUS_THRESHOLD and not self.is_bonus:
            self.is_bonus = True
            bonus_activated = True
        return {
            'total_fouls': self.team_fouls_this_quarter,
            'is_bonus': self.is_bonus,
            'bonus_activated': bonus_activated,
            'at_limit': self.team_fouls_this_quarter >= self.MAX_DISPLAY_FOULS
        }
    
    def subtract_team_foul(self):
        """
        Resta una falta al contador del equipo (para correcciones).
        Desactiva el BONUS si se baja del umbral.
        No puede bajar de 0.

        Returns:
            dict: Información sobre el cambio con:
                - 'total_fouls': Total de faltas del equipo en este cuarto
                - 'is_bonus': Si el equipo está en BONUS
                - 'bonus_deactivated': Si se desactivó el BONUS con esta resta
        """
        if self.team_fouls_this_quarter > 0:
            self.team_fouls_this_quarter -= 1

        bonus_deactivated = False

        # Verificar si se debe desactivar el BONUS
        if self.team_fouls_this_quarter < self.BONUS_THRESHOLD and self.is_bonus:
            self.is_bonus = False
            bonus_deactivated = True

        return {
            'total_fouls': self.team_fouls_this_quarter,
            'is_bonus': self.is_bonus,
            'bonus_deactivated': bonus_deactivated
        }

    def reset_for_period(self, new_quarter):
        """
        Resetea el contador de faltas y el BONUS para un nuevo cuarto.
        Sigue el mismo patrón que TimeoutManager.reset_for_period()
        Las faltas de jugadores en este cuarto también se resetean para la validación.

        Args:
            new_quarter (int): Número del nuevo cuarto
        """
        self.current_quarter = new_quarter
        self.team_fouls_this_quarter = 0
        self.player_fouls_this_quarter = 0  # Resetear contador de faltas asignadas a jugadores
        self.is_bonus = False
        print(f"🔄 Faltas de equipo reseteadas para cuarto {new_quarter}")

    def register_player_foul(self):
        """
        Registra que una falta fue asignada a un jugador en este cuarto.
        Se usa para validar que hay faltas de equipo disponibles.
        """
        self.player_fouls_this_quarter += 1

    def unregister_player_foul(self):
        """
        Des-registra una falta de jugador (para correcciones).
        """
        if self.player_fouls_this_quarter > 0:
            self.player_fouls_this_quarter -= 1

    def can_assign_player_foul(self):
        """
        Verifica si se puede asignar una falta a un jugador.

        Reglas:
        - Si las faltas de equipo son 5 o más, siempre se puede asignar
        - Si las faltas de equipo son menores a 5, solo se puede asignar si
          hay faltas de equipo "disponibles" (no asignadas a jugadores)

        Returns:
            bool: True si se puede asignar una falta a un jugador
        """
        # Si ya estamos en el límite de faltas (5), siempre se permite
        if self.team_fouls_this_quarter >= self.MAX_DISPLAY_FOULS:
            return True

        # Si hay más faltas de equipo que faltas asignadas a jugadores, se permite
        return self.player_fouls_this_quarter < self.team_fouls_this_quarter

    def get_available_fouls_for_players(self):
        """
        Retorna el número de faltas de equipo disponibles para asignar a jugadores.

        Returns:
            int: Número de faltas disponibles (puede ser infinito si está en 5)
        """
        if self.team_fouls_this_quarter >= self.MAX_DISPLAY_FOULS:
            return float('inf')  # En el límite, se pueden asignar infinitas
        return max(0, self.team_fouls_this_quarter - self.player_fouls_this_quarter)
    
    def get_team_fouls(self):
        """
        Retorna el número de faltas del equipo en el cuarto actual.
        
        Returns:
            int: Número de faltas del equipo
        """
        return self.team_fouls_this_quarter
    
    def get_bonus_status(self):
        """
        Retorna el estado de BONUS del equipo.
        
        Returns:
            bool: True si el equipo está en BONUS, False si no
        """
        return self.is_bonus
    
    def get_status_info(self):
        """
        Retorna información completa del estado de faltas.

        Returns:
            dict: Información con:
                - 'team_fouls': Faltas del equipo en este cuarto
                - 'is_bonus': Estado de BONUS
                - 'fouls_to_bonus': Faltas que faltan para BONUS (0 si ya está en BONUS)
                - 'player_fouls_this_quarter': Faltas asignadas a jugadores en este cuarto
                - 'available_for_players': Faltas disponibles para asignar a jugadores
        """
        fouls_to_bonus = max(0, self.BONUS_THRESHOLD - self.team_fouls_this_quarter)

        return {
            'team_fouls': self.team_fouls_this_quarter,
            'is_bonus': self.is_bonus,
            'fouls_to_bonus': fouls_to_bonus,
            'player_fouls_this_quarter': self.player_fouls_this_quarter,
            'available_for_players': self.get_available_fouls_for_players()
        }

