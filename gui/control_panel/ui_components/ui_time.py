from tkinter import ttk
from gui.control_panel.ui_components.ui_quarter import buttons_change_quarter
import time as time_module


def start_timer(self):
    """
    Temporizador principal del partido basado en tiempo real del sistema.
    Usa time.perf_counter() para precisión de milésimas.

    Sistema de tiempo real:
    - Guarda el timestamp de inicio del temporizador
    - Guarda el tiempo total restante al iniciar
    - Calcula el tiempo transcurrido en cada actualización
    - Actualiza cada 50ms en último minuto, cada 100ms en tiempo normal
    """
    if not self.is_active_timer:
        return

    # Obtener tiempo actual con alta precisión
    current_time = time_module.perf_counter()

    # Calcular tiempo transcurrido desde que se inició/reanudó
    elapsed = current_time - self._timer_start_time

    # Calcular tiempo restante real (en milisegundos)
    time_remaining_ms = self._timer_initial_ms - (elapsed * 1000)

    # Verificar si el tiempo llegó a cero
    if time_remaining_ms <= 0:
        # Tiempo terminado
        self.match_state_controller.match_state.seconds_time_left = 0
        self.scoreboard_window.update_time_labels(0)
        self.is_active_timer = False
        print("⏱️ Tiempo terminado - Fin del cuarto")
        return

    # Convertir a segundos y milésimas
    total_seconds = int(time_remaining_ms / 1000)
    milliseconds = int(time_remaining_ms % 1000)

    # Actualizar el estado
    self.match_state_controller.match_state.seconds_time_left = total_seconds

    # Determinar si estamos en el último minuto
    is_last_minute = total_seconds < 60

    # Actualizar display
    if is_last_minute:
        # Último minuto: mostrar milésimas
        self.scoreboard_window.update_time_labels(milliseconds)
        # Actualizar cada 50ms para suavidad
        update_interval = 50
    else:
        # Tiempo normal: mostrar solo segundos
        self.scoreboard_window.update_time_labels(0)
        # Actualizar cada 100ms (suficiente para segundos)
        update_interval = 100

    # Programar siguiente actualización
    self.root.after(update_interval, lambda: start_timer(self))


def pause_resume_timer(self):
    """
    Pausa o reanuda el temporizador.
    Al pausar: guarda el tiempo restante exacto.
    Al reanudar: reinicia el contador desde el tiempo guardado.
    """
    if self.is_active_timer:
        # PAUSAR: guardar el tiempo restante exacto
        if hasattr(self, '_timer_start_time'):
            current_time = time_module.perf_counter()
            elapsed = current_time - self._timer_start_time
            time_remaining_ms = self._timer_initial_ms - (elapsed * 1000)

            # Guardar el tiempo restante para cuando se reanude
            self._paused_time_ms = max(0, time_remaining_ms)

            print(f"⏸️ Pausado en: {time_remaining_ms/1000:.3f} segundos")

        self.is_active_timer = False
    else:
        # REANUDAR: iniciar desde el tiempo guardado
        if hasattr(self, '_paused_time_ms'):
            # Reanudar desde el tiempo pausado
            self._timer_initial_ms = self._paused_time_ms
        else:
            # Primera vez que se inicia
            total_seconds = self.match_state_controller.match_state.seconds_time_left
            self._timer_initial_ms = total_seconds * 1000

        # Reiniciar el timestamp de inicio
        self._timer_start_time = time_module.perf_counter()

        self.is_active_timer = True

        print(f"▶️ Reanudado desde: {self._timer_initial_ms/1000:.3f} segundos")

        # Iniciar el loop del temporizador
        start_timer(self)

def change_text_button_timer(self, string="Reanudar"):
    text = "Pausar" if self.is_active_timer else string
    self.button.timer.config(text=text)


