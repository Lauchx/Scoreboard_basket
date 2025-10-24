import tkinter as tk
from tkinter import ttk, messagebox
import threading

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

    console = tk.StringVar(value="PlayStation")
    control_panel.is_playstation = True
    control_panel.radioButton = {}
    control_panel.radioButton["playstation"] = ttk.Radiobutton(info_frame, text="PlayStation", variable=console, value="PlayStation",command=lambda:on_console_change(control_panel, True))
    control_panel.radioButton["playstation"].grid(row=0, column=3, sticky="w")
    control_panel.radioButton["xbox"] = ttk.Radiobutton(info_frame, text="Xbox", variable=console, value="Xbox", command=lambda:on_console_change(control_panel, False))
    control_panel.radioButton["xbox"].grid(row=0, column=4, sticky="w")

def on_console_change(control_panel,bool):
    setattr(control_panel, "is_playstation", bool)
    config_button(control_panel)

def config_button(control_panel):
    if control_panel.is_playstation == True:
        control_panel.button_config = {
            'L1': 4,
            'R1':5,
            '□': 2,
            '△':3,
            '►':7 ,
            'X':0,
            'O':1
        }
    else:
            control_panel.button_config = {
            'LB': 4,
            'RB': 5,
            'X': 2,
            'Y': 3,
            '►': 7,
            'A': 0,
            'B': 1
        }        
    
    for key in control_panel.config_entries:
            print("2")
            print(control_panel.config_entries[key])
            control_panel.config_entries[key].configure(values=list(control_panel.button_config.keys()))
            control_panel.config_entries[key].set('')
        

    

    
        

       

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
    """Crea la sección de configuración de botones del joystick"""
    # Frame principal para configuración
    control_panel.config_frame = ttk.LabelFrame(control_panel.frames.joystick, text="⚙️ Configuración de Botones", padding=10)
    control_panel.config_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

    # Configurar grid del frame de configuración
    for i in range(8):
        control_panel.config_frame.grid_columnconfigure(i, weight=1)

    # Inicializar diccionario para almacenar las configuraciones
    if not hasattr(control_panel, 'button_config'):
        control_panel.button_config = {
            'home_add_point': 4,
            'away_add_point': 5,
            'home_subtract_point': 2,
            'away_subtract_point': 3,
            'manage_timer': 7
        }

    # Crear labels y entries para cada acción
    control_panel.config_entries = {}

    config_button(control_panel)

    # Fila 1: Puntos
    ttk.Label(control_panel.config_frame, text="🏠 +1 Local:", font=('Arial', 8)).grid(row=0, column=1, sticky="w")
    ttk.Label(control_panel.config_frame, text="🚗 +1 Visit:", font=('Arial', 8)).grid(row=0, column=2,  sticky="w")
    ttk.Label(control_panel.config_frame, text="🏠 -1 Local:", font=('Arial', 8)).grid(row=0, column=3,  sticky="w")
    ttk.Label(control_panel.config_frame, text="🚗 -1 Visit:", font=('Arial', 8)).grid(row=0, column=4,  sticky="w")
    ttk.Label(control_panel.config_frame, text="▶️ Iniciar:", font=('Arial', 8)).grid(row=0, column=5,  sticky="w")

    reset_button_config(control_panel)
    for i,key in enumerate(control_panel.default_config, start=1):
            control_panel.config_entries[key] = ttk.Combobox(control_panel.config_frame, state="readonly", values=list(control_panel.button_config.keys()), width=5)
            control_panel.config_entries[key].grid(row=1, column=i)
            control_panel.config_entries[key].set('L1')

    # Botones de acción
    btn_apply = ttk.Button(control_panel.config_frame, text="✅ Aplicar",  command=lambda: apply_button_config(control_panel))
    btn_apply.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    btn_reset = ttk.Button(control_panel.config_frame, text="🔄 Restablecer", command=lambda: reset_button_config(control_panel))
    btn_reset.grid(row=3, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

    btn_test_mode = ttk.Button(control_panel.config_frame, text="🧪 Modo Prueba", command=lambda: toggle_test_mode(control_panel))
    btn_test_mode.grid(row=3, column=4, columnspan=2, padx=5, pady=10, sticky="ew")



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
        control_panel.joystick_info_labels['name'].config(text=info['name'])
        control_panel.joystick_info_labels['buttons'].config(text=str(info['num_buttons']))
        control_panel.joystick_info_labels['axes'].config(text=str(info['num_axes']))
        
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
    """Aplica la nueva configuración de botones"""
    try:
        # Leer valores de los entries
        new_config = {}
        for action, combobox in control_panel.config_entries.items():
            value = control_panel.button_config[combobox.get().strip()]
            print(value, "g")
            if not isinstance(value, int):
                raise ValueError(f"El valor para {action} debe ser un número")
            new_config[action] = int(value)
        
        for action in new_config:
            print(action, "=", new_config[action])

        # Verificar que no hay botones duplicados
        button_numbers = list(new_config.values())
        if len(button_numbers) != len(set(button_numbers)):
            raise ValueError("No puedes asignar el mismo botón a múltiples acciones")

        # Verificar que los números de botón son válidos (0-11 es un rango razonable)
        for action, button_num in new_config.items():
            if button_num < 0 or button_num > 11:
                raise ValueError(f"El botón {button_num} está fuera del rango válido (0-11)")

        # Actualizar configuración
        control_panel.button_config = new_config

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
    control_panel.default_config = {
        'home_add_point': 4,
        'away_add_point': 5,
        'home_subtract_point': 2,
        'away_subtract_point': 3,
        'manage_timer': 7
    }

    # Actualizar entries con valores por defecto
    for action, default_value in control_panel.default_config.items():
        if action in control_panel.config_entries:
            control_panel.config_entries[action].delete(0, tk.END)
            control_panel.config_entries[action].insert(0, str(default_value))

    # Actualizar configuración
    #control_panel.button_config = control_panel.default_config

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
    """Actualiza el mapeo de botones en el joystick controller"""
    # Crear nuevo mapeo basado en la configuración actual
    new_mapping = {}
    for action, button_num in control_panel.button_config.items():
        new_mapping[button_num] = action

    # Actualizar el método _get_button_mapping del joystick controller
    def get_custom_mapping():
        return new_mapping

    # Reemplazar el método temporalmente
    control_panel.joystick_controller._get_button_mapping = get_custom_mapping

    log_joystick_message(control_panel, f"🔄 Mapeo actualizado: {control_panel.button_config}")
