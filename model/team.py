from model.timeout_manager import TimeoutManager


class Team:
    def __init__(self, logo, name, fouls, points, players, timeouts):
        self.logo = logo
        self.name = name
        self.fouls = fouls
        self.points = points
        self.players = players
        self.timeouts = timeouts  # Mantener por compatibilidad (deprecated)

        # Nuevo sistema de gestión de timeouts
        self.timeout_manager = TimeoutManager(current_quarter=1)