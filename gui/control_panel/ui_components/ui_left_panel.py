from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
from model.player import Player
from PIL import Image, ImageTk
from gui.control_panel.styles_control_panel import apply_styles_control_panel_test

def setup_left_panel(self):
    apply_styles_control_panel_test()
    self.left_frame = ttk.Frame(self.root, style="PanelTestLeft.TFrame")
    self.left_frame.grid(row=0, column=0, sticky="nsew")

    self.notebook = ttk.Notebook(self.left_frame)
    self.notebook.pack(fill="both", expand=True, padx=2, pady=2)

    # Pestaña de Equipos (con notebook interno)
    self.tab_equipos = ttk.Frame(self.notebook)
    self.notebook.add(self.tab_equipos, text="Equipos")
    setup_tab_equipos(self)

    # Pestaña de Ajustes
    self.tab_ajustes = ttk.Frame(self.notebook)
    self.notebook.add(self.tab_ajustes, text="Ajustes")
    setup_tab_ajustes(self)

def setup_tab_equipos(self):
    inner_notebook = ttk.Notebook(self.tab_equipos, style="Compact.TNotebook")
    inner_notebook.pack(fill="both", expand=True, padx=2, pady=2)

    # Pestaña Local
    self.tab_local_team = ttk.Frame(inner_notebook)
    inner_notebook.add(self.tab_local_team, text="Local")
    setup_team_form(self, self.tab_local_team, "local")

    # Pestaña Visitante
    self.tab_visitor_team = ttk.Frame(inner_notebook)
    inner_notebook.add(self.tab_visitor_team, text="Visitante")
    setup_team_form(self, self.tab_visitor_team, "visitor")


