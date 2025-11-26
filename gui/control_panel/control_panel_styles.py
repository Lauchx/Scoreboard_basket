"""
Estilos visuales para el panel de control.
Configura los widgets ttk.Entry, ttk.Combobox, etc. para tener buena visibilidad.
"""

from tkinter import ttk


def apply_control_panel_styles(root):
    """
    Aplica estilos personalizados al panel de control para mejorar la visibilidad.
    
    Args:
        root: Ventana raíz del panel de control
    """
    style = ttk.Style(root)
    
    # Usar tema 'clam' como base (más personalizable)
    available_themes = style.theme_names()
    if 'clam' in available_themes:
        style.theme_use('clam')
    elif 'alt' in available_themes:
        style.theme_use('alt')
    
    # ═══════════════════════════════════════════════════════════
    # ENTRY WIDGETS - Campos de texto
    # ═══════════════════════════════════════════════════════════
    
    # Configuración para Entry widgets con máxima visibilidad
    # Fondo blanco, texto negro, borde visible
    style.configure("TEntry",
                   fieldbackground='#FFFFFF',  # Fondo blanco
                   foreground='#000000',       # Texto negro
                   bordercolor='#4a5568',      # Borde gris oscuro
                   lightcolor='#e2e8f0',       # Color claro del borde 3D
                   darkcolor='#2d3748',        # Color oscuro del borde 3D
                   insertcolor='#000000',      # Color del cursor (negro)
                   selectbackground='#3b82f6', # Fondo de selección (azul)
                   selectforeground='#FFFFFF') # Texto seleccionado (blanco)
    
    # Estado de foco (cuando el usuario está escribiendo)
    style.map("TEntry",
             fieldbackground=[('focus', '#FFFFFF')],  # Mantener fondo blanco
             foreground=[('focus', '#000000')],       # Mantener texto negro
             bordercolor=[('focus', '#3b82f6')])      # Borde azul cuando tiene foco
    
    # ═══════════════════════════════════════════════════════════
    # COMBOBOX WIDGETS - Listas desplegables
    # ═══════════════════════════════════════════════════════════
    
    # Configuración para Combobox con buena visibilidad
    style.configure("TCombobox",
                   fieldbackground='#FFFFFF',  # Fondo blanco
                   foreground='#000000',       # Texto negro
                   background='#FFFFFF',       # Fondo del botón
                   bordercolor='#4a5568',      # Borde gris oscuro
                   arrowcolor='#000000',       # Flecha negra
                   selectbackground='#3b82f6', # Fondo de selección
                   selectforeground='#FFFFFF') # Texto seleccionado
    
    style.map("TCombobox",
             fieldbackground=[('readonly', '#F0F0F0'),  # Fondo gris claro en readonly
                            ('focus', '#FFFFFF')],      # Fondo blanco con foco
             foreground=[('readonly', '#000000'),       # Texto negro en readonly
                        ('focus', '#000000')],          # Texto negro con foco
             bordercolor=[('focus', '#3b82f6')])        # Borde azul con foco
    
    # ═══════════════════════════════════════════════════════════
    # LABEL WIDGETS - Etiquetas de texto
    # ═══════════════════════════════════════════════════════════
    
    # Labels con texto oscuro sobre fondo claro
    style.configure("TLabel",
                   background='#F5F5F5',  # Fondo gris muy claro
                   foreground='#1a202c')  # Texto gris muy oscuro (casi negro)
    
    # ═══════════════════════════════════════════════════════════
    # LABELFRAME WIDGETS - Marcos con etiqueta
    # ═══════════════════════════════════════════════════════════
    
    # LabelFrame con buen contraste
    style.configure("TLabelframe",
                   background='#F5F5F5',  # Fondo gris muy claro
                   foreground='#1a202c',  # Texto oscuro
                   bordercolor='#cbd5e0', # Borde gris medio
                   relief='groove')
    
    style.configure("TLabelframe.Label",
                   background='#F5F5F5',  # Fondo gris muy claro
                   foreground='#1a202c',  # Texto oscuro
                   font=('Arial', 10, 'bold'))
    
    # ═══════════════════════════════════════════════════════════
    # BUTTON WIDGETS - Botones
    # ═══════════════════════════════════════════════════════════
    
    # Botones con buen contraste
    style.configure("TButton",
                   background='#4a5568',  # Fondo gris oscuro
                   foreground='#FFFFFF',  # Texto blanco
                   bordercolor='#2d3748', # Borde más oscuro
                   relief='raised',
                   padding=(10, 5))
    
    style.map("TButton",
             background=[('active', '#3b82f6'),   # Azul al pasar el mouse
                        ('pressed', '#2563eb')],  # Azul más oscuro al presionar
             foreground=[('active', '#FFFFFF'),   # Texto blanco
                        ('pressed', '#FFFFFF')])  # Texto blanco
    
    # ═══════════════════════════════════════════════════════════
    # CHECKBUTTON WIDGETS - Casillas de verificación
    # ═══════════════════════════════════════════════════════════
    
    style.configure("TCheckbutton",
                   background='#F5F5F5',  # Fondo gris muy claro
                   foreground='#1a202c',  # Texto oscuro
                   indicatorcolor='#FFFFFF',  # Color del indicador
                   bordercolor='#4a5568')     # Borde del indicador
    
    # ═══════════════════════════════════════════════════════════
    # NOTEBOOK WIDGETS - Pestañas
    # ═══════════════════════════════════════════════════════════
    
    # Notebook (pestañas) con buen contraste
    style.configure("TNotebook",
                   background='#E5E5E5',  # Fondo gris claro
                   bordercolor='#cbd5e0', # Borde gris
                   tabmargins=[2, 5, 2, 0])
    
    style.configure("TNotebook.Tab",
                   background='#D0D0D0',  # Fondo de pestaña inactiva
                   foreground='#1a202c',  # Texto oscuro
                   padding=[10, 5],
                   font=('Arial', 9, 'bold'))
    
    style.map("TNotebook.Tab",
             background=[('selected', '#FFFFFF'),   # Fondo blanco para pestaña activa
                        ('active', '#E0E0E0')],     # Gris claro al pasar el mouse
             foreground=[('selected', '#1a202c'),   # Texto oscuro
                        ('active', '#1a202c')])     # Texto oscuro
    
    # ═══════════════════════════════════════════════════════════
    # FRAME WIDGETS - Contenedores
    # ═══════════════════════════════════════════════════════════
    
    style.configure("TFrame",
                   background='#F5F5F5')  # Fondo gris muy claro
    
    print("[OK] Estilos del panel de control aplicados correctamente")
    
    return style