def reset_timer(self):
    """
    Reinicia el temporizador al tiempo configurado.
    Limpia todas las variables de tiempo real.
    """
    # Pausar si está activo
    if self.is_active_timer:
        self.is_active_timer = False

    # Reiniciar tiempo al valor configurado
    self.match_state_controller.match_state.seconds_time_left = self.match_state_controller.match_state.seconds_match_time

    # Limpiar variables del temporizador de tiempo real
    if hasattr(self, '_timer_start_time'):
        delattr(self, '_timer_start_time')
    if hasattr(self, '_timer_initial_ms'):
        delattr(self, '_timer_initial_ms')
    if hasattr(self, '_paused_time_ms'):
        delattr(self, '_paused_time_ms')

    # Reiniciar el formateador de tiempo (volver a formato normal)
    self.scoreboard_window.time_formatter.reset()

    # Actualizar display
    self.scoreboard_window.update_time_labels(0)

    # Cambiar texto del botón
    change_text_button_timer(self, 'Iniciar')

    print("🔄 Temporizador reiniciado")


def manage_timer(self):
    """
    Gestiona el inicio/pausa del temporizador con debounce.
    """
    import time

    # Debounce de 500ms para evitar doble click
    if time.time() - self.last_timer_button_time < 0.5:
        return

    self.last_timer_button_time = time.time()

    # Pausar/Reanudar
    pause_resume_timer(self)

    # Cambiar texto del botón
    change_text_button_timer(self)
            

def setup_ui_time(self):
    print(self)
    self.last_timer_button_time = 0
    ttk.Label(self.frames.match.time, text="Minutos").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    self.match.entry.minutes_match_time = ttk.Entry(self.frames.match.time)
    self.match.entry.minutes_match_time.grid(row=1, column=1,sticky="nsew")
    ttk.Label(self.frames.match.time, text="Segundos").grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    self.match.entry.seconds_match_time = ttk.Entry(self.frames.match.time)
    self.match.entry.seconds_match_time.grid(row=1, column=3, sticky="nsew")
    ttk.Button(self.frames.match.time, text="Actualizar tiempo", command=lambda: change_time(self)).grid(row=1, column=4,sticky="nsew")

def change_time(self):
    """
    Cambia el tiempo del partido.
    Limpia las variables del temporizador de tiempo real.
    """
    minutes = int(self.match.entry.minutes_match_time.get())
    seconds = int(self.match.entry.seconds_match_time.get())

    # Actualizar tiempo configurado
    self.match_state_controller.match_state.seconds_match_time = (minutes * 60) + seconds
    self.match_state_controller.match_state.seconds_time_left = self.match_state_controller.match_state.seconds_match_time

    # Limpiar variables del temporizador de tiempo real
    if hasattr(self, '_timer_start_time'):
        delattr(self, '_timer_start_time')
    if hasattr(self, '_timer_initial_ms'):
        delattr(self, '_timer_initial_ms')
    if hasattr(self, '_paused_time_ms'):
        delattr(self, '_paused_time_ms')

    # Reiniciar el formateador de tiempo cuando se cambia el tiempo
    self.scoreboard_window.time_formatter.reset()

    # Actualizar display
    self.scoreboard_window.update_time_labels(0)

    print(f"⏱️ Tiempo actualizado a: {minutes}:{seconds:02d}")

def setup_ui_control_time_match(self):
    self.frames.match.time = ttk.LabelFrame(self.frames.match, text="Tiempo",)
    # Colocar en row=2 (debajo de timeouts en row=1 y botones de puntos en row=0)
    self.frames.match.time.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew", columnspan=2)
    buttons_change_quarter(self)
    setup_ui_time(self)

def buttons_for_match_time(self):
    self.button.timer = ttk.Button(self.frames.match.time, text="Iniciar", command=lambda: manage_timer(self))
    self.button.timer.grid(row=1, column=5)
    self.button.reset_timer = ttk.Button(self.frames.match.time, text="Reset", command=lambda: reset_timer(self))
    self.button.reset_timer.grid(row=1, column=6)
