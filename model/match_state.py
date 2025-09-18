class Match_state:
    def __init__(self, home_team, away_team,seconds_match_time, seconds_time_left, possession,quarter):
        self.home_team = home_team
        self.away_team = away_team
        self.seconds_match_time = seconds_match_time
        self.possession = possession
        self.quarter = quarter
        self.seconds_time_left = seconds_time_left
        ## Se debe agregar Cuarto de partido tambien
 