"""
Formateador de tiempo para el scoreboard con soporte para último minuto.
Cambia automáticamente de MM:SS a SS:ms cuando queda menos de 1 minuto.
"""


class TimeFormatter:
    """
    Gestiona el formato del tiempo y el estilo del borde según el tiempo restante.
    
    En el último minuto (< 60 segundos):
    - Formato: SS:ms (segundos y milésimas)
    - Borde: Rojo brillante
    
    Resto del tiempo:
    - Formato: MM:SS (minutos y segundos)
    - Borde: Blanco
    """
    
    # Constantes
    LAST_MINUTE_THRESHOLD = 60  # Segundos para activar formato especial
    
    # Colores de borde
    BORDER_COLOR_NORMAL = '#FFFFFF'      # Blanco (tiempo normal)
    BORDER_COLOR_LAST_MINUTE = '#FF0000'  # Rojo brillante (último minuto)
    
    def __init__(self):
        """Inicializa el formateador."""
        self.is_last_minute_mode = False
        self.last_seconds = None
    
    def format_time(self, total_seconds, milliseconds=0):
        """
        Formatea el tiempo según el modo actual.

        Args:
            total_seconds (int): Segundos totales restantes
            milliseconds (int): Milésimas de segundo (0-999)

        Returns:
            str: Tiempo formateado (MM:SS o SS.ms)
        """
        if total_seconds < self.LAST_MINUTE_THRESHOLD:
            # Último minuto: formato SS.ms (punto en lugar de dos puntos)
            self.is_last_minute_mode = True
            # Convertir milésimas a centésimas (2 dígitos) para mantener ancho fijo
            centiseconds = milliseconds // 10
            return f"{total_seconds:02d}.{centiseconds:02d}"
        else:
            # Tiempo normal: formato MM:SS
            self.is_last_minute_mode = False
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_border_color(self):
        """
        Retorna el color del borde según el modo actual.
        
        Returns:
            str: Color hexadecimal del borde
        """
        if self.is_last_minute_mode:
            return self.BORDER_COLOR_LAST_MINUTE
        else:
            return self.BORDER_COLOR_NORMAL
    
    def should_update_border(self, total_seconds):
        """
        Verifica si se debe actualizar el borde (cambio de modo).
        
        Args:
            total_seconds (int): Segundos totales restantes
            
        Returns:
            bool: True si cambió de modo, False si no
        """
        was_last_minute = self.is_last_minute_mode
        is_now_last_minute = total_seconds < self.LAST_MINUTE_THRESHOLD
        
        # Retornar True si cambió de modo
        return was_last_minute != is_now_last_minute
    
    def reset(self):
        """Reinicia el formateador al estado inicial (nuevo cuarto)."""
        self.is_last_minute_mode = False
        self.last_seconds = None
    
    def get_display_info(self, total_seconds, milliseconds=0):
        """
        Retorna toda la información necesaria para actualizar el display.
        
        Args:
            total_seconds (int): Segundos totales restantes
            milliseconds (int): Milésimas de segundo (0-999)
            
        Returns:
            dict: Información de display con:
                - 'text': Texto formateado del tiempo
                - 'border_color': Color del borde
                - 'is_last_minute': Si está en modo último minuto
                - 'should_update_border': Si se debe actualizar el borde
        """
        should_update = self.should_update_border(total_seconds)
        text = self.format_time(total_seconds, milliseconds)
        border_color = self.get_border_color()
        
        return {
            'text': text,
            'border_color': border_color,
            'is_last_minute': self.is_last_minute_mode,
            'should_update_border': should_update
        }

