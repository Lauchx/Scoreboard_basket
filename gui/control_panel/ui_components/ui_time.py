from tkinter import ttk
import pygame
from pathlib import Path

# Inicializar pygame mixer para sonidos
pygame.mixer.init()

# Ruta al archivo de bocina
BOCINA_PATH = Path(__file__).parent.parent.parent.parent / "assets" / "bocina.mp3"

def setup_time_panel(self, parent_frame):
    """Configura el panel de tiempo (cronómetro)"""
    self.frames.match.time = ttk.Frame(parent_frame, style="PanelTestTime.TFrame")
    self.frames.match.time.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    self.frames.match.time.grid_rowconfigure(0, weight=0)
    self.frames.match.time.grid_rowconfigure(1, weight=1)
    self.frames.match.time.grid_columnconfigure(0, weight=1)

    ttk.Label(self.frames.match.time, text="TIEMPO", style="PanelTestTimeTitle.TLabel", anchor="center").grid(row=0, column=0, sticky="ew", pady=(2, 0))

    self.match.time.label = ttk.Label(self.frames.match.time, text="00:00", style="PanelTestTime.TLabel", anchor="center")
    self.match.time.label.grid(row=1, column=0, sticky="nsew", pady=(0, 2))
    
    update_time_label(self)
    

def setup_timer_buttons(self, parent_frame):
    """Configura los botones de control del temporizador (Iniciar / Reiniciar)"""
    button_container = ttk.Frame(parent_frame, style="ControlPanel.Stack.TFrame")
    button_container.grid(row=0, column=1, sticky="n", padx=6, pady=6)

    buttons_inner = ttk.Frame(button_container, style="ControlPanel.Stack.TFrame")
    buttons_inner.pack(anchor="center", pady=10)

    # Frame superior para botones (pack)
    top_frame = ttk.Frame(buttons_inner, style="ControlPanel.Stack.TFrame")
    top_frame.pack(side="top", fill="x")

    self.button.timer = ttk.Button(top_frame, text="Iniciar", style="ControlPanel.Button.TButton", command=lambda: manage_timer(self))
    self.button.reset_timer = ttk.Button(top_frame, text="Reiniciar", style="ControlPanel.Button.TButton", command=lambda: reset_timer(self))

    self.button.timer.pack(side="top", pady=6)
    self.button.reset_timer.pack(side="top", pady=6)

    # Frame inferior para inputs de tiempo (grid)
    bottom_frame = ttk.Frame(buttons_inner, style="ControlPanel.Stack.TFrame")
    bottom_frame.pack(side="top", fill="x", pady=(10, 0))
    
    ui_for_change_time(self, bottom_frame)

def ui_for_change_time(self, parent):
    ttk.Label(parent, text="Minutos").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    self.match.entry.minutes_match_time = ttk.Entry(parent, width=5)
    self.match.entry.minutes_match_time.grid(row=0, column=1, sticky="nsew", padx=2)
    
    ttk.Label(parent, text="Segundos").grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
    self.match.entry.seconds_match_time = ttk.Entry(parent, width=5)
    self.match.entry.seconds_match_time.grid(row=0, column=3, sticky="nsew", padx=2)
    
    ttk.Button(parent, text="Actualizar", command=lambda: change_time(self)).grid(row=0, column=4, sticky="nsew", padx=5)

def start_timer(self):
    """
    Inicia el temporizador del partido.

    Comportamiento:
    - Cuando hay más de 60 segundos: actualiza cada 1 segundo
    - Cuando hay 60 segundos o menos: actualiza cada 10ms para mostrar centésimas
    - Cuando llega a 00:00: reproduce bocina y cambia fondo a rojo
    """
    time_left = self.match_state_controller.match_state.seconds_time_left

    # Inicializar milisegundos si no existe
    if not hasattr(self.match_state_controller.match_state, 'milliseconds_left'):
        self.match_state_controller.match_state.milliseconds_left = 0

    # Solo continuar si el timer está activo
    if not self.is_active_timer:
        return  # Timer pausado, no hacer nada

    # Verificar si hay tiempo restante
    has_time_left = time_left > 0 or self.match_state_controller.match_state.milliseconds_left > 0

    if has_time_left:
        if time_left < 60:
            # Último minuto: actualizar cada 10ms para mostrar centésimas
            self.match_state_controller.match_state.milliseconds_left -= 10

            if self.match_state_controller.match_state.milliseconds_left < 0:
                if time_left > 0:
                    self.match_state_controller.match_state.seconds_time_left -= 1
                    self.match_state_controller.match_state.milliseconds_left = 990
                else:
                    self.match_state_controller.match_state.milliseconds_left = 0

            milliseconds = self.match_state_controller.match_state.milliseconds_left
            self.scoreboard_window.update_time_labels(milliseconds)
            update_time_label(self)
            self.root.after(10, lambda: start_timer(self))
        else:
            # Tiempo normal: actualizar cada 1 segundo
            self.match_state_controller.match_state.seconds_time_left -= 1
            self.match_state_controller.match_state.milliseconds_left = 0
            self.scoreboard_window.update_time_labels(0)
            update_time_label(self)
            self.root.after(1000, lambda: start_timer(self))
    else:
        # TIEMPO LLEGÓ A 00.00 - Solo activar si no se ha triggereado previamente
        if not getattr(self, '_time_ended_triggered', False):
            print("🔔 TIEMPO TERMINADO - Reproduciendo bocina")
            on_time_ended(self)

