import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from types import SimpleNamespace
from gui.scoreboard.time_formatter import TimeFormatter
# from PIL import Image, ImageTk
# import os -- Revisar uso.

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE DISEÑO
# ═══════════════════════════════════════════════════════════════════════════
# Cambiar a True para activar el diseño moderno profesional tipo NBA/FIBA
# Cambiar a False para usar el diseño original
USE_MODERN_DESIGN = True
# ═══════════════════════════════════════════════════════════════════════════

if USE_MODERN_DESIGN:
    # Importar módulos del diseño moderno
    from gui.scoreboard.apply_modern_design import (
        apply_modern_design,
        setup_ui_modern,
        creates_home_team_modern,
        creates_away_team_modern,
        update_label_players_modern
    )
else:
    # Importar módulos del diseño original
    from gui.scoreboard.styles_scoreboard import apply_styles
    from gui.scoreboard.ui_components.ui_time import create_time_labels
    from gui.scoreboard.ui_components.ui_teams import (
        create_names_labels, create_logos_labels,
        create_points_labels, teams_labels_grid_configure
    )
    from gui.scoreboard.ui_components.ui_players import create_players_labels
    from gui.scoreboard.ui_components.ui_match import (
        create_possession_labels, create_quarter_labels, setup_ui_match
    )
    from gui.scoreboard.ui_components.ui_timeouts import (
        create_timeout_indicators, update_timeout_indicators
    )
