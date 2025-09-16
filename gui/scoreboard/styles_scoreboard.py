from tkinter import ttk

def apply_styles():
    style = ttk.Style()
    style.configure("Teams_name.TLabel", font=("Arial", 40, "bold"), foreground="white", background="black")
    # Podés definir más estilos:
    style.configure("Red.TButton", font=("Arial", 14), foreground="white", background="red")
    style.configure("Title.TEntry", font=("Arial", 16))
    style.configure("home_team.TFrame",background="red")
    style.configure("time.TFrame",background="orange")