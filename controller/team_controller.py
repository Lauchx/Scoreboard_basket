class Team_controller:
    def __init__(self, team):
        self.team = team
    
    def add_point(self):
     self.team.points += 1