from tkinter import messagebox
import pygame
import threading
import time
from model.joystick.joystick_types import AbstractButton, ControllerType
from model.joystick.button_mapping import ButtonMapping
from model.joystick.joystick_config import DEFAULT_SCOREBOARD_ACTIONS

class JoystickController:
    """
    Controlador para manejar input de joystick/gamepad.

    Esta clase se encarga de:
    1. Detectar joysticks conectados
    2. Leer input de botones y ejes
    3. Mapear acciones a funciones del marcador
    """

    def __init__(self, on_disconnect_callback):
        # Inicializar pygame y el módulo de joystick
        pygame.init()
        pygame.joystick.init()

        # Variables de estado
        self.joystick = None
        self.is_running = False
        self.thread = None

        # Callback functions - aquí conectaremos con el marcador
        self.callbacks = {}
        self.on_disconnect_callback = on_disconnect_callback

        # Sistema de mapeo abstracto de botones (inyección del modelo)
        self.button_mapping = ButtonMapping()

        # Configuración de acciones con botones abstractos
        self.action_config = DEFAULT_SCOREBOARD_ACTIONS.copy()

        print("JoystickController inicializado con sistema de mapeo abstracto")

    def detect_joysticks(self):
        """
        Detecta y lista todos los joysticks conectados.
        Retorna una lista con información de los joysticks.
        """
        self.joystick_count = pygame.joystick.get_count()
        joysticks_array_info = []

        for i in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick_info = {
                'id': i,
                'name': joystick.get_name(),
                'num_buttons': joystick.get_numbuttons(),
                'num_axes': joystick.get_numaxes(),
                'num_hats': joystick.get_numhats()
            }
            joysticks_array_info.append(joystick_info)

        return joysticks_array_info

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
                return False
            if joystick_id >= pygame.joystick.get_count():
                return False

            # Conectar al joystick
            self.joystick = pygame.joystick.Joystick(joystick_id)
            self.joystick.init()

            # Detectar automáticamente el tipo de controlador
            controller_name = self.joystick.get_name()
            detected_type = self._detect_controller_type(controller_name)
            self._set_controller_type(detected_type)

            print(f"✅ Conectado a: {controller_name}")
            print(f"   Tipo detectado: {detected_type.value}")
            print(f"   Botones: {self.joystick.get_numbuttons()}")
            print(f"   Ejes: {self.joystick.get_numaxes()}")

            return True

        except Exception as e:
            print(f"❌ Error conectando joystick: {e}")
            return False

    def disconnect_joystick(self):
        if self.joystick:
            self.joystick.quit()
            self.joystick = None

    def try_auto_connect(self):
        """
        Intenta conectar automáticamente al primer joystick disponible.
        Este método se usa para detectar joysticks que se conectaron después
        de iniciar la aplicación.

        Returns:
            bool: True si se conectó exitosamente, False si no
        """
        self.joystick_count = pygame.joystick.get_count()

        if self.joystick_count > 0:
            print(f"🔍 Detectados {self.joystick_count} joystick(s), intentando conectar al primero...")
            return self.connect_joystick(0)

        return False

    def refresh_joystick_detection(self):
        """
        Fuerza una detección de joysticks y actualiza el estado.
        Útil para llamar desde un botón de "Refrescar" en la UI.

        Returns:
            bool: True si se detectó y conectó un joystick, False si no
        """
        # Si ya hay un joystick conectado, primero lo desconectamos
        
        if self.is_connected():
            self.disconnect_joystick()
            if self.is_running:
                self.stop_listening()

        # Forzar a pygame que actualice la lista de joysticks
        pygame.joystick.quit()
        pygame.joystick.init()

        # Intentar conectar automáticamente
        return self.try_auto_connect()

    def is_connected(self):
        return self.joystick is not None and self.joystick.get_init()

    def set_callback(self, action, callback_function):
        """
        Asigna una función callback a una acción específica.
        Args:
            action (str): Nombre de la acción (ej: 'home_add_point', 'manage_timer')
            callback_function: Función a ejecutar cuando se presione el botón
        """
        self.callbacks[action] = callback_function
        print(f"📋 Callback asignado: {action}")

    def set_action_config(self, action_config: dict):
        """
        Establece la configuración de acciones con botones abstractos.

        Args:
            action_config (dict): Diccionario de acciones a botones abstractos
        """
        self.action_config = action_config.copy()
        return f"⚙️ Configuración de acciones actualizada: {len(action_config)} acciones"
        

    def set_controller_type(self, controller_type):
        """
        Establece manualmente el tipo de controlador.

        Args:
            controller_type: Tipo de controlador (ControllerType o string)
        """
        if isinstance(controller_type, str):
            controller_type = ControllerType(controller_type)

        self._set_controller_type(controller_type)
        print(f"🎮 Tipo de controlador establecido manualmente: {controller_type.value}")
    

    def start_listening(self, joystick_id=0):
        """
        Inicia el hilo que escucha constantemente el input del joystick.
        Esto permite que el joystick funcione sin bloquear la interfaz.
        """
        # Primero intentar conectar automáticamente si no hay joystick conectado
        if not self.is_connected():
           
            if self.try_auto_connect():
                print("🎮 Joystick conectado automáticamente")
            else:
                messagebox.showinfo("❌ No hay joystick conectado para escuchar")
                return False

        if self.is_running:
            messagebox.showinfo("⚠️ Ya se está escuchando el joystick")
            return False

        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("🎧 Iniciando escucha del joystick...")
        return True

    def stop_listening(self):
        """Para la escucha del joystick"""
        try:
          self.is_running = False
          if self.thread:
              current = threading.current_thread()
              if self.thread == current:
                  self.thread = None  # Solo limpiar la referencia
              else:
                  self.thread.join(timeout=1.0)
        except Exception as e:
          print(f"Error al cerrar thread: {type(e).__name__}: {e}")
          print(f"Thread actual: {threading.current_thread().name}")
          print(f"Thread a cerrar: {self.thread.name}")

    def get_available_buttons(self):
        """
        Obtiene los botones disponibles con sus nombres para mostrar.

        Returns:
            Dict[str, str]: Diccionario de botones abstractos y sus nombres
        """
        if self.joystick == None:
            return None
        else:
            return {btn.value: name for btn, name in self.button_mapping._get_available_buttons().items()}
        
    def get_joystick_info(self):
        """
        Retorna información detallada del joystick conectado.
        Útil para debugging y configuración.
        """
        if not self.is_connected():
            return None

        base_info = {
            'name': self.joystick.get_name(),
            'id': self.joystick.get_instance_id(),
            'num_buttons': self.joystick.get_numbuttons(),
            'num_axes': self.joystick.get_numaxes(),
            'num_hats': self.joystick.get_numhats(),
            'power_level': self.joystick.get_power_level() if hasattr(self.joystick, 'get_power_level') else 'Unknown'
        }

        # Agregar información del mapeador
        mapper_info = self.button_mapping._get_controller_info()
        base_info.update(mapper_info)

        return base_info
    
    def create_button_mapping(self):
        """
        Retorna el mapeo de botones físicos a acciones usando el sistema abstracto.

        Returns:
            dict: Diccionario con button_id -> action_name
        """
        # Crear mapeo usando el sistema abstracto
        physical_mapping = {}
        for action, abstract_button in self.action_config.items():
            physical_button = self.button_mapping._get_physical_button(abstract_button)
            if physical_button is not None:
                physical_mapping[physical_button] = action
        return physical_mapping
    
    def get_abstract_button_from_action(self, action:str):
        for action_config, abstract_btn in self.action_config.items():
            if action == action_config:
                return abstract_btn
    def get_display_name(self, abstract_button: AbstractButton) -> str:
        return self.button_mapping._get_display_name(abstract_button)
    
    def get_abstract_button(self, physical_button: int):
        return self.button_mapping._get_abstract_button(physical_button)
    # =======================================================================
    # MÉTODOS PRIVADOS DE LÓGICA (antes estaban en el modelo)
    # =======================================================================

    def _detect_controller_type(self, controller_name: str) -> ControllerType:
        """
        Detecta el tipo de controlador basado en el nombre del dispositivo.
        Lógica movida desde el modelo.

        Args:
            controller_name (str): Nombre del controlador detectado por pygame

        Returns:
            ControllerType: Tipo de controlador detectado
        """
        controller_name_lower = controller_name.lower()

        # Patrones comunes para Xbox
        xbox_patterns = ['xbox', 'xinput', 'microsoft']
        # Patrones comunes para PlayStation
        playstation_patterns = ['playstation', 'dualshock', 'dual sense', 'sony', 'ps3']

        if any(pattern in controller_name_lower for pattern in xbox_patterns):
            return ControllerType.XBOX
        elif any(pattern in controller_name_lower for pattern in playstation_patterns):
            return ControllerType.PLAYSTATION
        else:
            return ControllerType.UNKNOWN

    def _set_controller_type(self, controller_type: ControllerType):
        """
        Establece el tipo de controlador y actualiza el mapeo correspondiente.
        Lógica movida desde el modelo.

        Args:
            controller_type (ControllerType): Tipo de controlador a establecer
        """
        self.button_mapping.controller_type = controller_type
        self._update_current_mapping()

    def _update_current_mapping(self):
        """Actualiza el mapeo actual basado en el tipo de controlador.
        Lógica movida desde el modelo."""
        if self.button_mapping.controller_type in self.button_mapping.CONTROLLER_MAPPINGS:
            self.button_mapping.current_mapping = self.button_mapping.CONTROLLER_MAPPINGS[self.button_mapping.controller_type].copy()
        else:
            # Si no se reconoce el controlador, usar mapeo genérico (Xbox como default)
            self.button_mapping.current_mapping = self.button_mapping.CONTROLLER_MAPPINGS[ControllerType.XBOX].copy()

    def _check_joystick_connected(self):
        try:
          if not hasattr(self, 'joystick_count'):
            self.try_auto_connect()
          # Verificar si el dispositivo físico sigue existiendo
          current_count = pygame.joystick.get_count()
          if current_count < self.joystick_count:
            # Se desconectó un joystick
            raise pygame.error("Joystick desconectado")

          # Intentar acceder al índice actual
          pygame.joystick.Joystick(self.joystick.get_id())
          return True
        except (pygame.error, AttributeError) as e:
            messagebox.showinfo(f"❌ Error en el joystick", f"{e}")
            self.cleanup()
            self._clean_ui_control_panel()
            return False               

    def _listen_loop(self):
        """
        Bucle principal que escucha constantemente el input del joystick.
        Esta función corre en un hilo separado.
        """
        # Variables para evitar spam de botones
        button_states = {}

        while self.is_running:
            try:
                # Procesar eventos de pygame
                pygame.event.pump()

                if not self.is_connected():
                    break

                if not self._check_joystick_connected():
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
                # Leer D-pad (hat): Devolviendo su posición como una tupla de dos valores (x,y).
                self._handle_hat()
                # Pequeña pausa para no sobrecargar el CPU
                time.sleep(0.01)  # 100 FPS es más que suficiente

            except Exception as e:
                messagebox.showinfo(f"❌ Error en bucle de escucha: ", f"{e}")
                print( f"{e}")
                break

    def _handle_button_press(self, button_id):
        """
        Maneja cuando se presiona un botón específico.

        Args:
            button_id (int): ID del botón presionado
        """
        print(f"🔘 Botón presionado: {button_id}")

        # Mapeo de botones a acciones (esto lo configuraremos después)
        button_actions = self.create_button_mapping()

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
            hat = self.joystick.get_hat(0)  # Primer D-pad # hat devuelve (x, y) donde cada valor puede ser -1, 0, o 1

            if hat != (0, 0):  # Si se está presionando alguna dirección
                pass  # Implementaremos después
   
    def _clean_ui_control_panel(self):
        print(self.on_disconnect_callback())
        if self.on_disconnect_callback():
            self.on_disconnect_callback()
        else:
            messagebox.showinfo(f"❌ Error", "No se pudo actualizar el panel de control. Asegurese de tener conectado el joystick")

    def cleanup(self):
        """
        Limpia recursos y cierra conexiones.
        Llama esto antes de cerrar la aplicación.
        """
        self.stop_listening()
        self.disconnect_joystick()
        pygame.joystick.quit()
        pygame.quit()

# Función de utilidad para crear y probar el controlador


