import tkinter as tk
from tkinter import ttk, messagebox
import threading
from model.joystick_types import ControllerType, AbstractButton
from model.joystick_config import DEFAULT_SCOREBOARD_ACTIONS

def setup_joystick_ui(control_panel):
    """
    Configura la interfaz de usuario para el control del joystick.
    
    Args:
        control_panel: Instancia de Gui_control_panel
    """
    # Crear frame para joystick en el notebook
    control_panel.frames.joystick = ttk.Frame(control_panel.notebook)
    control_panel.notebook.add(control_panel.frames.joystick, text="🎮 Joystick")
    
    # Configurar grid
    control_panel.frames.joystick.grid_rowconfigure(0, weight=0)  # Info
    control_panel.frames.joystick.grid_rowconfigure(1, weight=0)  # Controles
    control_panel.frames.joystick.grid_rowconfigure(2, weight=0)  # Configuración
    control_panel.frames.joystick.grid_rowconfigure(3, weight=1)  # Log
    control_panel.frames.joystick.grid_columnconfigure(0, weight=1)

    # Crear secciones
    create_joystick_info_section(control_panel)
    create_joystick_controls_section(control_panel)
    create_joystick_config_section(control_panel)
    create_joystick_log_section(control_panel)
    
    # Actualizar información inicial
    update_joystick_info(control_panel)

def create_joystick_info_section(control_panel):
    """Crea la sección de información del joystick"""
    # Frame principal para información
    info_frame = ttk.LabelFrame(control_panel.frames.joystick, text="📋 Información del Joystick", padding=10)
    info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
    
    # Labels para mostrar información
    control_panel.joystick_info_labels = {}
    
    # Estado de conexión
    ttk.Label(info_frame, text="Estado:").grid(row=0, column=0, sticky="w", padx=(0, 10))
    control_panel.joystick_info_labels['status'] = ttk.Label(info_frame, text="❌ Desconectado", foreground="red")
    control_panel.joystick_info_labels['status'].grid(row=0, column=1, sticky="w")
    
    # Nombre del joystick
    ttk.Label(info_frame, text="Nombre:").grid(row=1, column=0, sticky="w", padx=(0, 10))
    control_panel.joystick_info_labels['name'] = ttk.Label(info_frame, text="N/A")
    control_panel.joystick_info_labels['name'].grid(row=1, column=1, sticky="w")
    
    # Número de botones
    ttk.Label(info_frame, text="Botones:").grid(row=2, column=0, sticky="w", padx=(0, 10))
    control_panel.joystick_info_labels['buttons'] = ttk.Label(info_frame, text="N/A")
    control_panel.joystick_info_labels['buttons'].grid(row=2, column=1, sticky="w")
    
    # Número de ejes
    ttk.Label(info_frame, text="Ejes:").grid(row=3, column=0, sticky="w", padx=(0, 10))
    control_panel.joystick_info_labels['axes'] = ttk.Label(info_frame, text="N/A")
    control_panel.joystick_info_labels['axes'].grid(row=3, column=1, sticky="w")

    # Selector de tipo de controlador
    control_panel.controller_type_var = tk.StringVar(value="xbox")
    control_panel.controller_type_radios = {}

    control_panel.controller_type_radios["xbox"] = ttk.Radiobutton(info_frame, text="Xbox",
        variable=control_panel.controller_type_var,
        value="xbox",
        command=lambda: on_controller_type_change(control_panel)
    )
    control_panel.controller_type_radios["xbox"].grid(row=0, column=3, sticky="w")

    control_panel.controller_type_radios["playstation"] = ttk.Radiobutton(
        info_frame, text="PlayStation",
        variable=control_panel.controller_type_var,
        value="playstation",
        command=lambda: on_controller_type_change(control_panel)
    )
    control_panel.controller_type_radios["playstation"].grid(row=0, column=4, sticky="w")

def on_controller_type_change(control_panel):
    """
    Maneja el cambio de tipo de controlador.
    """
    selected_type = control_panel.controller_type_var.get()
    
    control_panel.joystick_controller.set_controller_type(selected_type)
    update_button_config_ui(control_panel)
    log_joystick_message(control_panel, f"🎮 Tipo de controlador cambiado a: {selected_type}")

