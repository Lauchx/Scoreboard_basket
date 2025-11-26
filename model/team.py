from model.timeout_manager import TimeoutManager
from model.foul_manager import FoulManager


class Team:
    def __init__(self, logo, name, fouls, points, players, timeouts):
        self.logo = logo
        self.name = name
        self.fouls = fouls  # Mantener por compatibilidad (deprecated)
        self.points = points
        self.players = players
        self.timeouts = timeouts  # Mantener por compatibilidad (deprecated)

        # Nuevo sistema de gestión de timeouts
        self.timeout_manager = TimeoutManager(current_quarter=1)

        # Nuevo sistema de gestión de faltas de equipo
        self.foul_manager = FoulManager(current_quarter=1)