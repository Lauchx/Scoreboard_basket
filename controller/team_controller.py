class Team_controller:
    def __init__(self, team):
        self.team = team
    
    def add_point(self):
        self.team.points += 1
    def substract_point(self):
        self.team.points -= 1   
    def change_name(self, name):
        self.team.name = name
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

    def show_team_players(self):
        print(self.team.name)


        