def setup_team_form(self, parent_frame, team_type):
    # Determinar el controller correspondiente
    if team_type == "local":
        team_controller = self.match_state_controller.home_team_controller
    else:
        team_controller = self.match_state_controller.away_team_controller

    form_panel = ttk.Frame(parent_frame, padding=3)
    form_panel.pack(fill="x", padx=2, pady=2)

    # Nombre del equipo (máximo 12 caracteres)
    MAX_TEAM_NAME_LENGTH = 12

    ttk.Label(form_panel, text="Equipo:", style="PlayerForm.TLabel").grid(row=0, column=0, sticky="w", padx=2, pady=1)

    # Variable con validación de límite de caracteres
    team_name_var = tk.StringVar()

    def validate_team_name_length(*args):
        """Limita el nombre del equipo a MAX_TEAM_NAME_LENGTH caracteres."""
        current = team_name_var.get()
        if len(current) > MAX_TEAM_NAME_LENGTH:
            team_name_var.set(current[:MAX_TEAM_NAME_LENGTH])

    team_name_var.trace_add('write', validate_team_name_length)

    team_entry = ttk.Entry(form_panel, width=15, style="PlayerForm.TEntry", textvariable=team_name_var)
    team_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=1)
    setattr(self, f"{team_type}_team_name_entry", team_entry)

    def update_team_name():
        team_name = team_entry.get()[:MAX_TEAM_NAME_LENGTH]  # Asegurar truncamiento
        if team_name.strip():
            team_controller.change_name(team_name)
            # Actualizar marcador si está disponible
            if hasattr(self, 'main_panel') and self.main_panel is not None:
                if hasattr(self.main_panel, 'scoreboard_window'):
                    self.main_panel.scoreboard_window.update_team_names_labels()
            team_entry.delete(0, tk.END)

    ttk.Button(form_panel, text="Actualizar", style="PlayerForm.TButton", command=update_team_name).grid(row=0, column=2, padx=2, pady=1)

    def upload_logo():
        """Carga un logo para el equipo"""
        path = filedialog.askopenfilename(
            title="Seleccionar logo",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if path:
            try:
                image = Image.open(path)
                # Tamaño pequeño (80x80) para que quede proporcional al nombre del equipo
                image = image.resize((80, 80), Image.LANCZOS)
                logo = ImageTk.PhotoImage(image)
                team_controller.change_logo(logo)
                
                # Actualizar scoreboard si está disponible
                if hasattr(self, 'main_panel') and self.main_panel is not None:
                    if hasattr(self.main_panel, 'scoreboard_window'):
                        self.main_panel.scoreboard_window.update_team_logo_label()
                
                messagebox.showinfo("Éxito", "Logo cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

    ttk.Button(form_panel, text="Cargar Logo", style="PlayerForm.TButton", command=upload_logo).grid(row=0, column=3, padx=2, pady=1)

    # Nombre del jugador
    ttk.Label(form_panel, text="Jugador:", style="PlayerForm.TLabel").grid(row=1, column=0, sticky="w", padx=2, pady=1)
    player_entry = ttk.Entry(form_panel, width=15, style="PlayerForm.TEntry")
    player_entry.grid(row=1, column=1, sticky="ew", padx=2, pady=1)
    setattr(self, f"{team_type}_player_name_entry", player_entry)

    # Dorsal
    ttk.Label(form_panel, text="Dorsal:", style="PlayerForm.TLabel").grid(row=2, column=0, sticky="w", padx=2, pady=1)
    dorsal_combo = ttk.Combobox(form_panel, values=[str(i) for i in range(0, 100)], width=5, style="PlayerForm.TCombobox")
    dorsal_combo.set("0")
    dorsal_combo.grid(row=2, column=1, sticky="w", padx=2, pady=1)
    setattr(self, f"{team_type}_dorsal_combobox", dorsal_combo)

    # Titular - Botones para cambiar estado (se actualiza desde la tabla)
    is_active_var = tk.BooleanVar(value=False)
    setattr(self, f"{team_type}_is_active_var", is_active_var)
    
    def toggle_player_active():
        from tkinter import messagebox

        # Límite máximo de titulares
        MAX_STARTERS = 5

        tree = getattr(self, f"{team_type}_players_tree")
        selected_item = tree.selection()
        if not selected_item:
            return

        # Obtener datos del item seleccionado
        item = tree.item(selected_item)
        jersey_number = int(item['values'][0])

        # Buscar el jugador en el controller
        player = None
        for p in team_controller.team.players:
            if int(p.jersey_number) == jersey_number:
                player = p
                break

        if player:
            # Validar límite de titulares si se va a activar
            if not player.is_active:  # Va a pasar a activo
                current_starters = sum(1 for p in team_controller.team.players if p.is_active)
                if current_starters >= MAX_STARTERS:
                    messagebox.showwarning(
                        "Límite de titulares",
                        "Solo pueden haber 5 titulares al mismo tiempo."
                    )
                    return

            # Cambiar estado
            player.is_active = not player.is_active

            # Actualizar scoreboard si está disponible
            if hasattr(self, 'main_panel') and self.main_panel is not None:
                if hasattr(self.main_panel, 'scoreboard_window'):
                    self.main_panel.scoreboard_window.update_label_players(player, team_controller)

            status_text = "Titular" if player.is_active else "No Titular"
            status_val = '✓' if player.is_active else '○'

            # Actualizar fila en la tabla (Treeview)
            try:
                tree.item(selected_item[0], values=(player.jersey_number, player.name, status_val, player.foul))
            except Exception:
                # Fallback por si selected_item no es indexable
                try:
                    tree.item(selected_item, values=(player.jersey_number, player.name, status_val, player.foul))
                except Exception:
                    pass

            print(f"{status_val} {player.name} marcado como {status_text}")
    
    ttk.Button(form_panel, text="Cambiar Titular", style="PlayerForm.TButton", command=toggle_player_active).grid(row=2, column=2, sticky="ew", padx=2, pady=1)

    # Funciones para agregar y restar faltas al jugador seleccionado
    def add_player_foul_action():
        tree = getattr(self, f"{team_type}_players_tree")
        selected_item = tree.selection()
        if not selected_item:
            return

        # Obtener datos del item seleccionado
        item = tree.item(selected_item)
        jersey_number = int(item['values'][0])

        # Buscar el jugador en el controller
        player = None
        for p in team_controller.team.players:
            if int(p.jersey_number) == jersey_number:
                player = p
                break

        if player:
            # Validar que hay faltas de equipo disponibles para asignar
            if not team_controller.can_assign_player_foul():
                messagebox.showwarning(
                    "Faltas no disponibles",
                    "No hay faltas de equipo disponibles para asignar.\n\nPrimero agregá una falta de equipo."
                )
                return

            # Agregar falta
            result = team_controller.add_player_foul(player)
            
            # Actualizar scoreboard si está disponible
            if hasattr(self, 'main_panel') and self.main_panel is not None:
                if hasattr(self.main_panel, 'scoreboard_window'):
                    self.main_panel.scoreboard_window.update_label_players(player, team_controller)
                    self.main_panel.scoreboard_window.update_fouls_labels()
                    
                    # Actualizar faltas del equipo en el scoreboard
                    team_fouls = team_controller.get_team_fouls()
                    is_bonus = team_controller.is_team_bonus()
                    
                    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
                        if hasattr(self.main_panel.scoreboard_window, 'home_bonus_fouls'):
                            self.main_panel.scoreboard_window.home_bonus_fouls.update_fouls(team_fouls)
                            self.main_panel.scoreboard_window.home_bonus_fouls.set_bonus(is_bonus)
                    else:
                        if hasattr(self.main_panel.scoreboard_window, 'away_bonus_fouls'):
                            self.main_panel.scoreboard_window.away_bonus_fouls.update_fouls(team_fouls)
                            self.main_panel.scoreboard_window.away_bonus_fouls.set_bonus(is_bonus)
                    # Actualizar etiqueta de faltas en el panel de control (si existe)
                    try:
                        if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
                            team_ns = self.home_team
                        else:
                            team_ns = self.away_team

                        # Si existe método de actualización guardado por ui_players
                        if hasattr(team_ns, 'player') and hasattr(team_ns.player, 'update_team_status'):
                            team_ns.player.update_team_status()
                        # Si existe etiqueta directa de faltas (desde ui_fouls)
                        if hasattr(team_ns, 'fouls') and hasattr(team_ns.fouls, 'label'):
                            try:
                                team_ns.fouls.label.config(text=str(team_controller.get_team_fouls()))
                            except Exception:
                                pass
                    except Exception:
                        pass
            
            # Actualizar fila en la tabla (Treeview)
            status_val = "✓" if player.is_active else "○"
            try:
                tree.item(selected_item, values=(player.jersey_number, player.name, status_val, player.foul))
            except Exception:
                pass

            print(f"➕ Falta añadida a {player.name}: {player.foul}/5 faltas")
            # Imprimir faltas del equipo en consola
            try:
                print(f"Faltas equipo {team_controller.team.name}: {team_fouls}/5")
            except Exception:
                pass
            if result['player_info'].get('suspended'):
                print(f"🚫 {player.name} ha sido SUSPENDIDO (5 faltas)")
            if result['team_info'].get('bonus_activated'):
                print(f"🔴 ¡BONUS ACTIVADO! El equipo tiene {result['team_info']['total_fouls']} faltas")

    def subtract_player_foul_action():
        tree = getattr(self, f"{team_type}_players_tree")
        selected_item = tree.selection()
        if not selected_item:
            return
        
        # Obtener datos del item seleccionado
        item = tree.item(selected_item)
        jersey_number = int(item['values'][0])
        
        # Buscar el jugador en el controller
        player = None
        for p in team_controller.team.players:
            if int(p.jersey_number) == jersey_number:
                player = p
                break
        
        if player:
            # Restar falta
            result = team_controller.subtract_player_foul(player)
            
            # Actualizar scoreboard si está disponible
            if hasattr(self, 'main_panel') and self.main_panel is not None:
                if hasattr(self.main_panel, 'scoreboard_window'):
                    self.main_panel.scoreboard_window.update_label_players(player, team_controller)
                    self.main_panel.scoreboard_window.update_fouls_labels()
                    
                    # Actualizar faltas del equipo en el scoreboard
                    team_fouls = team_controller.get_team_fouls()
                    is_bonus = team_controller.is_team_bonus()
                    
                    if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
                        if hasattr(self.main_panel.scoreboard_window, 'home_bonus_fouls'):
                            self.main_panel.scoreboard_window.home_bonus_fouls.update_fouls(team_fouls)
                            self.main_panel.scoreboard_window.home_bonus_fouls.set_bonus(is_bonus)
                    else:
                        if hasattr(self.main_panel.scoreboard_window, 'away_bonus_fouls'):
                            self.main_panel.scoreboard_window.away_bonus_fouls.update_fouls(team_fouls)
                            self.main_panel.scoreboard_window.away_bonus_fouls.set_bonus(is_bonus)
                    # Actualizar etiqueta de faltas en el panel de control (si existe)
                    try:
                        if team_controller.team.name == self.match_state_controller.home_team_controller.team.name:
                            team_ns = self.home_team
                        else:
                            team_ns = self.away_team

                        if hasattr(team_ns, 'player') and hasattr(team_ns.player, 'update_team_status'):
                            team_ns.player.update_team_status()
                        if hasattr(team_ns, 'fouls') and hasattr(team_ns.fouls, 'label'):
                            try:
                                team_ns.fouls.label.config(text=str(team_controller.get_team_fouls()))
                            except Exception:
                                pass
                    except Exception:
                        pass
            
            # Actualizar fila en la tabla (Treeview)
            status_val = "✓" if player.is_active else "○"
            try:
                tree.item(selected_item, values=(player.jersey_number, player.name, status_val, player.foul))
            except Exception:
                pass

            print(f"➖ Falta quitada a {player.name}: {player.foul}/5 faltas")
            # Imprimir faltas del equipo en consola
            try:
                team_fouls = team_controller.get_team_fouls()
                print(f"Faltas equipo {team_controller.team.name}: {team_fouls}/5")
            except Exception:
                pass

    # Botones para sumar y restar faltas
    fouls_buttons_frame = ttk.Frame(form_panel)
    fouls_buttons_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=2, pady=1)
    
    ttk.Button(fouls_buttons_frame, text="➕ Sumar Falta", style="PlayerForm.TButton", command=add_player_foul_action).pack(side="left", fill="x", expand=True, padx=1)
    ttk.Button(fouls_buttons_frame, text="➖ Restar Falta", style="PlayerForm.TButton", command=subtract_player_foul_action).pack(side="left", fill="x", expand=True, padx=1)

    # Constantes de límites
    MAX_PLAYERS_PER_TEAM = 12
    MAX_STARTERS = 5

    # Funciones para agregar y eliminar jugadores
    def add_player_action():
        from tkinter import messagebox

        player_name = player_entry.get().strip()
        player_jersey = dorsal_combo.get().strip()
        player_is_active = is_active_var.get()

        # Validar límite máximo de jugadores (12)
        if len(team_controller.team.players) >= MAX_PLAYERS_PER_TEAM:
            messagebox.showwarning(
                "Límite de jugadores",
                "No se pueden cargar más de 12 jugadores por equipo."
            )
            return

        if not player_name:
            return

        if not player_jersey.isdigit():
            return

        jersey_int = int(player_jersey)

        # Verificar duplicados
        existing = [int(p.jersey_number) for p in team_controller.team.players]
        if jersey_int in existing:
            messagebox.showwarning("Dorsal duplicado", f"El número #{jersey_int} ya está en uso en el equipo.")
            return

        # Validar límite de titulares (5) si se marca como titular
        if player_is_active:
            current_starters = sum(1 for p in team_controller.team.players if p.is_active)
            if current_starters >= MAX_STARTERS:
                messagebox.showwarning(
                    "Límite de titulares",
                    "Solo pueden haber 5 titulares al mismo tiempo."
                )
                return

        player = Player(player_name, jersey_int, player_is_active)
        team_controller.add_player_in_team(player)
        
        # Actualizar treeview (reconstruir para mantener orden)
        tree = getattr(self, f"{team_type}_players_tree")
        for item in tree.get_children():
            tree.delete(item)
            
        for p in team_controller.team.players:
            status = "✓" if p.is_active else "○"
            tree.insert("", "end", values=(p.jersey_number, p.name, status, p.foul))

        # Actualizar marcador si está disponible
        if hasattr(self, 'main_panel') and self.main_panel is not None:
            if hasattr(self.main_panel, 'scoreboard_window'):
                if hasattr(self.main_panel.scoreboard_window, 'refresh_player_list'):
                    self.main_panel.scoreboard_window.refresh_player_list(team_controller)
                else:
                    self.main_panel.scoreboard_window.update_label_players(player, team_controller)
                    
        # Limpiar entrada
        player_entry.delete(0, tk.END)
        dorsal_combo.set("0")
        is_active_var.set(False)

    def remove_player_action():
        tree = getattr(self, f"{team_type}_players_tree")
        selected_item = tree.selection()
        if not selected_item:
            return
            
        # Obtener datos del item seleccionado
        item = tree.item(selected_item)
        jersey_number = item['values'][0]
        
        # Eliminar del modelo
        team_controller.remove_player(jersey_number)
        
        # Actualizar treeview
        tree.delete(selected_item)
        
        # Actualizar marcador
        if hasattr(self, 'main_panel') and self.main_panel is not None:
            if hasattr(self.main_panel, 'scoreboard_window'):
                if hasattr(self.main_panel.scoreboard_window, 'refresh_player_list'):
                    self.main_panel.scoreboard_window.refresh_player_list(team_controller)

    # Botones de acción
    buttons_frame = ttk.Frame(form_panel)
    buttons_frame.grid(row=2, column=3, padx=2, pady=1)
    
    ttk.Button(buttons_frame, text="Añadir", style="PlayerForm.TButton", command=add_player_action).pack(side="left", padx=1)
    ttk.Button(buttons_frame, text="Eliminar", style="PlayerForm.TButton", command=remove_player_action).pack(side="left", padx=1)

    # Configurar columnas
    form_panel.columnconfigure(1, weight=1)

    # Frame para la lista de jugadores
    list_panel = ttk.Frame(parent_frame, padding=3)
    list_panel.pack(fill="both", expand=True, padx=2, pady=2)

    ttk.Label(list_panel, text="Jugadores:", style="PlayerForm.TLabel").pack(anchor="w", padx=2, pady=1)

    # Treeview para mostrar lista de jugadores (compacto)
    columns = ("Dorsal", "Nombre", "Titular", "Faltas")
    player_tree = ttk.Treeview(list_panel, columns=columns, height=8, show="tree headings", style="Compact.Treeview")
    player_tree.column("#0", width=0, stretch="no")
    player_tree.column("Dorsal", anchor="center", width=40)
    player_tree.column("Nombre", anchor="w", width=80)
    player_tree.column("Titular", anchor="center", width=50)
    player_tree.column("Faltas", anchor="center", width=40)
    player_tree.heading("Dorsal", text="Dorsal")
    player_tree.heading("Nombre", text="Nombre")
    player_tree.heading("Titular", text="Titular")
    player_tree.heading("Faltas", text="Faltas")
    player_tree.pack(fill="both", expand=True, padx=2, pady=1)

    setattr(self, f"{team_type}_players_tree", player_tree)
    setattr(self, f"{team_type}_players_list", [])

    # Cargar jugadores existentes
    for player in team_controller.team.players:
        status = "✓" if player.is_active else "○"
        player_tree.insert("", "end", values=(player.jersey_number, player.name, status, player.foul))


def setup_tab_ajustes(self):
    """Configura la pestaña de ajustes con personalización de colores"""
    # Crear un canvas con scrollbar para permitir scroll vertical
    canvas = tk.Canvas(self.tab_ajustes, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(self.tab_ajustes, orient="vertical", command=canvas.yview)
    
    # Frame scrolleable dentro del canvas
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Insertar el frame dentro del canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Permitir scroll con rueda del ratón
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Pack canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Botón de Joystick primero
    button_joystick_frame = ttk.Frame(scrollable_frame)
    button_joystick_frame.pack(fill="x", padx=10, pady=(10, 15))
    
    ttk.Button(
        button_joystick_frame,
        text="🎮 Configuración de Joystick",
        command=lambda: open_joystick_config_window(self)
    ).pack(fill="both", expand=True, ipady=8)
    
    # Agregar contenido de personalización de colores
    from gui.control_panel.ui_components.ui_color_customization import setup_color_customization_ui_left
    setup_color_customization_ui_left(self, scrollable_frame)


def open_joystick_config_window(control_panel_test):
    """
    Abre una ventana emergente con la configuración del joystick.
    
    Args:
        control_panel_test: Instancia de Gui_control_panel_test
    """
    # Obtener el joystick_controller del panel principal
    if not hasattr(control_panel_test, 'main_panel') or control_panel_test.main_panel is None:
        return
    
    main_panel = control_panel_test.main_panel
    if not hasattr(main_panel, 'joystick_controller'):
        return
    
    # Crear ventana emergente
    joystick_window = tk.Toplevel(control_panel_test.root)
    joystick_window.title("🎮 Configuración de Joystick")
    joystick_window.geometry("600x500")
    
    # Importar la función de setup del joystick
    from gui.control_panel.ui_components.ui_joystick import (
        create_joystick_info_section,
        create_joystick_controls_section,
        create_joystick_config_section,
        create_joystick_log_section,
        update_joystick_info
    )
    
    # Crear un namespace simulado para compatibilidad
    class JoystickWindowNamespace:
        pass
    
    joystick_ns = JoystickWindowNamespace()
    joystick_ns.frames = tk.Frame.__new__(tk.Frame)
    joystick_ns.frames.joystick = ttk.Frame(joystick_window)
    joystick_ns.frames.joystick.grid_rowconfigure(0, weight=0)
    joystick_ns.frames.joystick.grid_rowconfigure(1, weight=0)
    joystick_ns.frames.joystick.grid_rowconfigure(2, weight=0)
    joystick_ns.frames.joystick.grid_rowconfigure(3, weight=1)
    joystick_ns.frames.joystick.grid_columnconfigure(0, weight=1)
    joystick_ns.frames.joystick.pack(fill="both", expand=True)
    
    # Copiar atributos necesarios del main_panel
    joystick_ns.joystick_controller = main_panel.joystick_controller
    joystick_ns.notebook = joystick_window  # Para compatibilidad
    
    # Crear secciones de joystick
    create_joystick_info_section(joystick_ns)
    create_joystick_controls_section(joystick_ns)
    create_joystick_config_section(joystick_ns)
    create_joystick_log_section(joystick_ns)
    
    # Actualizar información
    update_joystick_info(joystick_ns)
    
    # Permitir que la ventana sea modal si se desea
    joystick_window.transient(control_panel_test.root)
    joystick_window.grab_set()