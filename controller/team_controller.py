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

    # ═══════════════════════════════════════════════════════════
    # MÉTODOS DE GESTIÓN DE FALTAS
    # ═══════════════════════════════════════════════════════════

    def add_player_foul(self, player):
        """
        Suma una falta a un jugador específico.
        También suma una falta al contador del equipo.

        Args:
            player (Player): Jugador al que sumar la falta

        Returns:
            dict: Información sobre el cambio con player_info y team_info
        """
        # Sumar falta al jugador
        player_info = player.add_foul()

        # Sumar falta al contador del equipo
        team_info = self.team.foul_manager.add_team_foul()

        return {
            'player_info': player_info,
            'team_info': team_info
        }

    def subtract_player_foul(self, player):
        """
        Resta una falta a un jugador específico.
        También resta una falta al contador del equipo.

        Args:
            player (Player): Jugador al que restar la falta

        Returns:
            dict: Información sobre el cambio
        """
        # Restar falta al jugador
        player_info = player.subtract_foul()

        # Restar falta al contador del equipo
        team_info = self.team.foul_manager.subtract_team_foul()

        return {
            'player_info': player_info,
            'team_info': team_info
        }

    def suspend_player_manually(self, player):
        """
        Suspende a un jugador manualmente (falta antideportiva, etc.).

        Args:
            player (Player): Jugador a suspender
        """
        player.suspend_manually()

    def unsuspend_player_manually(self, player):
        """
        Quita la suspensión manual de un jugador.

        Args:
            player (Player): Jugador a quitar suspensión
        """
        player.unsuspend_manually()

    def get_team_foul_status(self):
        """
        Retorna el estado de faltas del equipo.

        Returns:
            dict: Información con faltas del equipo y estado de bonus
        """
        return self.team.foul_manager.get_status_info()

    def update_foul_quarter(self, new_quarter):
        """
        Actualiza el cuarto actual para el gestor de faltas.
        Resetea el contador de faltas del equipo y el bonus.

        Args:
            new_quarter (int): Número del nuevo cuarto
        """
        self.team.foul_manager.reset_for_period(new_quarter)

    def get_team_fouls(self):
        """
        Retorna el número de faltas del equipo en el cuarto actual.

        Returns:
            int: Número de faltas del equipo
        """
        return self.team.foul_manager.get_team_fouls()

    def is_team_bonus(self):
        """
        Retorna si el equipo está en estado de BONUS.

        Returns:
            bool: True si el equipo está en BONUS
        """
        return self.team.foul_manager.get_bonus_status()

    def add_team_foul(self):
        """
        Suma una falta al contador del equipo (sin asociarla a un jugador).

        Returns:
            dict: Información actualizada del equipo
        """
        return self.team.foul_manager.add_team_foul()

    def subtract_team_foul(self):
        """
        Resta una falta al contador del equipo.

        Returns:
            dict: Información actualizada del equipo
        """
        return self.team.foul_manager.subtract_team_foul()

    def suspend_player(self, player):
        """
        Alias para suspend_player_manually (compatibilidad con UI).
        """
        self.suspend_player_manually(player)

    def unsuspend_player(self, player):
        """
        Alias para unsuspend_player_manually (compatibilidad con UI).
        """
        self.unsuspend_player_manually(player)