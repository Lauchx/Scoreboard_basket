import tkinter as tk

class Gui_scoreboard:
    def __init__(self, root, home_team, away_team):
        self.root = root
        self.root.title("Scoreboard")
        self.root.configure(bg="black")
    # Elementos visuales del marcador
        self.logo1_label = tk.Label(self.root, bg="black")
        self.logo1_label.grid(row=0, column=0, padx=10, pady=5)

        self.home_team_label = tk.Label(self.root, text="Equipo 1", font=("Arial", 40, "bold"), fg="white", bg="black")
        self.home_team_label.grid(row=1, column=0, padx=20)

        self.time_label = tk.Label(self.root, text="15:00", font=("Arial", 60), fg="white", bg="black")
        self.time_label.grid(row=0, column=1)

        self.logo2_label = tk.Label(self.root, bg="black")
        self.logo2_label.grid(row=0, column=2, padx=10, pady=5)

        self.away_team_label = tk.Label(self.root, text="Equipo 2", font=("Arial", 40, "bold"), fg="white", bg="black")
        self.away_team_label.grid(row=1, column=2, padx=20)

        # Sección de puntajes
        self.puntaje1_label = tk.Label(self.root, text="0", font=("Arial", 80), fg="orange", bg="black")
        self.puntaje1_label.grid(row=2, column=0)

        self.quarter_label = tk.Label(self.root, text="Cuarto: 1", font=("Arial", 30), fg="white", bg="black")
        self.quarter_label.grid(row=1, column=1)

        self.puntaje2_label = tk.Label(self.root, text="0", font=("Arial", 80), fg="orange", bg="black")
        self.puntaje2_label.grid(row=2, column=2)

        self.poseesion_label = tk.Label(self.root, text="24", font=("Arial", 50), fg="red", bg="black")
        self.poseesion_label.grid(row=2, column=1)

        self.poseesion_texto = tk.Label(self.root, text="POSESIÓN", font=("Arial", 30), fg="white", bg="black")
        self.poseesion_texto.grid(row=3, column=1)

    def actualizar_marcador(self, home_team, away_team, tiempo, quarter, poseesion):
        """Actualiza los valores visibles en la pantalla pública."""
        self.puntaje1_label.config(text=str(home_team))
        self.puntaje2_label.config(text=str(away_team))
        self.tiempo_label.config(text=tiempo)
        self.quarter_label.config(text=f"Cuarto: {quarter}")
        self.poseesion_label.config(text=str(poseesion))

if __name__ == "__main__":
    root = tk.Tk()
    app = Gui_scoreboard(root)
    root.mainloop()