def update_button_config_ui(control_panel):
    """
    Actualiza la interfaz de configuración de botones según el tipo de controlador.
    """
    if hasattr(control_panel, 'config_entries'):
        available_buttons = control_panel.joystick_controller.get_available_buttons()
        print(available_buttons)
        for action, combobox in control_panel.config_entries.items():
            # Intentar mantener el valor actual si es válido para el nuevo tipo
            current_value = combobox.get()
            if current_value:
                current_action = control_panel.joystick_controller.get_abstract_button_from_action(action)
            else:
                current_abstract = None
            combobox['values'] = list(available_buttons.values())

            if current_abstract:
                print("holiwis")
                new_display_name = control_panel.joystick_controller.button_mapping.get_display_name_from_abstract(current_action)
                print(new_display_name)
                combobox.set(new_display_name)
            elif current_value not in available_buttons.values():
                combobox.set('')

def create_joystick_controls_section(control_panel):
    """Crea la sección de controles del joystick"""
    # Frame principal para controles
    controls_frame = ttk.LabelFrame(control_panel.frames.joystick, text="🎛️ Controles", padding=10)
    controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    
    # Configurar grid del frame de controles
    for i in range(4):
        controls_frame.grid_columnconfigure(i, weight=1)
    
    # Botón para detectar joysticks
    btn_detect = ttk.Button(controls_frame, text="🔍 Detectar Joysticks", command=lambda: detect_joysticks_action(control_panel))
    btn_detect.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    
    # Botón para conectar joystick
    control_panel.btn_connect = ttk.Button(controls_frame, text="🔌 Conectar", 
                                          command=lambda: connect_joystick_action(control_panel))
    control_panel.btn_connect.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    # Botón para iniciar/parar escucha
    control_panel.btn_listen = ttk.Button(controls_frame, text="🎧 Iniciar Escucha", 
                                         command=lambda: toggle_listening_action(control_panel))
    control_panel.btn_listen.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    
    # Botón para probar botones
    control_panel.btn_test = ttk.Button(controls_frame, text="🧪 Probar Botones", 
                                       command=lambda: test_buttons_action(control_panel))
    control_panel.btn_test.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

def create_joystick_config_section(control_panel):
    """Crea la sección de configuración de botones del joystick con sistema abstracto"""
    # Frame principal para configuración
    control_panel.config_frame = ttk.LabelFrame(control_panel.frames.joystick, text="⚙️ Configuración de Botones", padding=10)
    control_panel.config_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

    # Configurar grid del frame de configuración
    for i in range(8):
        control_panel.config_frame.grid_columnconfigure(i, weight=1)

    # Inicializar configuración de acciones con botones abstractos
    if not hasattr(control_panel, 'action_config'):
        control_panel.action_config = DEFAULT_SCOREBOARD_ACTIONS.copy()

    # Crear diccionario para almacenar las configuraciones de UI
    control_panel.config_entries = {}

    # Fila 1: Labels de acciones
    action_labels = {
        'home_add_point': "🏠 +1 Local:",
        'away_add_point': "🚗 +1 Visit:",
        'home_subtract_point': "🏠 -1 Local:",
        'away_subtract_point': "🚗 -1 Visit:",
        'manage_timer': "▶️ Iniciar:",
        'pause_timer': "⏸️ Pausar:",
        'resume_timer': "▶️ Reanudar:"
    }

    for i, (action, label) in enumerate(action_labels.items(), start=1):
        ttk.Label(control_panel.config_frame, text=label, font=('Arial', 8)).grid(row=0, column=i, sticky="w")

        # Crear combobox para cada acción
        available_buttons = control_panel.joystick_controller.get_available_buttons()
        control_panel.config_entries[action] = ttk.Combobox(
            control_panel.config_frame,
            state="readonly",
            values=list(available_buttons.values()),
            width=8
        )
        control_panel.config_entries[action].grid(row=1, column=i, padx=2)

        # Establecer valor por defecto
        default_abstract_button = control_panel.action_config[action]
        default_display_name = control_panel.joystick_controller.button_mapping.get_display_name(default_abstract_button)
        control_panel.config_entries[action].set(default_display_name)

    # Botones de acción
    btn_apply = ttk.Button(control_panel.config_frame, text="✅ Aplicar",
                          command=lambda: apply_button_config(control_panel))
    btn_apply.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

    btn_reset = ttk.Button(control_panel.config_frame, text="🔄 Restablecer",
                          command=lambda: reset_button_config(control_panel))
    btn_reset.grid(row=3, column=3, columnspan=2, padx=5, pady=10, sticky="ew")

    btn_test_mode = ttk.Button(control_panel.config_frame, text="🧪 Modo Prueba",
                              command=lambda: toggle_test_mode(control_panel))
    btn_test_mode.grid(row=3, column=5, columnspan=2, padx=5, pady=10, sticky="ew")



