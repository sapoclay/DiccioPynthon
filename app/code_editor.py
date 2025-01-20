import tkinter as tk
from app.config import load_config  # Importa la función para cargar la configuración
from app.themes import apply_theme, THEMES  
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from tkinter import filedialog
from tkinter import PhotoImage

def open_code_editor(root, category_name="", initial_code=""):
    """Abre una ventana dividida para editar tanto el título como el código con formato."""
    editor_window = tk.Toplevel(root)  # Usar el parámetro root
    editor_window.title(f"Añadir/Editar Categoría - {category_name}")
    editor_window.geometry("600x400")

    # Cargar el tema desde el archivo de configuración
    theme_name = load_config()  # Llamamos a load_config para obtener el tema guardado
    apply_theme(editor_window, theme_name)  # Aplicamos el tema a la ventana del editor

    # Obtener los colores del tema actual
    theme = THEMES.get(theme_name, THEMES["light"])
    bg_color = theme["bg"]
    fg_color = theme["fg"]
    entry_bg_color = theme["entry_bg"]
    entry_fg_color = theme["entry_fg"]
    frame_bg_color = theme["button_bg"]  # Usamos el color del botón para el fondo del frame en tema oscuro
    highlight_color = "#404040" if theme_name == "dark" else "#D3D3D3"  # Color de resaltado para la línea actual

    def save_code():
        """Guarda el título y el código con formato."""
        saved_title_code["title"] = title_entry.get("1.0", "end-1c")
        saved_title_code["code"] = code_entry.get("1.0", "end-1c")
        nonlocal is_saved
        is_saved = True  # Indicamos que se ha guardado
        editor_window.destroy()
        
    def load_file():
        """Carga el contenido de un archivo en el área de código."""
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                code_entry.delete("1.0", tk.END)
                code_entry.insert("1.0", file.read())

    # Cargar imágenes para los botones con tamaño máximo
    # Ajustar el tamaño de las imágenes a 50x50 píxeles
    load_icon = tk.PhotoImage(file="./img/loadfile.png").subsample(8, 8)  # Ajustar a 50x50 si la imagen original es 200x200
    save_icon = tk.PhotoImage(file="./img/savefile.png").subsample(8, 8)


    # Crear un frame para alinear los botones en la misma línea
    button_frame = tk.Frame(editor_window, bg=bg_color)
    button_frame.pack(fill="x", padx=10, pady=5, anchor="w")  # Expandir horizontalmente y alinear a la izquierda

    # Botón para cargar archivo con imagen
    load_button = tk.Button(button_frame, image=load_icon, command=load_file, bg=theme["button_bg"], fg=theme["button_fg"])
    load_button.image = load_icon  # Evitar que la imagen sea eliminada por el recolector de basura
    load_button.pack(side=tk.LEFT, padx=5)

    # Botón para guardar archivo con imagen
    save_button = tk.Button(button_frame, image=save_icon, command=save_code, bg=theme["button_bg"], fg=theme["button_fg"])
    save_button.image = save_icon
    save_button.pack(side=tk.LEFT, padx=5)
    
    # Crear un PanedWindow para dividir la ventana en dos secciones
    paned_window = tk.PanedWindow(editor_window, orient=tk.HORIZONTAL, bg=bg_color)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Título con barra de desplazamiento vertical
    title_frame = tk.Frame(paned_window, bg=frame_bg_color)
    title_label = tk.Label(title_frame, text="CONCEPTO A GUARDAR", font=("Arial", 10, "bold"), bg=frame_bg_color, fg=fg_color)
    title_label.pack(anchor="w", padx=5, pady=2)

    title_scrollbar = tk.Scrollbar(title_frame, orient=tk.VERTICAL)
    title_entry = tk.Text(title_frame, wrap="word", height=10, width=30, yscrollcommand=title_scrollbar.set, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
    title_scrollbar.config(command=title_entry.yview)
    title_scrollbar.pack_forget()  # Ocultar scrollbar
    title_entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    title_entry.insert("1.0", category_name)
    paned_window.add(title_frame)

    # Código con barra de desplazamiento vertical y numeración
    code_frame = tk.Frame(paned_window, bg=frame_bg_color)
    code_label = tk.Label(code_frame, text="CÓDIGO ASOCIADO AL CONCEPTO", font=("Arial", 10, "bold"), bg=frame_bg_color, fg=fg_color)
    code_label.pack(anchor="w", padx=5, pady=2)

    # Frame para el código
    code_inner_frame = tk.Frame(code_frame, bg=frame_bg_color)
    code_inner_frame.pack(fill=tk.BOTH, expand=True)

    # Widget para los números de línea
    line_numbers = tk.Text(code_inner_frame, width=5, height=10, bg=entry_bg_color, fg=entry_fg_color, padx=5, pady=2, wrap="none", state="disabled", font=("Courier", 12))
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)

    # Widget de entrada para código
    code_scrollbar = tk.Scrollbar(code_inner_frame, orient=tk.VERTICAL)
    code_entry = tk.Text(code_inner_frame, wrap="word", height=10, width=30, yscrollcommand=code_scrollbar.set, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color, font=("Courier", 12))
    code_scrollbar.config(command=code_entry.yview)
    code_scrollbar.pack_forget()  # Ocultar scrollbar
    code_entry.pack(expand=True, fill=tk.BOTH)
    code_entry.insert("1.0", initial_code)

    paned_window.add(code_frame)

    def update_line_numbers(event=None):
        """Actualiza la numeración de líneas en el widget de los números de línea"""
        code_text = code_entry.get("1.0", "end-1c")
        lines = code_text.split("\n")

        # Crear la numeración de líneas con un formato consistente
        numbered_lines = [f"{i + 1:4}" for i in range(len(lines))]

        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        line_numbers.insert("1.0", "\n".join(numbered_lines))
        line_numbers.config(state="disabled")
        line_numbers.yview_moveto(code_entry.yview()[0])

    def highlight_current_line(event=None):
        """Resalta la línea actual en el área de código"""
        code_entry.tag_remove("current_line", 1.0, "end")
        code_entry.tag_add("current_line", "insert linestart", "insert lineend+1c")
        code_entry.tag_configure("current_line", background=highlight_color)

    def syntax_highlight(event=None):
        """Aplica resaltado de sintaxis al texto en el área de código"""
        code_entry.mark_set("range_start", "1.0")
        data = code_entry.get("1.0", "end-1c")
        
        for token, content in lex(data, PythonLexer()):
            code_entry.mark_set("range_end", "range_start + %dc" % len(content))
            code_entry.tag_add(str(token), "range_start", "range_end")
            code_entry.mark_set("range_start", "range_end")

        apply_syntax_theme()

    def apply_syntax_theme():
        """Aplica el tema de sintaxis según el tema seleccionado"""
        style = get_style_by_name("monokai" if theme_name == "dark" else "default")
        for token, options in style:
            fg = options["color"]
            if fg:
                code_entry.tag_configure(str(token), foreground="#" + fg)
            else:
                code_entry.tag_configure(str(token), foreground=fg_color)

    def sync_scroll(*args):
        """Sincroniza el desplazamiento entre el código y los números de línea"""
        code_entry.yview_moveto(args[0])
        line_numbers.yview_moveto(args[0])

    # Sincronizar desplazamiento entre la numeración y el área de código
    code_entry.config(yscrollcommand=sync_scroll)
    line_numbers.config(yscrollcommand=sync_scroll)

    # Actualiza la numeración de líneas, resalta la línea actual y aplica resaltado de sintaxis al escribir en el código
    code_entry.bind("<KeyRelease>", lambda event: (update_line_numbers(), highlight_current_line(), syntax_highlight()))
    code_entry.bind("<MouseWheel>", update_line_numbers)  # Sincroniza al usar la rueda del ratón

    # Mantener la sincronización del desplazamiento sin necesidad de eventos extra
    code_entry.bind("<Configure>", update_line_numbers)  # Actualiza los números al cambiar el tamaño

    def auto_scroll(event):
        """Permitir el desplazamiento automático del cursor"""
        code_entry.see(tk.END)
        update_line_numbers()
        highlight_current_line()
        syntax_highlight()

    code_entry.bind("<KeyRelease-Return>", auto_scroll)

    # Inicializar la numeración de líneas, el resaltado de la línea actual y el resaltado de sintaxis
    update_line_numbers()
    highlight_current_line()
    syntax_highlight()

    saved_title_code = {"title": "", "code": ""}
    is_saved = False  # Variable para controlar si se ha guardado
    
    # Función que controla el cierre de la ventana
    def on_close():
        nonlocal is_saved
        if not is_saved:  # Si no se ha guardado
            editor_window.destroy()  # Cerrar la ventana
        else:
            editor_window.destroy()  # Si ya se guardó, se cierra normalmente

    editor_window.protocol("WM_DELETE_WINDOW", on_close)  # Interceptar el evento de cierre

    editor_window.wait_window()  # Esperar que se cierre la ventana
    return saved_title_code["title"], saved_title_code["code"]

