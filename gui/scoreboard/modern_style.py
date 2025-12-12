"""
Módulo de diseño visual moderno para el scoreboard de básquet.
Estilo profesional tipo NBA/FIBA con diseño responsive y efectos digitales.

Este módulo NO altera la lógica del scoreboard, solo mejora su apariencia visual.
"""

from tkinter import ttk, font as tkfont
import tkinter as tk
import os
from pathlib import Path


class ScoreboardModernStyle:
    """
    Clase que aplica un diseño visual moderno y profesional al scoreboard.
    Inspirado en tableros digitales de NBA/FIBA con efectos tipo display LED.
    """

    # 📁 RUTAS A LAS FUENTES DIGITAL-7
    DIGITAL_FONT_PATH = Path(__file__).parent.parent.parent / "assets" / "digital_7" / "digital-7 (italic).ttf"
    DIGITAL_MONO_FONT_PATH = Path(__file__).parent.parent.parent / "assets" / "digital_7" / "digital-7 (mono).ttf"

    # 🎨 PALETA DE COLORES PROFESIONAL (NBA/FIBA Style)
    COLORS = {
        # Fondos
        'bg_primary': '#0A0E27',        # Azul oscuro casi negro (fondo principal)
        'bg_secondary': '#1a1f3a',      # Azul oscuro (paneles)
        'bg_center': '#0d1117',         # Negro azulado (panel central)
        'bg_team_home': '#1a1a2e',      # Azul oscuro (equipo local) - mismo que visitante
        'bg_team_away': '#1a1a2e',      # Azul oscuro (visitante) - mismo que local

        # Fondos de secciones específicas (configurables)
        'bg_quarter': '#0d1117',        # Fondo del sector de cuarto
        'bg_fouls_bonus': '#0d1117',    # Fondo del sector de faltas y BONUS
        'bg_score': '#1a1f3a',          # Fondo del sector de puntajes
        'bg_team_name': '#1a1a2e',      # Fondo del sector de nombres de equipo
        'bg_logo': '#1a1f3a',           # Fondo del sector de logos
        'bg_players': '#1a1f3a',        # Fondo del sector de jugadores

        # Acentos y textos
        'accent_neon': '#00ff41',       # Verde neón (posesión, activos)
        'accent_cyan': '#00d9ff',       # Cian brillante (tiempo, detalles)
        'accent_red': '#ff0844',        # Rojo neón (alertas, home)
        'accent_orange': '#ff6b35',     # Naranja (cuarto, detalles)
        'accent_yellow': '#ffd700',     # Dorado (highlights)

        # Textos
        'text_primary': '#ffffff',      # Blanco puro (textos principales)
        'text_secondary': '#b8c5d6',    # Gris azulado claro (textos secundarios)
        'text_dim': '#6b7a8f',          # Gris medio (textos apagados)
        'text_bonus': '#ffffff',        # Blanco para texto BONUS (configurable)

        # Números y displays
        'display_time': '#00d9ff',      # Cian para el reloj
        'display_score': '#ffffff',     # Blanco para puntajes
        'display_glow': '#0088cc',      # Azul para efecto glow
        'display_fouls': '#ff6b35',     # Naranja para números de faltas (configurable)
        'display_quarter': '#ff6b35',   # Naranja para número de cuarto (configurable)

        # Bordes y efectos
        'border_light': '#2d3748',      # Borde sutil
        'border_bright': '#4a5568',     # Borde más visible
        'shadow': '#000000',            # Sombra

        # Timeouts (tiempos muertos)
        'timeout_available': '#00FF00',  # Verde brillante (timeout disponible y permitido)
        'timeout_used': '#FF0000',       # Rojo brillante (timeout ya usado)
        'timeout_not_allowed': '#808080',  # Gris (timeout no permitido en este periodo)
        'bg_team_info': '#1a1a2e',       # Fondo para info de equipo
    }
    
    # 📏 TAMAÑOS BASE (se escalan proporcionalmente)
    # Reducidos para dar más espacio horizontal a las columnas de jugadores
    # Columnas de info de equipo reducidas 5% adicional para permitir achicar ventana
    BASE_SIZES = {
        'font_team_name': 22,      # Reducido de 24 a 22 (5% más pequeño) para columna más compacta
        'font_score': 76,          # Reducido de 80 a 76 (5% más pequeño)
        'font_time': 100,          # MANTENER GRANDE - No se reduce (privilegiar tiempo)
        'font_quarter': 24,        # Reducido de 32 a 24 (25% más pequeño)
        'font_possession_arrow': 50,  # Proporcional a BONUS, visible desde lejos
        'font_possession_text': 20,    # Reducido de 28 a 20 (29% más pequeño)
        'font_label': 16,          # Reducido de 20 a 16 (20% más pequeño)
        'font_players': 13,        # Reducido de 14 a 13 (ligeramente más pequeño)

        'padding_main': 15,        # Reducido de 25 a 15 (40% menos padding)
        'padding_team': 8,         # Reducido de 10 a 8 (20% menos padding)
        'padding_center': 10,      # Reducido de 15 a 10 (33% menos padding)
        'border_width': 2,         # Reducido de 3 a 2 (más delgado)
        'time_border_width': 2,    # Borde para el reloj (mantener)
        'score_border_width': 2,   # Borde para los puntajes (mantener)
    }
    
    # 🔤 FUENTES (con fallbacks profesionales)
    FONTS = {
        # Fuentes digitales profesionales tipo 7 segmentos (con múltiples fallbacks)
        # Orbitron es una fuente moderna tipo digital que viene con Windows 10+
        'digital': ('Orbitron', 'Consolas', 'Courier New', 'monospace'),

        # Fuentes para números grandes (puntajes)
        'score': ('Impact', 'Arial Black', 'Helvetica', 'bold'),

        # Fuentes para textos
        'display': ('Segoe UI', 'Roboto', 'Arial', 'Helvetica', 'sans-serif'),
        'condensed': ('Segoe UI Semibold', 'Arial Narrow', 'Arial', 'sans-serif'),
    }
    
    def __init__(self, root):
        """
        Inicializa el sistema de estilos modernos.

        Args:
            root: Ventana raíz del scoreboard
        """
        self.root = root
        self.style = ttk.Style()
        self.scale_factor = 1.0

        # Cargar fuente Digital-7 Italic personalizada
        self.digital_font_family = self._load_digital_font()

        # Configurar tema base
        self._setup_theme()

        # Aplicar estilos ttk
        self._apply_ttk_styles()

        # Configurar responsive
        self._setup_responsive()

    def _load_digital_font(self):
        """
        Carga las fuentes Digital-7 (Italic y Mono) desde los archivos TTF.
        La fuente Mono es monoespaciada y evita que el reloj "salte".

        Returns:
            str: Nombre de la familia de fuente cargada, o fallback si falla
        """
        try:
            import ctypes
            from ctypes import wintypes

            # Cargar gdi32.dll
            gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)
            AddFontResourceEx = gdi32.AddFontResourceExW
            AddFontResourceEx.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID]
            AddFontResourceEx.restype = ctypes.c_int
            FR_PRIVATE = 0x10  # Fuente privada, no se instala permanentemente

            fonts_loaded = []

            # Cargar fuente Italic
            if self.DIGITAL_FONT_PATH.exists():
                result = AddFontResourceEx(str(self.DIGITAL_FONT_PATH.absolute()), FR_PRIVATE, 0)
                if result > 0:
                    fonts_loaded.append('Digital-7 Italic')
                    print(f"[OK] Fuente Digital-7 Italic cargada desde {self.DIGITAL_FONT_PATH.name}")

            # Cargar fuente Mono (monoespaciada - para el reloj)
            if self.DIGITAL_MONO_FONT_PATH.exists():
                result = AddFontResourceEx(str(self.DIGITAL_MONO_FONT_PATH.absolute()), FR_PRIVATE, 0)
                if result > 0:
                    fonts_loaded.append('Digital-7 Mono')
                    print(f"[OK] Fuente Digital-7 Mono cargada desde {self.DIGITAL_MONO_FONT_PATH.name}")

            if fonts_loaded:
                return 'Digital-7 Italic'
            else:
                print(f"[!] No se pudieron cargar las fuentes Digital-7, usando Consolas")
                return 'Consolas'

        except Exception as e:
            print(f"[!] Error al cargar fuentes Digital-7: {e}")
            print(f"   Usando fuente Consolas como alternativa")
            return 'Consolas'

    def _setup_theme(self):
        """Configura el tema base del scoreboard."""
        # Usar tema clam como base (más personalizable)
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        
        # Configurar colores del tema
        self.style.configure('.', 
                           background=self.COLORS['bg_primary'],
                           foreground=self.COLORS['text_primary'],
                           bordercolor=self.COLORS['border_light'],
                           darkcolor=self.COLORS['bg_secondary'],
                           lightcolor=self.COLORS['border_bright'])
    
    def _apply_ttk_styles(self):
        """Aplica todos los estilos ttk personalizados."""
        
        # ═══════════════════════════════════════════════════════════
        # FRAMES - Contenedores principales
        # ═══════════════════════════════════════════════════════════
        
        # Frame del equipo local (HOME)
        self.style.configure("HomeTeam.TFrame",
                           background=self.COLORS['bg_team_home'],
                           relief='flat',
                           borderwidth=self.BASE_SIZES['border_width'])
        
        # Frame del equipo visitante (AWAY)
        self.style.configure("AwayTeam.TFrame",
                           background=self.COLORS['bg_team_away'],
                           relief='flat',
                           borderwidth=self.BASE_SIZES['border_width'])
        
        # Frame central (tiempo, posesión, cuarto)
        self.style.configure("CenterPanel.TFrame",
                           background=self.COLORS['bg_center'],
                           relief='flat',
                           borderwidth=self.BASE_SIZES['border_width'])
        
        # ═══════════════════════════════════════════════════════════
        # LABELS - Textos y displays
        # ═══════════════════════════════════════════════════════════
        
        # Nombre del equipo - TEXTO BLANCO sobre fondo oscuro para máxima visibilidad
        self.style.configure("TeamName.TLabel",
                           font=(self.FONTS['condensed'][0], self.BASE_SIZES['font_team_name'], 'bold'),
                           foreground='#FFFFFF',  # Blanco puro para máximo contraste
                           background=self.COLORS['bg_secondary'],
                           anchor='center',
                           padding=(10, 5))

        # Puntaje (números grandes) - BLANCO sobre fondo oscuro
        self.style.configure("Score.TLabel",
                           font=(self.FONTS['score'][0], self.BASE_SIZES['font_score'], 'bold'),
                           foreground='#FFFFFF',  # Blanco puro para máximo contraste
                           background=self.COLORS['bg_secondary'],
                           anchor='center')

        # Reloj/Tiempo (estilo digital profesional) - CIAN BRILLANTE sobre fondo oscuro
        self.style.configure("Time.TLabel",
                           font=(self.FONTS['digital'][0], self.BASE_SIZES['font_time'], 'bold'),
                           foreground=self.COLORS['display_time'],  # Cian brillante
                           background=self.COLORS['bg_center'],
                           anchor='center',
                           padding=(15, 10))

        # Reloj digital con estilo mejorado usando Digital-7 Italic
        self.style.configure("DigitalTime.TLabel",
                           font=(self.digital_font_family, self.BASE_SIZES['font_time'], 'italic'),
                           foreground=self.COLORS['display_time'],  # Cian brillante
                           background=self.COLORS['bg_center'],
                           anchor='center',
                           padding=(20, 15),
                           relief='flat')

        # Cuarto/Period - NARANJA BRILLANTE sobre fondo oscuro
        self.style.configure("Quarter.TLabel",
                           font=(self.FONTS['display'][0], self.BASE_SIZES['font_quarter'], 'bold'),
                           foreground=self.COLORS['accent_orange'],  # Naranja brillante
                           background=self.COLORS['bg_center'],
                           anchor='center')

        # Flecha de posesión - VERDE NEÓN sobre fondo oscuro
        self.style.configure("Possession.TLabel",
                           font=(self.FONTS['display'][0], self.BASE_SIZES['font_possession_arrow'], 'bold'),
                           foreground=self.COLORS['accent_neon'],  # Verde neón
                           background=self.COLORS['bg_center'],
                           anchor='center')

        # Texto "POSESION" - BLANCO sobre fondo oscuro
        self.style.configure("PossessionText.TLabel",
                           font=(self.FONTS['condensed'][0], self.BASE_SIZES['font_possession_text'], 'bold'),
                           foreground='#FFFFFF',  # Blanco puro para máximo contraste
                           background=self.COLORS['bg_center'],
                           anchor='center')

        # Labels generales - BLANCO sobre fondo oscuro
        self.style.configure("Info.TLabel",
                           font=(self.FONTS['display'][0], self.BASE_SIZES['font_label']),
                           foreground='#FFFFFF',  # Blanco puro para máximo contraste
                           background=self.COLORS['bg_secondary'])
    
    def _setup_responsive(self):
        """Configura el sistema responsive para redimensionamiento."""
        # Bind para detectar cambios de tamaño
        self.root.bind('<Configure>', self._on_window_resize)

        # Tamaño mínimo muy reducido para permitir modo compacto
        self.root.minsize(350, 220)

        # Guardar referencia al scoreboard (se asignará después)
        self.scoreboard_instance = None

    def set_scoreboard_instance(self, scoreboard):
        """Guarda referencia al scoreboard para actualizar widgets dinámicamente."""
        self.scoreboard_instance = scoreboard

    def _on_window_resize(self, event):
        """
        Callback para manejar el redimensionamiento de la ventana.
        Escala TODOS los elementos proporcionalmente.
        """
        # Solo procesar eventos de la ventana principal
        if event.widget != self.root:
            return

        # Calcular factor de escala basado en el ancho
        base_width = 1200  # Ancho de referencia
        current_width = event.width
        new_scale = current_width / base_width

        # Permitir escala muy pequeña (hasta 30%) para modo compacto
        new_scale = max(0.30, min(new_scale, 2.0))

        # Solo actualizar si hay cambio significativo (reducido threshold)
        if abs(new_scale - self.scale_factor) > 0.02:
            self.scale_factor = new_scale
            self._update_scaled_styles()
            self._update_dynamic_widgets()
    
    def _update_scaled_styles(self):
        """Actualiza los tamaños de fuente según el factor de escala."""
        scale = self.scale_factor

        # Actualizar fuentes de los estilos
        self.style.configure("TeamName.TLabel",
                           font=(self.FONTS['condensed'][0],
                                int(self.BASE_SIZES['font_team_name'] * scale), 'bold'))

        self.style.configure("Score.TLabel",
                           font=(self.FONTS['score'][0],
                                int(self.BASE_SIZES['font_score'] * scale), 'bold'))

        self.style.configure("Time.TLabel",
                           font=(self.FONTS['digital'][0],
                                int(self.BASE_SIZES['font_time'] * scale), 'bold'))

        self.style.configure("DigitalTime.TLabel",
                           font=(self.digital_font_family,
                                int(self.BASE_SIZES['font_time'] * scale), 'italic'))

        self.style.configure("Quarter.TLabel",
                           font=(self.FONTS['display'][0],
                                int(self.BASE_SIZES['font_quarter'] * scale), 'bold'))

        self.style.configure("Possession.TLabel",
                           font=(self.FONTS['display'][0],
                                int(self.BASE_SIZES['font_possession_arrow'] * scale), 'bold'))

        self.style.configure("PossessionText.TLabel",
                           font=(self.FONTS['condensed'][0],
                                int(self.BASE_SIZES['font_possession_text'] * scale), 'bold'))

        self.style.configure("Info.TLabel",
                           font=(self.FONTS['display'][0],
                                int(self.BASE_SIZES['font_label'] * scale)))

        # Estilos adicionales para faltas y bonus
        self.style.configure("Fouls.TLabel",
                           font=(self.FONTS['display'][0],
                                int(self.BASE_SIZES.get('font_fouls', 28) * scale), 'bold'))

        self.style.configure("Bonus.TLabel",
                           font=(self.FONTS['condensed'][0],
                                int(self.BASE_SIZES.get('font_bonus', 24) * scale), 'bold'))

    def _update_dynamic_widgets(self):
        """
        Actualiza widgets dinámicos que usan tk.Label (no ttk) como el reloj, puntajes, faltas.
        Estos requieren actualización directa de la propiedad font.

        PRIORIDAD DE ESCALADO (mínimos más altos = más visibles al achicar):
        - ALTA: Tiempo, Puntajes, Nombres de equipos
        - BAJA: Faltas, Cuarto (se achican más)
        """
        if self.scoreboard_instance is None:
            return

        scale = self.scale_factor
        sb = self.scoreboard_instance

        try:
            # ═══════════════════════════════════════════════════════════
            # RELOJ (tk.Label con Digital-7 Mono) - PRIORIDAD ALTA
            # Mínimo 40px para mantener buena legibilidad
            # ═══════════════════════════════════════════════════════════
            if hasattr(sb, 'match') and hasattr(sb.match, 'labels') and hasattr(sb.match.labels, 'time'):
                time_label = sb.match.labels.time
                font_size = int(self.BASE_SIZES['font_time'] * scale)
                font_size = max(40, font_size)  # Mínimo ALTO para prioridad
                time_label.config(font=('Digital-7 Mono', font_size))

            # ═══════════════════════════════════════════════════════════
            # PUNTAJES DE EQUIPOS (tk.Label) - PRIORIDAD ALTA
            # Mínimo 32px para puntajes, 14px para nombres
            # ═══════════════════════════════════════════════════════════
            for team_attr in ['home_team', 'away_team']:
                team_ns = getattr(sb, team_attr, None)
                if team_ns and hasattr(team_ns, 'labels'):
                    labels = team_ns.labels

                    # Actualizar puntaje - PRIORIDAD ALTA
                    if hasattr(labels, 'points') and isinstance(labels.points, tk.Label):
                        font_size = int(self.BASE_SIZES['font_score'] * scale)
                        font_size = max(32, font_size)  # Mínimo ALTO
                        labels.points.config(font=(self.FONTS['score'][0], font_size, 'bold'))

                    # Actualizar nombre del equipo - PRIORIDAD ALTA
                    if hasattr(labels, 'name') and isinstance(labels.name, tk.Label):
                        font_size = int(self.BASE_SIZES['font_team_name'] * scale)
                        font_size = max(14, font_size)  # Mínimo ALTO
                        labels.name.config(font=('Arial Narrow', font_size, 'bold'))

            # ═══════════════════════════════════════════════════════════
            # FALTAS (tk.Label) - PRIORIDAD BAJA
            # Mínimo 10px para contadores
            # ═══════════════════════════════════════════════════════════
            if hasattr(sb.match.labels, 'fouls'):
                fouls = sb.match.labels.fouls
                font_size_counter = int(70 * scale)  # 70 es el tamaño base de faltas
                font_size_counter = max(10, font_size_counter)  # Mínimo BAJO

                for team in ['home', 'away']:
                    team_fouls = getattr(fouls, team, None)
                    if team_fouls and hasattr(team_fouls, 'counter') and isinstance(team_fouls.counter, tk.Label):
                        team_fouls.counter.config(font=(self.FONTS['display'][0], font_size_counter, 'bold'))

            # ═══════════════════════════════════════════════════════════
            # CUARTO (tk.Label) - PRIORIDAD BAJA
            # Mínimo 8px para número, 6px para texto
            # ═══════════════════════════════════════════════════════════
            # Número del cuarto
            if hasattr(sb.match.labels, 'quarter_number') and isinstance(sb.match.labels.quarter_number, tk.Label):
                font_size = int(self.BASE_SIZES['font_quarter'] * scale * 2)
                font_size = max(8, font_size)  # Mínimo BAJO
                sb.match.labels.quarter_number.config(font=(self.FONTS['display'][0], font_size, 'bold'))

            # Texto "cuarto"
            if hasattr(sb.match.labels, 'quarter_text') and isinstance(sb.match.labels.quarter_text, tk.Label):
                font_size = int(self.BASE_SIZES['font_label'] * scale)
                font_size = max(6, font_size)  # Mínimo MUY BAJO
                sb.match.labels.quarter_text.config(font=(self.FONTS['display'][0], font_size))

        except Exception as e:
            print(f"[!] Error actualizando widgets dinámicos: {e}")

    def get_player_listbox_config(self):
        """
        Retorna la configuración de estilo para el Listbox de jugadores.
        Configurado para máxima visibilidad: texto blanco sobre fondo oscuro.

        Returns:
            dict: Configuración de estilo para tk.Listbox
        """
        return {
            'bg': self.COLORS['bg_players'],  # Fondo configurable del sector de jugadores
            'fg': '#FFFFFF',  # Texto BLANCO para máximo contraste
            'font': (self.FONTS['display'][0],
                    int(self.BASE_SIZES['font_players'] * self.scale_factor)),
            'selectbackground': self.COLORS['accent_cyan'],  # Fondo de selección cian
            'selectforeground': '#000000',  # Texto negro cuando está seleccionado
            'borderwidth': 0,
            'highlightthickness': 1,
            'highlightbackground': self.COLORS['border_light'],
            'highlightcolor': self.COLORS['accent_cyan'],
            'activestyle': 'none'
        }

    def get_active_player_color(self):
        """Retorna el color para jugadores activos (verde neón brillante)."""
        return self.COLORS['accent_neon']  # Verde neón para jugadores en cancha

    def get_inactive_player_color(self):
        """Retorna el color para jugadores inactivos (configurable desde la pestaña Configuración)."""
        return self.COLORS['text_dim']  # Color configurable para jugadores en el banco

