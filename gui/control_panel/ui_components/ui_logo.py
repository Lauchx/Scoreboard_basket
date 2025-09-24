from tkinter import Image, filedialog, messagebox, ttk
from PIL import Image, ImageTk

def buttons_logo(self, team_controller, team_simple_name_space):
    ttk.Button(team_simple_name_space.labelFrame, text="Cargar Logo", command=lambda: upload_logo(self, team_controller, team_simple_name_space)).grid(row=0, column=2)

def upload_logo(self, teamController, team_simple_name_space):
        """Carga el logo del equipo desde 'assets/'."""
        path = filedialog.askopenfilename(title="Seleccionar logo", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
        if path:
            try:
                file_name = f"{teamController.team.name}_logo.png"

                image = Image.open(path)
                image = image.resize((300, 300), Image.LANCZOS)
                logo = ImageTk.PhotoImage(image)

                teamController.change_logo(logo)
                self.scoreboard_window.update_team_logo_label()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
