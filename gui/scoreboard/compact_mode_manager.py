"""
Módulo para gestionar el Modo Compacto del scoreboard.
Permite alternar entre modo normal y modo compacto (mini-visor).

El modo compacto:
- Oculta la sección de jugadores de ambos equipos
- Reduce el tamaño general del scoreboard
- Mantiene el reloj visible y legible
- Ajusta proporcionalmente las secciones de cuarto, faltas y posesión
"""

import tkinter as tk


class CompactModeManager:
    """
    Gestor del Modo Compacto para el scoreboard.
    Maneja la transición entre modo normal y modo compacto.
    """
    
    # Configuración de tamaños para modo compacto
    # Todo se reduce al 50% uniformemente
    COMPACT_CONFIG = {
        'window_width': 550,       # Ancho reducido (mitad de 1200 aprox)
        'window_height': 320,      # Alto reducido (mitad de 700 aprox)
        'min_window_width': 400,   # Ancho mínimo permitido
        'min_window_height': 250,  # Alto mínimo permitido
        'scale_factor': 0.50,      # Escala uniforme: TODO al 50%
    }

    # Configuración de tamaños para modo normal
    NORMAL_CONFIG = {
        'window_width': 1200,      # Ancho de ventana en modo normal
        'window_height': 700,      # Alto de ventana en modo normal
        'scale_factor': 1.0,       # Factor de escala normal
        'min_window_width': 1000,  # Ancho mínimo en modo normal
        'min_window_height': 600,  # Alto mínimo en modo normal
    }
    
    def __init__(self, scoreboard):
        """
        Inicializa el gestor de modo compacto.
        
        Args:
            scoreboard: Instancia de Gui_scoreboard
        """
        self.scoreboard = scoreboard
        self.is_compact = False
        
        # Guardar estado original del scoreboard
        self._save_original_state()
    
    def _save_original_state(self):
        """Guarda el estado original del scoreboard para poder restaurarlo."""
        root = self.scoreboard.root
        
        self.original_state = {
            'geometry': root.geometry(),
            'minsize': (root.minsize()[0], root.minsize()[1]) if root.minsize() else (1000, 600),
            'players_visible_home': True,
            'players_visible_away': True,
        }
    
    def toggle_compact_mode(self):
        """
        Alterna entre modo compacto y modo normal.
        
        Returns:
            bool: True si está en modo compacto, False si está en modo normal
        """
        if self.is_compact:
            self._disable_compact_mode()
        else:
            self._enable_compact_mode()
        
        return self.is_compact
    
    def _enable_compact_mode(self):
        """Activa el modo compacto del scoreboard."""
        if self.is_compact:
            return

        root = self.scoreboard.root
        config = self.COMPACT_CONFIG

        # 1. Guardar estado actual antes de cambiar
        self.original_state['geometry'] = root.geometry()

        # 2. Ocultar sección de jugadores de ambos equipos
        self._hide_players_sections()

        # 3. Ocultar logos de los equipos
        self._hide_logos()

        # 4. Aplicar escala compacta a los estilos
        self._apply_compact_scale()

        # 5. Ajustar tamaño de ventana a formato compacto (al final para que se recalcule)
        root.minsize(config['min_window_width'], config['min_window_height'])
        root.geometry(f"{config['window_width']}x{config['window_height']}")

        self.is_compact = True
        print("[OK] Modo Compacto: ACTIVADO")

    def _disable_compact_mode(self):
        """Desactiva el modo compacto y restaura el scoreboard al estado normal."""
        if not self.is_compact:
            return

        root = self.scoreboard.root
        config = self.NORMAL_CONFIG

        # 1. Restaurar escala normal primero
        self._apply_normal_scale()

        # 2. Mostrar logos de los equipos
        self._show_logos()

        # 3. Mostrar sección de jugadores de ambos equipos
        self._show_players_sections()

        # 4. Restaurar tamaño de ventana
        root.minsize(config['min_window_width'], config['min_window_height'])
        root.geometry(f"{config['window_width']}x{config['window_height']}")

        self.is_compact = False
        print("[OK] Modo Compacto: DESACTIVADO")
    
    def _hide_players_sections(self):
        """Oculta la sección de jugadores de ambos equipos y colapsa las columnas."""
        try:
            root = self.scoreboard.root

            # Ocultar jugadores del equipo local
            if hasattr(self.scoreboard.home_team.labels, 'players'):
                self.scoreboard.home_team.labels.players.grid_remove()
                root.grid_columnconfigure(0, weight=0, minsize=0)

            # Ocultar jugadores del equipo visitante
            if hasattr(self.scoreboard.away_team.labels, 'players'):
                self.scoreboard.away_team.labels.players.grid_remove()
                root.grid_columnconfigure(2, weight=0, minsize=0)

        except Exception as e:
            print(f"[!] Error al ocultar jugadores: {e}")

    def _show_players_sections(self):
        """Muestra la sección de jugadores de ambos equipos y restaura las columnas."""
        try:
            root = self.scoreboard.root

            # Mostrar jugadores del equipo local
            if hasattr(self.scoreboard.home_team.labels, 'players'):
                self.scoreboard.home_team.labels.players.grid(
                    row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 15), pady=5
                )
                root.grid_columnconfigure(0, weight=3)

            # Mostrar jugadores del equipo visitante
            if hasattr(self.scoreboard.away_team.labels, 'players'):
                self.scoreboard.away_team.labels.players.grid(
                    row=0, column=2, rowspan=3, sticky="nsew", padx=(15, 0), pady=5
                )
                root.grid_columnconfigure(2, weight=3)

        except Exception as e:
            print(f"[!] Error al mostrar jugadores: {e}")

    def _hide_logos(self):
        """Oculta los logos de ambos equipos en modo compacto."""
        try:
            # Ocultar logo del equipo local
            if hasattr(self.scoreboard.labels.home_team, 'logo'):
                self.scoreboard.labels.home_team.logo.grid_remove()

            # Ocultar logo del equipo visitante
            if hasattr(self.scoreboard.labels.away_team, 'logo'):
                self.scoreboard.labels.away_team.logo.grid_remove()

        except Exception as e:
            print(f"[!] Error al ocultar logos: {e}")

    def _show_logos(self):
        """Muestra los logos de ambos equipos."""
        try:
            # Mostrar logo del equipo local
            if hasattr(self.scoreboard.labels.home_team, 'logo'):
                self.scoreboard.labels.home_team.logo.grid()

            # Mostrar logo del equipo visitante
            if hasattr(self.scoreboard.labels.away_team, 'logo'):
                self.scoreboard.labels.away_team.logo.grid()

        except Exception as e:
            print(f"[!] Error al mostrar logos: {e}")

    def _apply_compact_scale(self):
        """
        Aplica la escala compacta UNIFORME al 50% a TODOS los elementos del scoreboard.
        """
        if hasattr(self.scoreboard, 'modern_style'):
            scale = self.COMPACT_CONFIG['scale_factor']  # 0.50
            modern_style = self.scoreboard.modern_style

            # Aplicar escala general
            modern_style.scale_factor = scale

            # Actualizar TODOS los estilos al 50%
            self._update_all_styles_uniform(scale)

    def _apply_normal_scale(self):
        """Restaura la escala normal de los elementos del scoreboard."""
        if hasattr(self.scoreboard, 'modern_style'):
            self.scoreboard.modern_style.scale_factor = self.NORMAL_CONFIG['scale_factor']
            self.scoreboard.modern_style._update_scaled_styles()

    def _update_all_styles_uniform(self, scale):
        """
        Actualiza TODOS los estilos con la MISMA escala uniforme.

        Args:
            scale: Factor de escala uniforme para todos los elementos (ej: 0.50 = 50%)
        """
        modern_style = self.scoreboard.modern_style
        style = modern_style.style
        fonts = modern_style.FONTS
        sizes = modern_style.BASE_SIZES

        # Nombres de equipo
        style.configure("TeamName.TLabel",
                       font=(fonts['condensed'][0],
                            int(sizes['font_team_name'] * scale), 'bold'))

        # Puntaje
        style.configure("Score.TLabel",
                       font=(fonts['score'][0],
                            int(sizes['font_score'] * scale), 'bold'))

        # Reloj
        style.configure("Time.TLabel",
                       font=(fonts['digital'][0],
                            int(sizes['font_time'] * scale), 'bold'))

        style.configure("DigitalTime.TLabel",
                       font=(modern_style.digital_font_family,
                            int(sizes['font_time'] * scale), 'italic'))

        # Cuarto
        style.configure("Quarter.TLabel",
                       font=(fonts['display'][0],
                            int(sizes['font_quarter'] * scale), 'bold'))

        # Posesión
        style.configure("Possession.TLabel",
                       font=(fonts['display'][0],
                            int(sizes['font_possession_arrow'] * scale), 'bold'))

        style.configure("PossessionText.TLabel",
                       font=(fonts['condensed'][0],
                            int(sizes['font_possession_text'] * scale), 'bold'))

        # Labels generales
        style.configure("Info.TLabel",
                       font=(fonts['display'][0],
                            int(sizes['font_label'] * scale)))

        # Faltas de equipo
        style.configure("Fouls.TLabel",
                       font=(fonts['display'][0],
                            int(sizes.get('font_fouls', 28) * scale), 'bold'))

        # Bonus
        style.configure("Bonus.TLabel",
                       font=(fonts['condensed'][0],
                            int(sizes.get('font_bonus', 24) * scale), 'bold'))

        # Timeouts
        style.configure("Timeout.TLabel",
                       font=(fonts['display'][0],
                            int(sizes.get('font_timeout', 20) * scale), 'bold'))
