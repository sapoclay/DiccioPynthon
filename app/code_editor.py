import tkinter as tk
from tkinter import messagebox

def open_code_editor(root, category_name="", initial_code=""):
    """Abre una ventana dividida para editar tanto el título como el código con formato."""
    editor_window = tk.Toplevel(root)  # Usar el parámetro root
    editor_window.title(f"Añadir/Editar Categoría - {category_name}")
    editor_window.geometry("600x400")

    # Crear un PanedWindow para dividir la ventana en dos secciones
    paned_window = tk.PanedWindow(editor_window, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Título con barra de desplazamiento vertical
    title_frame = tk.Frame(paned_window)

    # Título encima de la caja de texto
    title_label = tk.Label(title_frame, text="CONCEPTO A GUARDAR", font=("Arial", 10, "bold"))
    title_label.pack(anchor="w", padx=5, pady=2)

    title_scrollbar = tk.Scrollbar(title_frame, orient=tk.VERTICAL)
    title_entry = tk.Text(title_frame, wrap="word", height=10, width=30, yscrollcommand=title_scrollbar.set)
    title_scrollbar.config(command=title_entry.yview)
    title_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    title_entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    title_entry.insert("1.0", category_name)
    paned_window.add(title_frame)

    # Código con barra de desplazamiento vertical
    code_frame = tk.Frame(paned_window)

    # Título encima de la caja de texto
    code_label = tk.Label(code_frame, text="CÓDIGO ASOCIADO AL CONCEPTO", font=("Arial", 10, "bold"))
    code_label.pack(anchor="w", padx=5, pady=2)

    code_scrollbar = tk.Scrollbar(code_frame, orient=tk.VERTICAL)
    code_entry = tk.Text(code_frame, wrap="word", height=10, width=30, yscrollcommand=code_scrollbar.set)
    code_scrollbar.config(command=code_entry.yview)
    code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    code_entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    code_entry.insert("1.0", initial_code)
    paned_window.add(code_frame)

    saved_title_code = {"title": "", "code": ""}
    is_saved = False  # Variable para controlar si se ha guardado

    def save_code():
        """Guarda el título y el código con formato."""
        saved_title_code["title"] = title_entry.get("1.0", "end-1c")
        saved_title_code["code"] = code_entry.get("1.0", "end-1c")
        editor_window.destroy()
        nonlocal is_saved
        is_saved = True  # Indicamos que se ha guardado

    save_button = tk.Button(editor_window, text="Guardar", command=save_code)
    save_button.pack(pady=10)

    # Función que controla el cierre de la ventana
    def on_close():
        if not is_saved:  # Si no se ha guardado
            # Mostrar un mensaje de confirmación
            confirm = messagebox.askyesno("Confirmar", "¿Seguro que deseas salir sin guardar los cambios?")
            if confirm:
                editor_window.destroy()  # Cerrar la ventana
        else:
            editor_window.destroy()  # Si ya se guardó, se cierra normalmente

    editor_window.protocol("WM_DELETE_WINDOW", on_close)  # Interceptar el evento de cierre

    editor_window.wait_window()  # Esperar que se cierre la ventana
    return saved_title_code["title"], saved_title_code["code"]