class Gui_scoreboard:
    def __init__(self, root, match_state):
        """
        Args:
            home_team (Team): Objeto Team compartido con Gui_control_panel.
            away_team (Team): Objeto Team compartido con Gui_control_panel.
        """
        self.root = root
        self.root.title("Scoreboard")
        self.root.protocol("WM_DELETE_WINDOW", lambda: messagebox.showinfo("Info", "No podés cerrar esta ventana."))

        # Aplicar estilos según configuración
        if USE_MODERN_DESIGN:
            apply_modern_design(self)
        else:
            apply_styles()
            self.root.configure(bg="black")

        simpleNamespace_forUi(self)
        self.match_state = match_state

        # Inicializar el formateador de tiempo para el último minuto
        self.time_formatter = TimeFormatter()

        # Setup UI según diseño seleccionado
        if USE_MODERN_DESIGN:
            setup_ui_modern(self)
        else:
            setup_ui(self)

        if not hasattr(self, "labels"):
            self.labels = SimpleNamespace(home_team=SimpleNamespace(),
                                     away_team=SimpleNamespace(),
                                     match=SimpleNamespace())
        self.home_team_labels = _nameSpace_team_for_controller(self, self.match_state.home_team.name)
        self.away_team_labels =_nameSpace_team_for_controller(self, self.match_state.away_team.name)

        # Crear equipos según diseño seleccionado
        if USE_MODERN_DESIGN:
            creates_home_team_modern(self)
            creates_away_team_modern(self)
        else:
            creates_home_team(self)
            creates_away_team(self)
    # Updates labels functions
    def update_team_logo_label(self):
        self.labels.home_team.logo.config(image=self.match_state.home_team.logo)
        self.labels.away_team.logo.config(image=self.match_state.away_team.logo)
    def update_points_labels(self):
        self.labels.home_team.points.config(text=str(self.match_state.home_team.points))
        self.labels.away_team.points.config(text=str(self.match_state.away_team.points))

    def update_time_labels(self, milliseconds=0):
        """
        Actualiza el display del tiempo con formato automático según tiempo restante.

        Args:
            milliseconds (int): Milésimas de segundo (0-999) para formato SS:ms
        """
        total_seconds = self.match_state.seconds_time_left

        # Obtener información de display del formateador
        display_info = self.time_formatter.get_display_info(total_seconds, milliseconds)

        # Actualizar el texto del tiempo
        self.match.labels.time.config(text=display_info['text'])

        # Actualizar el color del borde si cambió de modo
        if display_info['should_update_border']:
            self.match.labels.time.config(
                highlightbackground=display_info['border_color'],
                highlightcolor=display_info['border_color']
            )

    def update_possession_labels(self, possession):
         self.match.labels.possesion.config(text=possession)   

    def update_team_names_labels(self):
        self.labels.home_team.name.config(text=self.match_state.home_team.name)
        self.labels.away_team.name.config(text=self.match_state.away_team.name)

    def update_quarter_labels(self, number):
        # Validar que el cuarto no baje de 1
        new_quarter = self.match_state.quarter + number
        if new_quarter < 1:
            print(f"[!] No se puede disminuir el cuarto por debajo de 1")
            return  # Ignorar la acción

        self.match_state.quarter = new_quarter
        if USE_MODERN_DESIGN:
            # En diseño moderno, solo actualizar el número (sin "Cuarto:")
            self.match.labels.quarter.config(text=str(self.match_state.quarter))
        else:
            # En diseño original, mostrar "Cuarto: X"
            self.match.labels.quarter.config(text=f"Cuarto: {self.match_state.quarter}")

    def update_possession_labels(self):
        current_possesion = self.match_state.possession
        if current_possesion == "Away":
            self.match_state.possession = "Home"
            new_possesion = "⇦"
            self.match.labels.possesion.config(text=str(new_possesion))
        else:
            self.match_state.possession = "Away"
            new_possesion = "⇨"
            self.match.labels.possesion.config(text=str(new_possesion))

    def update_timeout_labels(self):
        """
        Actualiza la visualización de los indicadores de timeout para ambos equipos.
        """
        if USE_MODERN_DESIGN:
            from gui.scoreboard.ui_components.ui_timeouts_modern import update_timeout_indicators_modern

            # Actualizar equipo local (pasar el timeout_manager completo)
            home_manager = self.match_state.home_team.timeout_manager
            update_timeout_indicators_modern(self.labels.home_team, home_manager)

            # Actualizar equipo visitante (pasar el timeout_manager completo)
            away_manager = self.match_state.away_team.timeout_manager
            update_timeout_indicators_modern(self.labels.away_team, away_manager)
        else:
            # Diseño original
            from gui.scoreboard.ui_components.ui_timeouts import update_timeout_indicators

            # Actualizar equipo local
            home_manager = self.match_state.home_team.timeout_manager
            update_timeout_indicators(self.labels.home_team, home_manager)

            # Actualizar equipo visitante
            away_manager = self.match_state.away_team.timeout_manager
            update_timeout_indicators(self.labels.away_team, away_manager)

    def update_fouls_labels(self):
        """
        Actualiza la visualización de faltas y BONUS para ambos equipos.
        """
        if USE_MODERN_DESIGN:
            from gui.scoreboard.ui_components.ui_fouls_modern import update_fouls_display_modern
            update_fouls_display_modern(self)
        # TODO: Implementar versión para diseño original si es necesario

    def update_label_players(self, player, team_contoller):
        if USE_MODERN_DESIGN:
            update_label_players_modern(self, player, team_contoller)
        else:
            team_simple_name_space = _nameSpace_team_for_controller(self, team_contoller.team.name)
            # Generar círculos de faltas (5 indicadores)
            foul_circles = self._get_foul_circles(player.foul)
            # Formato: num - nombre    ⚪⚪⚪⚪⚪
            player_text = f"{player.jersey_number} - {player.name}  {foul_circles}"
            team_simple_name_space.labels.players.insert(tk.END, player_text)
            index = team_simple_name_space.labels.players.size() - 1

            # Determinar color según estado
            if player.is_suspended:
                # ROJO: Jugador suspendido
                team_simple_name_space.labels.players.itemconfig(index, {'fg': 'red'})
            elif player.is_active:
                # VERDE: Jugador activo
                team_simple_name_space.labels.players.itemconfig(index, {'fg': 'green'})
            else:
                # NEGRO: Jugador inactivo
                team_simple_name_space.labels.players.itemconfig(index, {'fg': 'black'})

    def _get_foul_circles(self, foul_count):
        """Genera la representación visual de faltas con 5 círculos pequeños."""
        fouls = min(foul_count, 5)
        on = "●"   # Círculo negro relleno (U+25CF)
        off = "○"  # Círculo blanco vacío (U+25CB)
        return (on * fouls) + (off * (5 - fouls))

    def refresh_player_list(self, team_controller):
        """
        Refresca la lista completa de jugadores en el scoreboard.
        """
        if USE_MODERN_DESIGN:
            # En diseño moderno, update_label_players ya refresca toda la lista
            # Pasamos None como player ya que no se usa en la lógica moderna de refresco
            from gui.scoreboard.apply_modern_design import update_label_players_modern
            # Revisando apply_modern_design.py, usa player_obj del loop, el argumento player no se usa excepto compatibilidad
            update_label_players_modern(self, None, team_controller)
        else:
            # Diseño original: Limpiar y reconstruir
            team_simple_name_space = _nameSpace_team_for_controller(self, team_controller.team.name)
            if hasattr(team_simple_name_space.labels, 'players'):
                team_simple_name_space.labels.players.delete(0, tk.END)

                for player in team_controller.team.players:
                    self.update_label_players(player, team_controller)

