from tkinter import ttk

def apply_general_styles():
    styles = ttk.Style()
    styles.theme_use("xpnative") # Modifica El tema Globalmente en toda la app
    # style.theme_use("clam") --> Se usa para hacer estilos mas facilmente. Podemos optar por la opción de librerias como ttkthemes o ttkbootstrap
    #El mejor es ttkbootstrap, ya que tiene un diálogo de selección de color (ColorChooserDialog) que devuelve colores en hex. 
    # Podés ofrecer una interfaz directa al usuario para personalizar colores
