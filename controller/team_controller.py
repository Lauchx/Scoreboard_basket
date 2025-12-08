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
        # Limitar nombre a 12 caracteres máximo
        MAX_TEAM_NAME_LENGTH = 12
        self.team.name = name[:MAX_TEAM_NAME_LENGTH] if len(name) > MAX_TEAM_NAME_LENGTH else name

    def change_logo(self, logo):
        self.team.logo = logo

    def add_player_in_team(self, player):
        # Add player and keep players sorted by jersey number
        self.team.players.append(player)
        try:
            self.team.players.sort(key=lambda p: int(p.jersey_number))
        except Exception:
            # Fallback: keep insertion order if any jersey_number is not int-convertible
            pass
        
    def remove_player(self, jersey_number):
        print(f"Intentando eliminar jugador con número {jersey_number}")
        print("Jugadores antes de eliminar:")
        for player in self.team.players:
            print(f"Jugador: {player.name}, Número: {player.jersey_number}, Tipo: {type(player.jersey_number)}")
        
        # Asegurarse de que ambos números son del mismo tipo (str o int)
        if isinstance(jersey_number, str):
            jersey_number = int(jersey_number)
            
        # Filtrar los jugadores
        self.team.players = [p for p in self.team.players if int(p.jersey_number) != jersey_number]
        
        print("Jugadores después de eliminar:")
        for player in self.team.players:
            print(f"Jugador: {player.name}, Número: {player.jersey_number}")
        for a in self.team.players:
            print(a.jersey_number)
        
    def toggle_player_active(self, jersey_number):
        if isinstance(jersey_number, str):
            jersey_number = int(jersey_number)
            
        for player in self.team.players:
            if int(player.jersey_number) == jersey_number:
                player.is_active = not player.is_active
                print(f"Cambiando estado del jugador {player.name} ({player.jersey_number}) a {player.is_active}")
                break
    
    def get_player_numbers(self):
        return [player.get_display_text() for player in self.team.players]

    """"
    def add_player_in_team(self, player):
        # Add player and keep players sorted by jersey number
        self.team.players.append(player)
        try:
            self.team.players.sort(key=lambda p: int(p.jersey_number))
        except Exception:
            # Fallback: keep insertion order if any jersey_number is not int-convertible
            pass
  
    def remove_player(self, jersey_number):
        print(f"Intentando eliminar jugador con número {jersey_number}")
        
        # Asegurarse de que ambos números son del mismo tipo (str o int)
        if isinstance(jersey_number, str):
            jersey_number = int(jersey_number)
            
        # Filtrar los jugadores
        self.team.players = [p for p in self.team.players if int(p.jersey_number) != jersey_number]
    """     

    def toggle_player_active(self, jersey_number):
        if isinstance(jersey_number, str):
            jersey_number = int(jersey_number)
            
        for player in self.team.players:
            if int(player.jersey_number) == jersey_number:
                player.is_active = not player.is_active
                print(f"Cambiando estado del jugador {player.name} ({player.jersey_number}) a {player.is_active}")
                break
    
    def get_player_numbers(self):
        return [player.get_display_text() for player in self.team.players]
        
    def show_team_players(self):
        print(self.team.name)


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
        NO suma automáticamente al contador del equipo.
        Se debe registrar la falta de equipo primero con add_team_foul().

        Args:
            player (Player): Jugador al que sumar la falta

        Returns:
            dict: Información sobre el cambio con player_info y team_info
        """
        # Sumar falta al jugador
        player_info = player.add_foul()

        # Registrar que esta falta fue asignada a un jugador
        self.team.foul_manager.register_player_foul()

        # Obtener estado actual del equipo (sin modificar)
        team_info = self.team.foul_manager.get_status_info()

        return {
            'player_info': player_info,
            'team_info': team_info
        }

    def subtract_player_foul(self, player):
        """
        Resta una falta a un jugador específico.
        NO modifica automáticamente el contador del equipo.

        Args:
            player (Player): Jugador al que restar la falta

        Returns:
            dict: Información sobre el cambio
        """
        # Restar falta al jugador
        player_info = player.subtract_foul()

        # Des-registrar la falta de jugador
        self.team.foul_manager.unregister_player_foul()

        # Obtener estado actual del equipo (sin modificar)
        team_info = self.team.foul_manager.get_status_info()

        return {
            'player_info': player_info,
            'team_info': team_info
        }

    def can_assign_player_foul(self):
        """
        Verifica si se puede asignar una falta a un jugador.

        Returns:
            bool: True si hay faltas de equipo disponibles para asignar
        """
        return self.team.foul_manager.can_assign_player_foul()

    def get_available_fouls_for_players(self):
        """
        Retorna el número de faltas de equipo disponibles para asignar a jugadores.

        Returns:
            int: Número de faltas disponibles
        """
        return self.team.foul_manager.get_available_fouls_for_players()

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
