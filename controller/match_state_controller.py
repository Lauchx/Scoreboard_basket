from model.match_state import Match_state


class Match_state_controller:
    def __init__(self, home_team_controller,away_team_controller,possesion,quarter):
        self.home_team_controller = home_team_controller
        self.away_team_controller = away_team_controller
        self.possession = possesion  # valor inicial (también podría ser None)--> ?¡?¡?
        # Creamos el modelo
        self.match_state = Match_state(home_team_controller.team,away_team_controller.team,self.possession,quarter)
    