def pause_resume_timer(self):
    self.is_active_timer = not self.is_active_timer

def change_text_button_timer(self, string="Reanudar"):
    text = "Pausar" if self.is_active_timer else string
    self.button.timer.config(text=text)

def change_time(self):
     min_text = self.match.entry.minutes_match_time.get().strip()
     sec_text = self.match.entry.seconds_match_time.get().strip()
     # Permitir formato mm:ss en el campo de minutos
     if ':' in min_text:
         parts = min_text.split(':')
         if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
             minutes = int(parts[0])
             seconds = int(parts[1])
         else:
             print("Formato inválido. Usa mm:ss o solo minutos.")
             return
     else:
         minutes = int(min_text) if min_text.isdigit() else 0
         seconds = int(sec_text) if sec_text.isdigit() else 0
     self.match_state_controller.match_state.seconds_match_time = (minutes * 60) + seconds
     self.match_state_controller.match_state.seconds_time_left = self.match_state_controller.match_state.seconds_match_time
     # Resetear milisegundos al cambiar el tiempo
     self.match_state_controller.match_state.milliseconds_left = 0
     self.scoreboard_window.update_time_labels(0)
     # Resetear bandera de tiempo terminado para permitir nuevo trigger
     self._time_ended_triggered = False

def reset_timer(self):
    self.match_state_controller.match_state.seconds_time_left = self.match_state_controller.match_state.seconds_match_time
    # Resetear milisegundos al reiniciar
    self.match_state_controller.match_state.milliseconds_left = 0
    if self.is_active_timer:
        pause_resume_timer(self)
        change_text_button_timer(self, 'Iniciar')
    self.scoreboard_window.update_time_labels(0)
    update_time_label(self)
    # Resetear bandera de tiempo terminado para permitir nuevo trigger
    self._time_ended_triggered = False

def manage_timer(self):
    if (self.is_active_timer is not None):
        pause_resume_timer(self)  
        if self.is_active_timer:
            start_timer(self)
    else:
        self.is_active_timer = True
        start_timer(self)
    change_text_button_timer(self)

def update_time_label(self):
    """Actualiza el label de tiempo con el formato MM:SS"""
    try:
        if hasattr(self.match.time, 'label') and self.match.time.label.winfo_exists():
            seconds_left = self.match_state_controller.match_state.seconds_time_left
            minutes = seconds_left // 60
            seconds = seconds_left % 60
            self.match.time.label.config(text=f"{minutes:02}:{seconds:02}")
    except Exception:
        pass


def on_time_ended(self):
    """
    Se ejecuta cuando el tiempo llega a 00:00.
    Reproduce la bocina y cambia el fondo del scoreboard a rojo por 3 segundos.
    """
    # Marcar que el tiempo terminó (para evitar re-trigger del rojo)
    self._time_ended_triggered = True

    # Reproducir bocina a volumen máximo
    try:
        if BOCINA_PATH.exists():
            pygame.mixer.music.load(str(BOCINA_PATH))
            pygame.mixer.music.set_volume(1.0)  # Volumen máximo
            pygame.mixer.music.play()
            print(f"[OK] Bocina reproducida desde {BOCINA_PATH}")
        else:
            print(f"[!] No se encontró el archivo de bocina en {BOCINA_PATH}")
    except Exception as e:
        print(f"[!] Error al reproducir bocina: {e}")

    # Cambiar fondo del scoreboard a rojo
    try:
        self.scoreboard_window.set_background_red()
        # Restaurar el fondo automáticamente después de 3 segundos
        self.root.after(3000, lambda: restore_scoreboard_background(self))
    except Exception as e:
        print(f"[!] Error al cambiar fondo a rojo: {e}")


def restore_scoreboard_background(self):
    """
    Restaura el fondo original del scoreboard.
    Se llama cuando se reinicia o actualiza el tiempo.
    """
    try:
        self.scoreboard_window.restore_background()
    except Exception as e:
        print(f"[!] Error al restaurar fondo: {e}")