def create_joystick_log_section(control_panel):
    """Crea la sección de log del joystick"""
    # Frame principal para log
    log_frame = ttk.LabelFrame(control_panel.frames.joystick, text="📝 Log de Actividad", padding=10)
    log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
    
    # Configurar grid
    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)
    
    # Text widget para el log con scrollbar
    log_text_frame = ttk.Frame(log_frame)
    log_text_frame.grid(row=0, column=0, sticky="nsew")
    log_text_frame.grid_rowconfigure(0, weight=1)
    log_text_frame.grid_columnconfigure(0, weight=1)
    
    control_panel.joystick_log = tk.Text(log_text_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
    control_panel.joystick_log.grid(row=0, column=0, sticky="nsew")
    
    # Scrollbar para el log
    scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=control_panel.joystick_log.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    control_panel.joystick_log.configure(yscrollcommand=scrollbar.set)
    
    # Botón para limpiar log
    btn_clear_log = ttk.Button(log_frame, text="🗑️ Limpiar Log", 
                              command=lambda: clear_joystick_log(control_panel))
    btn_clear_log.grid(row=1, column=0, pady=(10, 0))

def log_joystick_message(control_panel, message):
    """
    Agrega un mensaje al log del joystick.
    
    Args:
        control_panel: Instancia de Gui_control_panel
        message (str): Mensaje a agregar
    """
    if hasattr(control_panel, 'joystick_log'):
        control_panel.joystick_log.config(state=tk.NORMAL)
        control_panel.joystick_log.insert(tk.END, f"{message}\n")
        control_panel.joystick_log.see(tk.END)
        control_panel.joystick_log.config(state=tk.DISABLED)

def clear_joystick_log(control_panel):
    """Limpia el log del joystick"""
    control_panel.joystick_log.config(state=tk.NORMAL)
    control_panel.joystick_log.delete(1.0, tk.END)
    control_panel.joystick_log.config(state=tk.DISABLED)

def update_joystick_info(control_panel):
    """Actualiza la información mostrada del joystick"""
    if control_panel.joystick_controller.is_connected():
        info = control_panel.joystick_controller.get_joystick_info()
        control_panel.joystick_info_labels['status'].config(text="✅ Conectado", foreground="green")
        control_panel.joystick_info_labels['name'].config(text=f"{info['name']} ({info['type'].title()})")
        control_panel.joystick_info_labels['buttons'].config(text=str(info['num_buttons']))
        control_panel.joystick_info_labels['axes'].config(text=str(info['num_axes']))

        # Actualizar el radio button del tipo de controlador detectado
        if info['type'] in ['xbox', 'playstation']:
            control_panel.controller_type_var.set(info['type'])
            update_button_config_ui(control_panel)

        # Actualizar botones
        control_panel.btn_connect.config(text="🔌 Desconectar")
        control_panel.btn_test.config(state="normal")
        control_panel.btn_listen.config(state="normal")
    else:
        control_panel.joystick_info_labels['status'].config(text="❌ Desconectado", foreground="red")
        control_panel.joystick_info_labels['name'].config(text="N/A")
        control_panel.joystick_info_labels['buttons'].config(text="N/A")
        control_panel.joystick_info_labels['axes'].config(text="N/A")

        # Actualizar botones
        control_panel.btn_connect.config(text="🔌 Conectar")
        control_panel.btn_test.config(state="disabled")
        control_panel.btn_listen.config(state="disabled", text="🎧 Iniciar Escucha")

# Funciones de acción para los botones

def detect_joysticks_action(control_panel):
    """Acción para detectar joysticks"""
    joysticks = control_panel.joystick_controller.detect_joysticks()
    
    if joysticks:
        message = f"🔍 Encontrados {len(joysticks)} joystick(s):\n"
        for joy in joysticks:
            message += f"  • {joy['name']} (ID: {joy['id']})\n"
    else:
        message = "❌ No se encontraron joysticks conectados"
    
    log_joystick_message(control_panel, message)
    messagebox.showinfo("Detección de Joysticks", message)

def connect_joystick_action(control_panel):
    """Acción para conectar/desconectar joystick"""
    if control_panel.joystick_controller.is_connected():
        # Desconectar
        control_panel.joystick_controller.stop_listening()
        control_panel.joystick_controller.disconnect_joystick()
        log_joystick_message(control_panel, "🔌 Joystick desconectado")
    else:
        # Conectar
        if control_panel.joystick_controller.connect_joystick(0):
            log_joystick_message(control_panel, "✅ Joystick conectado exitosamente")
        else:
            log_joystick_message(control_panel, "❌ Error al conectar joystick")
    
    update_joystick_info(control_panel)

def toggle_listening_action(control_panel):
    """Acción para iniciar/parar la escucha del joystick"""
    if control_panel.joystick_controller.is_running:
        # Parar escucha
        control_panel.joystick_controller.stop_listening()
        control_panel.btn_listen.config(text="🎧 Iniciar Escucha")
        log_joystick_message(control_panel, "🛑 Escucha del joystick detenida")
    else:
        # Iniciar escucha
        if control_panel.joystick_controller.start_listening():
            control_panel.btn_listen.config(text="🛑 Parar Escucha")
            log_joystick_message(control_panel, "🎧 Escucha del joystick iniciada")
        else:
            log_joystick_message(control_panel, "❌ Error al iniciar escucha")

def test_buttons_action(control_panel):
    """Acción para probar botones del joystick"""
    def test_in_thread():
        log_joystick_message(control_panel, "🧪 Modo prueba iniciado - Presiona botones para verlos")
        # Aquí podrías implementar un modo de prueba temporal
        # Por ahora solo mostramos el mensaje

    threading.Thread(target=test_in_thread, daemon=True).start()

def apply_button_config(control_panel):
    """Aplica la nueva configuración de botones usando el sistema abstracto"""
    try:
        # Leer valores de los comboboxes y convertir a botones abstractos
        new_action_config = {}

        
        available_buttons = control_panel.joystick_controller.get_available_buttons()

        for action, combobox in control_panel.config_entries.items():
            selected_display_name = combobox.get().strip()

            if not selected_display_name:
                raise ValueError(f"Debe seleccionar un botón para la acción: {action}")

            # Buscar el botón abstracto correspondiente al nombre seleccionado
            abstract_button = None
            for abstract_btn, display_name in available_buttons.items():
                if display_name == selected_display_name:
                    abstract_button = AbstractButton(abstract_btn)
                    break

            if abstract_button is None:
                raise ValueError(f"Botón '{selected_display_name}' no reconocido para la acción: {action}")

            new_action_config[action] = abstract_button

        # Verificar que no hay botones duplicados
        button_values = list(new_action_config.values())
        if len(button_values) != len(set(button_values)):
            raise ValueError("No puedes asignar el mismo botón a múltiples acciones")

        # Actualizar configuración de acciones
        control_panel.action_config = new_action_config

        # Actualizar la configuración en el joystick controller
        control_panel.joystick_controller.set_action_config(new_action_config)

        # Actualizar el mapeo en el joystick controller
        update_joystick_mapping(control_panel)

        log_joystick_message(control_panel, "✅ Configuración de botones aplicada exitosamente")
        messagebox.showinfo("Configuración", "✅ Configuración de botones aplicada exitosamente")

    except ValueError as e:
        error_msg = f"❌ Error en configuración: {str(e)}"
        log_joystick_message(control_panel, error_msg)
        messagebox.showerror("Error de Configuración", error_msg)
    except Exception as e:
        error_msg = f"❌ Error inesperado: {str(e)}"
        log_joystick_message(control_panel, error_msg)
        messagebox.showerror("Error", error_msg)

def reset_button_config(control_panel):
    """Restablece la configuración de botones a los valores por defecto"""
    # Restablecer a la configuración por defecto abstracta
    control_panel.action_config = DEFAULT_SCOREBOARD_ACTIONS.copy()

    # Actualizar los comboboxes con los valores por defecto
    available_buttons = control_panel.joystick_controller.get_available_buttons()

    for action, abstract_button in control_panel.action_config.items():
        if action in control_panel.config_entries:
            # Obtener el nombre para mostrar del botón abstracto
            display_name = control_panel.joystick_controller.button_mapping.get_display_name(abstract_button)
            control_panel.config_entries[action].set(display_name)

    # Actualizar la configuración en el joystick controller
    control_panel.joystick_controller.set_action_config(control_panel.action_config)

    # Actualizar el mapeo en el joystick controller
    update_joystick_mapping(control_panel)

    log_joystick_message(control_panel, "🔄 Configuración restablecida a valores por defecto")
    messagebox.showinfo("Configuración", "🔄 Configuración restablecida a valores por defecto")

def toggle_test_mode(control_panel):
    """Activa/desactiva el modo de prueba para identificar botones"""
    if not control_panel.joystick_controller.is_connected():
        messagebox.showwarning("Joystick", "❌ Conecta un joystick primero")
        return

    # Crear ventana de modo prueba
    test_window = tk.Toplevel(control_panel.root)
    test_window.title("🧪 Modo Prueba - Identificar Botones")
    test_window.geometry("400x400")
    test_window.resizable(False, False)

    # Hacer la ventana modal
    test_window.transient(control_panel.root)
    test_window.grab_set()

    # Contenido de la ventana
    ttk.Label(test_window, text="🧪 Modo Prueba de Botones",font=('Arial', 14, 'bold')).pack(pady=10)

    ttk.Label(test_window, text="Presiona cualquier botón del joystick para ver su número", font=('Arial', 10)).pack(pady=5)

    # Text widget para mostrar botones presionados
    test_text = tk.Text(test_window, height=10, width=40, state=tk.DISABLED)
    test_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Scrollbar para el text widget
    scrollbar = ttk.Scrollbar(test_window, orient="vertical", command=test_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    test_text.configure(yscrollcommand=scrollbar.set)

    # Botón para cerrar
    ttk.Button(test_window, text="❌ Cerrar", command=test_window.destroy).pack(pady=10)

    # Función para mostrar botones presionados
    def show_button_press(button_id):
        test_text.config(state=tk.NORMAL)
        test_text.insert(tk.END, f"🔘 Botón {button_id} presionado\n")
        test_text.see(tk.END)
        test_text.config(state=tk.DISABLED)

    # Temporalmente cambiar el callback del joystick para el modo prueba
    original_mapping = control_panel.joystick_controller._get_button_mapping()

    # Crear mapeo temporal para modo prueba
    test_mapping = {}
    for i in range(16):  # Hasta 16 botones
        test_mapping[i] = f'test_button_{i}'
        control_panel.joystick_controller.set_callback(f'test_button_{i}',
                                                      lambda btn=i: show_button_press(btn))

    # Función para restaurar configuración al cerrar
    def on_test_close():
        # Restaurar mapeo original
        update_joystick_mapping(control_panel)
        test_window.destroy()

    test_window.protocol("WM_DELETE_WINDOW", on_test_close)

def update_joystick_mapping(control_panel):
    """Actualiza el mapeo de botones en el joystick controller usando el sistema abstracto"""
    # El sistema abstracto ya maneja el mapeo automáticamente a través del button_mapper
    # Solo necesitamos asegurarnos de que la configuración de acciones esté actualizada
    if hasattr(control_panel, 'action_config'):
        control_panel.joystick_controller.set_action_config(control_panel.action_config)

    # Obtener información del mapeo actual para logging
    current_mapping = control_panel.joystick_controller._get_button_mapping()

    # Formatear mensaje de log
    mapping_info = []
    for physical_btn, action in current_mapping.items():
        abstract_btn = control_panel.joystick_controller.button_mapping.get_abstract_button(physical_btn)
        if abstract_btn:
            display_name = control_panel.joystick_controller.button_mapping.get_display_name(abstract_btn)
            mapping_info.append(f"{display_name}({physical_btn})→{action}")

    log_joystick_message(control_panel, f"🔄 Mapeo actualizado: {', '.join(mapping_info)}")
