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
        self.team.players.append(player)

    def show_team_players(self):
        print(self.team.name)