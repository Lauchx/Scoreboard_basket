class Player:
    """
    Representa a un jugador de básquetbol.

    Attributes:
        name (str): Nombre del jugador
        jersey_number (int): Número de camiseta
        point (int): Puntos anotados
        foul (int): Número de faltas personales
        is_active (bool): Si el jugador está activo en cancha
        is_suspended (bool): Si el jugador está suspendido (5 faltas o falta antideportiva)
    """

    # Constante
    MAX_FOULS = 5  # Número máximo de faltas antes de suspensión

    def __init__(self, name, jersey_number, is_active):
        self.name = name
        self.jersey_number = jersey_number
        self.point = 0
        self.foul = 0
        self.is_active = is_active
        self.is_suspended = False  # Estado de suspensión

    def add_foul(self):
        """
        Suma una falta al jugador.
        Si llega a 5 faltas, se suspende automáticamente.

        Returns:
            dict: Información sobre el cambio
        """
        self.foul += 1
        suspended_now = False

        # Verificar si alcanzó el máximo de faltas
        if self.foul >= self.MAX_FOULS and not self.is_suspended:
            self.is_suspended = True
            suspended_now = True

        return {
            'total_fouls': self.foul,
            'is_suspended': self.is_suspended,
            'suspended_now': suspended_now
        }

    def subtract_foul(self):
        """
        Resta una falta al jugador (para correcciones).
        Si baja de 5 faltas, se quita la suspensión automática.

        Returns:
            dict: Información sobre el cambio
        """
        if self.foul > 0:
            self.foul -= 1

        unsuspended_now = False

        # Si baja de 5 faltas, quitar suspensión automática
        if self.foul < self.MAX_FOULS and self.is_suspended:
            self.is_suspended = False
            unsuspended_now = True

        return {
            'total_fouls': self.foul,
            'is_suspended': self.is_suspended,
            'unsuspended_now': unsuspended_now
        }

    def suspend_manually(self):
        """
        Suspende al jugador manualmente (por falta antideportiva, etc.).
        """
        self.is_suspended = True

    def unsuspend_manually(self):
        """
        Quita la suspensión manual del jugador.
        """
        self.is_suspended = False

    def get_foul_status(self):
        """
        Retorna el estado de faltas del jugador.

        Returns:
            dict: Información con faltas y estado de suspensión
        """
        fouls_to_suspension = max(0, self.MAX_FOULS - self.foul)

        return {
            'fouls': self.foul,
            'is_suspended': self.is_suspended,
            'fouls_to_suspension': fouls_to_suspension
        }
