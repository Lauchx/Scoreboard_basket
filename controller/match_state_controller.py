from model.match_state import Match_state


class Match_state_controller:
    def __init__(self, home_team_controller,away_team_controller,seconds_match_time, seconds_time_left,possession,quarter):
        self.home_team_controller = home_team_controller
        self.away_team_controller = away_team_controller
        self.possession = possession  # valor inicial (también podría ser None)--> ?¡?¡?
        # Creamos el modelo
        self.match_state = Match_state(home_team_controller.team,away_team_controller.team,seconds_match_time, seconds_time_left,self.possession,quarter)
    