def simpleNamespace_forUi(self):
        #self.labels = SimpleNamespace(home_team=SimpleNamespace(),away_team=SimpleNamespace(),match=SimpleNamespace())
        self.frames = SimpleNamespace(teams=SimpleNamespace()) 
        self.home_team = SimpleNamespace(labels=SimpleNamespace(), frames=SimpleNamespace())
        self.away_team = SimpleNamespace(labels=SimpleNamespace(), frames=SimpleNamespace())
        self.match = SimpleNamespace(labels=SimpleNamespace(), frames=SimpleNamespace())
# Create functions labels

def _nameSpace_team_for_controller(self, team_name) -> SimpleNamespace:
    if team_name == self.match_state.home_team.name:
        return self.home_team
    return self.away_team

def setup_ui(self):
    for column in range(3):
        self.root.grid_columnconfigure(column, weight=1, uniform="scoreboard")

    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_rowconfigure(1, weight=0)

    setup_ui_match(self)
    
    create_time_labels(self)
    create_possession_labels(self)
    create_quarter_labels(self)

def creates_home_team(self):
    self.home_team.frames = ttk.Frame(self.root, style="home_team.TFrame", padding=(20, 15))
    self.home_team.frames.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
    #ui_team
    teams_labels_grid_configure(self.home_team.frames)
    create_names_labels(self.home_team.frames, self.labels.home_team, self.match_state.home_team.name)
    create_logos_labels(self.home_team.frames, self.labels.home_team)
    create_points_labels(self.home_team.frames, self.labels.home_team, self.match_state.home_team.points)
    #ui_players
    create_players_labels(self.home_team, True)
    #ui_timeouts
    create_timeout_indicators(self.home_team.frames, self.labels.home_team)
   

def creates_away_team(self):
    self.away_team.frames = ttk.Frame(self.root, padding=(20, 15))
    self.away_team.frames.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=20)
    #ui_team
    teams_labels_grid_configure(self.away_team.frames)
    create_names_labels(self.away_team.frames, self.labels.away_team, self.match_state.away_team.name)
    create_logos_labels(self.away_team.frames, self.labels.away_team)
    create_points_labels(self.away_team.frames, self.labels.away_team, self.match_state.away_team.points)
    #ui_players
    create_players_labels(self.away_team, False)

    #ui_timeouts
    create_timeout_indicators(self.away_team.frames, self.labels.away_team)


# ═══════════════════════════════════════════════════════════════════════════
# MÉTODOS PARA CAMBIO DE FONDO AL TERMINAR EL TIEMPO
# ═══════════════════════════════════════════════════════════════════════════

def set_background_red(self):
    """
    Cambia el fondo del scoreboard a rojo cuando el tiempo llega a 00:00.
    """
    try:
        if USE_MODERN_DESIGN:
            # Guardar color original si no está guardado
            if not hasattr(self, '_original_bg_color'):
                self._original_bg_color = self.modern_style.COLORS['bg_primary']

            # Cambiar fondo a rojo
            self.root.configure(bg='#FF0000')

            # Cambiar también los frames principales
            for widget in self.root.winfo_children():
                try:
                    widget.configure(bg='#FF0000')
                except:
                    pass
        else:
            # Diseño original
            if not hasattr(self, '_original_bg_color'):
                self._original_bg_color = 'black'
            self.root.configure(bg='#FF0000')

        print("[OK] Fondo del scoreboard cambiado a ROJO")
    except Exception as e:
        print(f"[!] Error al cambiar fondo a rojo: {e}")


