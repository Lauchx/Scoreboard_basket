class Team_controller:
    def __init__(self, team):
        self.team = team

    def add_point(self):
        self.team.points += 1

    def substract_point(self):
        # No permitir puntos negativos
        if self.team.points > 0:
            self.team.points -= 1

    def add_foul(self):
        self.team.fouls += 1

    def substract_foul(self):
        # No permitir faltas negativas
        if self.team.fouls > 0:
            self.team.fouls -= 1

    def change_name(self, name):
        self.team.name = name

    def change_logo(self, logo):
        self.team.logo = logo

    def add_player_in_team(self, player):
        self.team.players.append(player)

    def show_team_players(self):
        print(self.team.name)

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS DE GESTIÓN DE TIMEOUTS
    # ═══════════════════════════════════════════════════════════

    def toggle_timeout(self, timeout_index):
        """
        Alterna el estado de un timeout (usado <-> disponible).

        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)

        Returns:
            bool: True si se cambió el estado exitosamente
        """
        return self.team.timeout_manager.toggle_timeout(timeout_index)

    def use_timeout(self, timeout_index):
        """
        Marca un timeout como usado.

        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)

        Returns:
            bool: True si se usó exitosamente
        """
        return self.team.timeout_manager.use_timeout(timeout_index)

    def restore_timeout(self, timeout_index):
        """
        Restaura un timeout (marca como disponible).

        Args:
            timeout_index (int): Índice del timeout (0, 1, o 2)

        Returns:
            bool: True si se restauró exitosamente
        """
        return self.team.timeout_manager.restore_timeout(timeout_index)

    def reset_timeouts(self):
        """
        Reinicia todos los timeouts del equipo.
        """
        self.team.timeout_manager.reset_all()

    def update_timeout_quarter(self, new_quarter):
        """
        Actualiza el cuarto actual para el gestor de timeouts.

        Args:
            new_quarter (int): Número del nuevo cuarto
        """
        self.team.timeout_manager.reset_for_period(new_quarter)

    def get_timeout_states(self):
        """
        Obtiene el estado de todos los timeouts.

        Returns:
            list: Lista de 3 booleanos (True = usado, False = disponible)
        """
        return self.team.timeout_manager.get_timeout_states()

    def get_timeout_display_info(self):
        """
        Obtiene información completa para mostrar en la UI.

        Returns:
            dict: Información de display de timeouts
        """
        return self.team.timeout_manager.get_display_info()