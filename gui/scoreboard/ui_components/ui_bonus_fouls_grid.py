"""
Componente UI moderno para la grilla de BONUS y contador de faltas de equipo.

Estructura:
- Primera fila: Etiqueta "BONUS" + indicador (botón que se enciende rojo cuando hay bonus)
- Segunda fila: Número grande de faltas del equipo en el cuarto actual
"""
import tkinter as tk


class BonusFoulsGrid:
    def __init__(self, parent, team_name, is_home_team):
        self.frame = tk.Frame(parent, bg="black")
        self.is_home_team = is_home_team
        self.team_name = team_name
        self.current_fouls = 0
        self.is_bonus = False

        self.bonus_label = tk.Label(
            self.frame,
            text="BONUS",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="black"
        )
        self.bonus_indicator = tk.Button(
            self.frame,
            width=2,
            height=1,
            bg="gray",
            state="disabled",
            relief=tk.FLAT,
            bd=2
        )

        self.fouls_label = tk.Label(
            self.frame,
            text="0",
            font=("Arial", 32, "bold"),
            fg="white",
            bg="black"
        )

        self.bonus_label.grid(row=0, column=0, padx=5, pady=2)
        self.bonus_indicator.grid(row=0, column=1, padx=5, pady=2)
        self.fouls_label.grid(row=1, column=0, columnspan=2, padx=5, pady=2)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def update_fouls(self, fouls_count):
        """Actualiza el contador de faltas del equipo."""
        self.current_fouls = fouls_count
        self.fouls_label.config(text=str(fouls_count))

    def set_bonus(self, is_bonus):
        """Activa/desactiva el indicador visual de BONUS."""
        self.is_bonus = is_bonus
        if is_bonus:
            self.bonus_indicator.config(bg="red")
        else:
            self.bonus_indicator.config(bg="gray")

    def reset_for_new_quarter(self):
        """Resetea el contador y bonus al cambiar de cuarto."""
        self.current_fouls = 0
        self.is_bonus = False
        self.update_fouls(0)
        self.set_bonus(False)
