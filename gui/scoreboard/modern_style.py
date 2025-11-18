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

    # 📁 RUTA A LA FUENTE DIGITAL-7 ITALIC
    DIGITAL_FONT_PATH = Path(__file__).parent.parent.parent / "assets" / "digital_7" / "digital-7 (italic).ttf"

    # 🎨 PALETA DE COLORES PROFESIONAL (NBA/FIBA Style)
    COLORS = {
        # Fondos
        'bg_primary': '#0A0E27',        # Azul oscuro casi negro (fondo principal)
        'bg_secondary': '#1a1f3a',      # Azul oscuro (paneles)
        'bg_center': '#0d1117',         # Negro azulado (panel central)
        'bg_team_home': '#1a0f0f',      # Rojo muy oscuro (equipo local)
        'bg_team_away': '#0f1a1a',      # Verde azulado oscuro (visitante)
        
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
        
        # Números y displays
        'display_time': '#00d9ff',      # Cian para el reloj
        'display_score': '#ffffff',     # Blanco para puntajes
        'display_glow': '#0088cc',      # Azul para efecto glow
        
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
    BASE_SIZES = {
        'font_team_name': 24,      # Reducido de 32 a 24 (25% más pequeño) para columna más compacta
        'font_score': 60,          # Reducido de 80 a 60 (25% más pequeño) para columna más compacta
        'font_time': 100,          # MANTENER GRANDE - No se reduce
        'font_quarter': 24,        # Reducido de 32 a 24 (25% más pequeño)
        'font_possession_arrow': 120,  # Reducido de 180 a 120 (33% más pequeño)
        'font_possession_text': 20,    # Reducido de 28 a 20 (29% más pequeño)
        'font_label': 16,          # Reducido de 20 a 16 (20% más pequeño)
        'font_players': 13,        # Reducido de 14 a 13 (ligeramente más pequeño)

        'padding_main': 15,        # Reducido de 25 a 15 (40% menos padding)
        'padding_team': 10,        # Reducido de 20 a 10 (50% menos padding)
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
        Carga la fuente Digital-7 Italic desde el archivo TTF.
        Usa múltiples métodos para máxima compatibilidad sin requerir permisos de administrador.

        Returns:
            str: Nombre de la familia de fuente cargada, o fallback si falla
        """
        try:
            # Verificar que el archivo existe
            if not self.DIGITAL_FONT_PATH.exists():
                print(f"[!] Advertencia: No se encontró la fuente en {self.DIGITAL_FONT_PATH}")
                return 'Consolas'  # Fallback

            font_path_str = str(self.DIGITAL_FONT_PATH.absolute())

            # Método 1: Verificar si la fuente Digital-7 ya está disponible
            # Verificar en la lista de fuentes del sistema
            try:
                available_fonts = tkfont.families()
                # Buscar variantes de Digital-7 en las fuentes disponibles
                digital_fonts = [f for f in available_fonts if 'digital' in f.lower() or 'Digital' in f]

                if digital_fonts:
                    # La fuente ya está disponible en el sistema
                    print(f"[OK] Fuente Digital-7 ya disponible en el sistema: {digital_fonts}")
                    return 'Digital-7 Italic'  # Retornar el nombre que usa ui_time_modern.py
                else:
                    # La fuente no está en la lista, intentar cargarla
                    print("[!] Fuente Digital-7 no encontrada en el sistema, intentando cargarla...")
            except Exception as e:
                print(f"[!] Error al verificar fuentes disponibles: {e}")

            # Método 2: Cargar con ctypes (Windows) - SIN SendMessageW para evitar permisos
            try:
                import ctypes
                from ctypes import wintypes

                # Cargar gdi32.dll
                gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

                # Definir la función AddFontResourceExW
                AddFontResourceEx = gdi32.AddFontResourceExW
                AddFontResourceEx.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID]
                AddFontResourceEx.restype = ctypes.c_int

                # FR_PRIVATE = 0x10 (fuente privada, no se instala permanentemente)
                FR_PRIVATE = 0x10

                # Cargar la fuente
                result = AddFontResourceEx(font_path_str, FR_PRIVATE, 0)

                if result > 0:
                    print(f"[OK] Fuente Digital-7 Italic cargada desde {self.DIGITAL_FONT_PATH.name}")

                    # NO usar SendMessageW - puede requerir permisos de administrador
                    # La fuente funcionará sin la notificación broadcast

                    # Guardar referencia para poder descargar la fuente al cerrar
                    self.loaded_font_path = font_path_str

                    return 'Digital-7 Italic'
                else:
                    print(f"[!] AddFontResourceEx retournó {result}, intentando método alternativo...")

            except Exception as e:
                print(f"[!] Error al cargar fuente con ctypes: {e}")
                print(f"   Esto puede ocurrir por permisos. Intentando método alternativo...")

            # Método 3: Intentar con pyglet como fallback
            try:
                from pyglet import font as pyglet_font  # type: ignore
                pyglet_font.add_file(font_path_str)
                print(f"[OK] Fuente Digital-7 Italic cargada con pyglet desde {self.DIGITAL_FONT_PATH.name}")
                return 'Digital-7 Italic'
            except ImportError:
                print(f"[!] pyglet no está instalado, saltando este método")
            except Exception as e:
                print(f"[!] Error al cargar fuente con pyglet: {e}")

            # Si todo falla, usar fallback
            print(f"[!] No se pudo cargar la fuente Digital-7, usando Consolas como fallback")
            print(f"   La aplicación funcionará normalmente con la fuente alternativa")
            return 'Consolas'

        except Exception as e:
            print(f"[!] Error general al cargar fuente Digital-7 Italic: {e}")
            print(f"   Usando fuente Consolas como alternativa")
            return 'Consolas'  # Fallback

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
        
        # Tamaño mínimo recomendado
        self.root.minsize(1000, 600)
    
    def _on_window_resize(self, event):
        """
        Callback para manejar el redimensionamiento de la ventana.
        Escala los elementos proporcionalmente.
        """
        # Solo procesar eventos de la ventana principal
        if event.widget != self.root:
            return
        
        # Calcular factor de escala basado en el ancho
        base_width = 1200  # Ancho de referencia
        current_width = event.width
        new_scale = current_width / base_width
        
        # Limitar el rango de escala
        new_scale = max(0.6, min(new_scale, 2.0))
        
        # Solo actualizar si hay cambio significativo
        if abs(new_scale - self.scale_factor) > 0.05:
            self.scale_factor = new_scale
            self._update_scaled_styles()
    
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
    
    def get_player_listbox_config(self):
        """
        Retorna la configuración de estilo para el Listbox de jugadores.
        Configurado para máxima visibilidad: texto blanco sobre fondo oscuro.

        Returns:
            dict: Configuración de estilo para tk.Listbox
        """
        return {
            'bg': self.COLORS['bg_secondary'],  # Fondo oscuro
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
        """Retorna el color para jugadores inactivos (blanco para visibilidad)."""
        return '#FFFFFF'  # Blanco en lugar de gris para mejor visibilidad

