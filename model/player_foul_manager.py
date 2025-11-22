"""
Módulo para la gestión de faltas individuales y suspensión de jugadores.
"""

class PlayerFoulManager:
    SUSPENSION_THRESHOLD = 5

    def __init__(self, player):
        self.player = player

    def add_foul(self):
        self.player.foul += 1
        if self.player.foul >= self.SUSPENSION_THRESHOLD:
            self.player.is_suspended = True
        return self.player.foul, self.player.is_suspended

    def subtract_foul(self):
        if self.player.foul > 0:
            self.player.foul -= 1
        if self.player.foul < self.SUSPENSION_THRESHOLD:
            self.player.is_suspended = False
        return self.player.foul, self.player.is_suspended

    def suspend_player(self):
        self.player.is_suspended = True
        return self.player.is_suspended

    def unsuspend_player(self):
        self.player.is_suspended = False
        return self.player.is_suspended

    def reset_fouls(self):
        self.player.foul = 0
        self.player.is_suspended = False
        return self.player.foul, self.player.is_suspended
