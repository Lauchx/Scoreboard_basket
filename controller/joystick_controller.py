import pygame
import threading
import time

class JoystickController:
    """
    Controlador para manejar input de joystick/gamepad.

    Esta clase se encarga de:
    1. Detectar joysticks conectados
    2. Leer input de botones y ejes
    3. Mapear acciones a funciones del marcador
    """

    def __init__(self):
        """Inicializa pygame y configura el joystick"""
        # Inicializar pygame y el módulo de joystick
        pygame.init()
        pygame.joystick.init()

        # Variables de estado
        self.joystick = None
        self.is_running = False
        self.thread = None

        # Callback functions - aquí conectaremos con el marcador
        self.callbacks = {}

        print("🎮 JoystickController inicializado")

    def detect_joysticks(self):
        """
        Detecta y lista todos los joysticks conectados.
        Retorna una lista con información de los joysticks.
        """
        joystick_count = pygame.joystick.get_count()
        joysticks_info = []

        print(f"🔍 Buscando joysticks... Encontrados: {joystick_count}")

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick_info = {
                'id': i,
                'name': joystick.get_name(),
                'num_buttons': joystick.get_numbuttons(),
                'num_axes': joystick.get_numaxes(),
                'num_hats': joystick.get_numhats()
            }
            joysticks_info.append(joystick_info)
            print(f"  📱 Joystick {i}: {joystick_info['name']}")
            print(f"     Botones: {joystick_info['num_buttons']}")
            print(f"     Ejes: {joystick_info['num_axes']}")

        return joysticks_info

    def connect_joystick(self, joystick_id=0):
        """
        Conecta con un joystick específico.

        Args:
            joystick_id (int): ID del joystick a conectar (por defecto 0)

        Returns:
            bool: True si se conectó exitosamente, False si no
        """
        try:
            if pygame.joystick.get_count() == 0:
                print("❌ No hay joysticks conectados")
                return False

            if joystick_id >= pygame.joystick.get_count():
                print(f"❌ Joystick ID {joystick_id} no existe")
                return False

            # Conectar al joystick
            self.joystick = pygame.joystick.Joystick(joystick_id)
            self.joystick.init()

            print(f"✅ Conectado a: {self.joystick.get_name()}")
            print(f"   Botones: {self.joystick.get_numbuttons()}")
            print(f"   Ejes: {self.joystick.get_numaxes()}")

            return True

        except Exception as e:
            print(f"❌ Error conectando joystick: {e}")
            return False

    def disconnect_joystick(self):
        """Desconecta el joystick actual"""
        if self.joystick:
            self.joystick.quit()
            self.joystick = None
            print("🔌 Joystick desconectado")

    def is_connected(self):
        """Verifica si hay un joystick conectado"""
        return self.joystick is not None and self.joystick.get_init()

    def set_callback(self, action, callback_function):
        """
        Asigna una función callback a una acción específica.

        Args:
            action (str): Nombre de la acción (ej: 'home_add_point', 'start_timer')
            callback_function: Función a ejecutar cuando se presione el botón
        """
        self.callbacks[action] = callback_function
        print(f"📋 Callback asignado: {action}")

    def start_listening(self):
        """
        Inicia el hilo que escucha constantemente el input del joystick.
        Esto permite que el joystick funcione sin bloquear la interfaz.
        """
        if not self.is_connected():
            print("❌ No hay joystick conectado para escuchar")
            return False

        if self.is_running:
            print("⚠️ Ya se está escuchando el joystick")
            return False

        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("🎧 Iniciando escucha del joystick...")
        return True

    def stop_listening(self):
        """Para la escucha del joystick"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        print("🛑 Escucha del joystick detenida")

    def _listen_loop(self):
        """
        Bucle principal que escucha constantemente el input del joystick.
        Esta función corre en un hilo separado.
        """
        print("🔄 Bucle de escucha iniciado")

        # Variables para evitar spam de botones
        button_states = {}

        while self.is_running:
            try:
                # Procesar eventos de pygame
                pygame.event.pump()

                if not self.is_connected():
                    break

                # Leer estado de todos los botones
                for button_id in range(self.joystick.get_numbuttons()):
                    button_pressed = self.joystick.get_button(button_id)

                    # Solo actuar cuando se presiona el botón (no cuando se mantiene)
                    if button_pressed and not button_states.get(button_id, False):
                        self._handle_button_press(button_id)

                    button_states[button_id] = button_pressed

                # Leer ejes (sticks analógicos)
                self._handle_axes()

                # Leer D-pad (hat)
                self._handle_hat()

                # Pequeña pausa para no sobrecargar el CPU
                time.sleep(0.01)  # 100 FPS es más que suficiente

            except Exception as e:
                print(f"❌ Error en bucle de escucha: {e}")
                break

        print("🔄 Bucle de escucha terminado")

    def _handle_button_press(self, button_id):
        """
        Maneja cuando se presiona un botón específico.

        Args:
            button_id (int): ID del botón presionado
        """
        print(f"🔘 Botón presionado: {button_id}")

        # Mapeo de botones a acciones (esto lo configuraremos después)
        button_actions = self._get_button_mapping()

        if button_id in button_actions:
            action = button_actions[button_id]
            if action in self.callbacks:
                try:
                    self.callbacks[action]()
                    print(f"✅ Acción ejecutada: {action}")
                except Exception as e:
                    print(f"❌ Error ejecutando acción {action}: {e}")
            else:
                print(f"⚠️ No hay callback para la acción: {action}")
        else:
            print(f"⚠️ Botón {button_id} no mapeado")

    def _handle_axes(self):
        """
        Maneja los ejes analógicos (sticks).
        Por ahora solo detectamos, después podemos usar para navegación.
        """
        # Por ahora no implementamos acciones con sticks
        # Pero podríamos usarlos para cambiar valores rápidamente
        pass

    def _handle_hat(self):
        """
        Maneja el D-pad (cruceta direccional).
        Útil para navegación o acciones direccionales.
        """
        if self.joystick.get_numhats() > 0:
            hat = self.joystick.get_hat(0)  # Primer D-pad
            # hat devuelve (x, y) donde cada valor puede ser -1, 0, o 1
            # Por ejemplo: (0, 1) = arriba, (1, 0) = derecha, etc.

            # Por ahora solo detectamos, después implementaremos acciones
            if hat != (0, 0):  # Si se está presionando alguna dirección
                pass  # Implementaremos después

    def _get_button_mapping(self):
        """
        Retorna el mapeo de botones a acciones.
        Este mapeo se puede personalizar según el tipo de control.

        Returns:
            dict: Diccionario con button_id -> action_name
        """
        # Mapeo personalizado según los requerimientos del usuario:
        # Botón 5: +1 punto equipo visitante
        # Botón 4: +1 punto equipo local
        # Botón 2: -1 punto equipo local
        # Botón 3: -1 punto equipo visitante
        # Botón 7: iniciar tiempo
        # Botón 0: pausar tiempo
        # Botón 1: reanudar tiempo
        return {
            0: 'pause_timer',           # Pausar cronómetro
            1: 'resume_timer',          # Reanudar cronómetro
            2: 'home_subtract_point',   # -1 punto equipo local
            3: 'away_subtract_point',   # -1 punto equipo visitante
            4: 'home_add_point',        # +1 punto equipo local
            5: 'away_add_point',        # +1 punto equipo visitante
            7: 'start_timer',           # Iniciar cronómetro
        }

    def get_joystick_info(self):
        """
        Retorna información detallada del joystick conectado.
        Útil para debugging y configuración.
        """
        if not self.is_connected():
            return None

        return {
            'name': self.joystick.get_name(),
            'id': self.joystick.get_instance_id(),
            'num_buttons': self.joystick.get_numbuttons(),
            'num_axes': self.joystick.get_numaxes(),
            'num_hats': self.joystick.get_numhats(),
            'power_level': self.joystick.get_power_level() if hasattr(self.joystick, 'get_power_level') else 'Unknown'
        }

    def test_all_buttons(self):
        """
        Función de prueba que imprime cuando se presiona cualquier botón.
        Útil para identificar qué botón es cuál en tu control.
        """
        if not self.is_connected():
            print("❌ No hay joystick conectado")
            return

        print("🧪 MODO PRUEBA: Presiona cualquier botón (Ctrl+C para salir)")
        print("   Esto te ayudará a identificar qué número tiene cada botón")

        button_states = {}

        try:
            while True:
                pygame.event.pump()

                # Probar botones
                for button_id in range(self.joystick.get_numbuttons()):
                    button_pressed = self.joystick.get_button(button_id)

                    if button_pressed and not button_states.get(button_id, False):
                        print(f"🔘 BOTÓN {button_id} presionado")

                    button_states[button_id] = button_pressed

                # Probar D-pad
                if self.joystick.get_numhats() > 0:
                    hat = self.joystick.get_hat(0)
                    if hat != (0, 0):
                        direction = ""
                        if hat[1] == 1: direction += "ARRIBA "
                        if hat[1] == -1: direction += "ABAJO "
                        if hat[0] == 1: direction += "DERECHA "
                        if hat[0] == -1: direction += "IZQUIERDA "
                        print(f"🎯 D-PAD: {direction}")

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n🛑 Modo prueba terminado")

    def cleanup(self):
        """
        Limpia recursos y cierra conexiones.
        Llama esto antes de cerrar la aplicación.
        """
        print("🧹 Limpiando JoystickController...")
        self.stop_listening()
        self.disconnect_joystick()
        pygame.joystick.quit()
        pygame.quit()
        print("✅ JoystickController limpiado")

# Función de utilidad para crear y probar el controlador
def test_joystick_controller():
    """
    Función de prueba independiente para probar el JoystickController.
    Puedes ejecutar este archivo directamente para probar.
    """
    print("🎮 === PRUEBA DEL JOYSTICK CONTROLLER ===")

    # Crear controlador
    controller = JoystickController()

    # Detectar joysticks
    joysticks = controller.detect_joysticks()

    if not joysticks:
        print("❌ No se encontraron joysticks. Conecta un control y vuelve a intentar.")
        return

    # Conectar al primer joystick
    if controller.connect_joystick(0):
        print("\n📋 Información del joystick:")
        info = controller.get_joystick_info()
        for key, value in info.items():
            print(f"   {key}: {value}")

        print("\n🧪 Iniciando modo prueba...")
        print("   Presiona botones para ver sus números")
        print("   Presiona Ctrl+C para terminar")

        controller.test_all_buttons()

    # Limpiar
    controller.cleanup()

if __name__ == "__main__":
    test_joystick_controller()