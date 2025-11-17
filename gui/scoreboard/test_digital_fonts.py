"""
Script de prueba para visualizar diferentes fuentes digitales disponibles.
Útil para elegir la mejor fuente para el reloj del scoreboard.
"""

import tkinter as tk
from tkinter import font as tkfont

# Lista de fuentes digitales/monoespaciadas a probar
DIGITAL_FONTS = [
    'Orbitron',
    'Consolas',
    'Courier New',
    'Lucida Console',
    'Monaco',
    'Monospace',
    'DejaVu Sans Mono',
    'Liberation Mono',
    'Courier',
    'Fixedsys',
    'Terminal',
    'OCR A Extended',
    'DS-Digital',
    'Digital-7',
    'DSEG7 Classic',
]

def create_font_preview():
    """Crea una ventana con preview de todas las fuentes digitales."""
    root = tk.Tk()
    root.title("Preview de Fuentes Digitales - Scoreboard")
    root.geometry("900x700")
    root.configure(bg='#0A0E27')
    
    # Título
    title = tk.Label(
        root,
        text="FUENTES DIGITALES DISPONIBLES",
        font=('Arial', 16, 'bold'),
        fg='#00d9ff',
        bg='#0A0E27',
        pady=10
    )
    title.pack()
    
    # Instrucciones
    instructions = tk.Label(
        root,
        text="Estas son las fuentes disponibles en tu sistema.\nLas que se ven mejor son las que deberías usar.",
        font=('Arial', 10),
        fg='#b8c5d6',
        bg='#0A0E27',
        pady=5
    )
    instructions.pack()
    
    # Frame con scroll
    canvas = tk.Canvas(root, bg='#0A0E27', highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#0A0E27')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Obtener todas las fuentes disponibles en el sistema
    available_fonts = set(tkfont.families())
    
    # Probar cada fuente
    for font_name in DIGITAL_FONTS:
        # Frame para cada fuente
        font_frame = tk.Frame(scrollable_frame, bg='#1a1f3a', pady=10, padx=15)
        font_frame.pack(fill='x', padx=10, pady=5)
        
        # Verificar si la fuente está disponible
        is_available = font_name in available_fonts
        status_color = '#00ff41' if is_available else '#ff0844'
        status_text = '✓ DISPONIBLE' if is_available else '✗ NO DISPONIBLE'
        
        # Nombre de la fuente
        name_label = tk.Label(
            font_frame,
            text=f"{font_name}",
            font=('Arial', 11, 'bold'),
            fg='#ffffff',
            bg='#1a1f3a',
            anchor='w'
        )
        name_label.pack(anchor='w')
        
        # Estado
        status_label = tk.Label(
            font_frame,
            text=status_text,
            font=('Arial', 9),
            fg=status_color,
            bg='#1a1f3a',
            anchor='w'
        )
        status_label.pack(anchor='w')
        
        # Preview del reloj con esta fuente
        try:
            preview_label = tk.Label(
                font_frame,
                text="12:34",
                font=(font_name, 60, 'bold'),
                fg='#00d9ff',
                bg='#0d1117',
                pady=10
            )
            preview_label.pack(fill='x', pady=5)
        except:
            preview_label = tk.Label(
                font_frame,
                text="[No se puede mostrar preview]",
                font=('Arial', 10),
                fg='#ff0844',
                bg='#0d1117',
                pady=10
            )
            preview_label.pack(fill='x', pady=5)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Información adicional
    info_frame = tk.Frame(root, bg='#0A0E27', pady=10)
    info_frame.pack(fill='x')
    
    info_text = tk.Label(
        info_frame,
        text="💡 Tip: Las fuentes marcadas con ✓ están instaladas en tu sistema.\n"
             "Orbitron y Consolas son las recomendadas para un look profesional.",
        font=('Arial', 9),
        fg='#ffd700',
        bg='#0A0E27',
        justify='left'
    )
    info_text.pack()
    
    root.mainloop()

if __name__ == "__main__":
    print("=" * 60)
    print("PREVIEW DE FUENTES DIGITALES PARA SCOREBOARD")
    print("=" * 60)
    print("\nAbriendo ventana de preview...")
    print("\nFuentes a probar:")
    for font in DIGITAL_FONTS:
        print(f"  - {font}")
    print("\n" + "=" * 60)
    
    create_font_preview()