def restore_background(self):
    """
    Restaura el fondo original del scoreboard.
    """
    try:
        if hasattr(self, '_original_bg_color'):
            if USE_MODERN_DESIGN:
                original_color = self.modern_style.COLORS['bg_primary']
                self.root.configure(bg=original_color)

                # Restaurar también los frames principales
                for widget in self.root.winfo_children():
                    try:
                        widget.configure(bg=original_color)
                    except:
                        pass
            else:
                self.root.configure(bg=self._original_bg_color)

            print("[OK] Fondo del scoreboard restaurado")
    except Exception as e:
        print(f"[!] Error al restaurar fondo: {e}")


# Agregar métodos a la clase Gui_scoreboard
Gui_scoreboard.set_background_red = set_background_red
Gui_scoreboard.restore_background = restore_background


# ═══════════════════════════════════════════════════════════════════════════════
# TOGGLE VISIBILIDAD DE SECCIÓN DE JUGADORES
# ═══════════════════════════════════════════════════════════════════════════════

# Configuración de tamaños de ventana para toggle de jugadores
WINDOW_SIZES = {
    'full_width': 1200,           # Ancho con ambos jugadores visibles
    'one_hidden_width': 900,      # Ancho con un panel de jugadores oculto
    'both_hidden_width': 600,     # Ancho con ambos paneles de jugadores ocultos
    'height': 700,                # Alto constante
}


def toggle_players_section(self, is_home, visible):
    """
    Muestra u oculta la sección de jugadores de un equipo en el scoreboard.
    Ajusta automáticamente el ancho de la ventana y colapsa las columnas vacías.

    Args:
        is_home (bool): True para equipo local, False para visitante
        visible (bool): True para mostrar, False para ocultar
    """
    try:
        # Obtener el namespace del equipo correspondiente
        team_namespace = self.home_team if is_home else self.away_team

        # Verificar que existe el widget de jugadores
        if not hasattr(team_namespace.labels, 'players'):
            print(f"[!] No se encontró el widget de jugadores para {'HOME' if is_home else 'AWAY'}")
            return

        players_widget = team_namespace.labels.players
        col = 0 if is_home else 2

        if visible:
            # Mostrar la sección de jugadores
            padding = (0, 15) if is_home else (15, 0)
            players_widget.grid(
                row=0,
                column=col,
                rowspan=3,
                sticky="nsew",
                padx=padding,
                pady=5
            )
            # Restaurar peso de la columna para que ocupe espacio
            self.root.grid_columnconfigure(col, weight=3)
            print(f"[OK] Jugadores {'LOCAL' if is_home else 'VISITANTE'} visibles")
        else:
            # Ocultar la sección de jugadores (quitar del grid sin destruir)
            players_widget.grid_remove()
            # Colapsar la columna para que no ocupe espacio
            self.root.grid_columnconfigure(col, weight=0, minsize=0)
            print(f"[OK] Jugadores {'LOCAL' if is_home else 'VISITANTE'} ocultos")

        # Ajustar tamaño de ventana según jugadores visibles
        _adjust_window_size(self)

    except Exception as e:
        print(f"[!] Error al toggle jugadores: {e}")


def _adjust_window_size(self):
    """
    Ajusta el tamaño de la ventana según cuántos paneles de jugadores están visibles.
    Mantiene la ventana completamente responsive (se puede achicar manualmente).
    """
    try:
        # Verificar estado de visibilidad de ambos paneles
        home_visible = True
        away_visible = True

        if hasattr(self.home_team.labels, 'players'):
            home_visible = self.home_team.labels.players.winfo_ismapped()
        if hasattr(self.away_team.labels, 'players'):
            away_visible = self.away_team.labels.players.winfo_ismapped()

        # Determinar ancho según visibilidad
        if home_visible and away_visible:
            new_width = WINDOW_SIZES['full_width']
        elif home_visible or away_visible:
            new_width = WINDOW_SIZES['one_hidden_width']
        else:
            new_width = WINDOW_SIZES['both_hidden_width']

        height = WINDOW_SIZES['height']

        # Aplicar nuevo tamaño
        self.root.geometry(f"{new_width}x{height}")

        # Mínimo MUY pequeño para permitir responsive total
        self.root.minsize(400, 250)

        print(f"[OK] Ventana ajustada a {new_width}x{height}")

    except Exception as e:
        print(f"[!] Error al ajustar ventana: {e}")


# Agregar métodos a la clase Gui_scoreboard
Gui_scoreboard.toggle_players_section = toggle_players_section
