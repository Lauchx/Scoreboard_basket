import tkinter as tk
from gui.scoreboard.gui_scoreboard import Gui_scoreboard
from team.model.entity.team import Team
def main():
    main_window =tk.Tk()
    home_team = Team("logo","Home Team",0,0,[],3)
    away_team = Team("logo","Away Team",0,0,[],3)
    scoreboard_window = Gui_scoreboard(tk.Toplevel(main_window), home_team, away_team)
    main_window.mainloop()
if __name__ == "__main__":
    main()