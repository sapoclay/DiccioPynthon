import tkinter as tk
from .about import show_about  
from .ollama import run_ollama 
from .search import search_python_docs, search_python_packages, abrir_tutoriales
from .export_to_pdf import export_to_pdf
from app.themes import apply_theme, apply_theme_and_restart


def create_menu(self, open_update_manager):
    """Crea el menú superior con las opciones Archivo y Preferencias."""
    menu_bar = tk.Menu(self.root)

    # Menú Archivo
    file_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 elimina la línea punteada
    file_menu.add_command(label="Ollama", command=lambda: run_ollama(self.root)) 
    file_menu.add_separator()
    file_menu.add_command(label="Exportar a PDF", command=lambda: export_to_pdf(self.db_actions))
    file_menu.add_separator()
    file_menu.add_command(label="Salir", command=self.root.quit)
    menu_bar.add_cascade(label="Archivo", menu=file_menu)

    # Menú Preferencias
    preferences_menu = tk.Menu(menu_bar, tearoff=0)
    preferences_menu.add_command(label="Tema Claro", command=lambda: apply_theme_and_restart(self.root, "light", self))
    preferences_menu.add_command(label="Tema Oscuro", 
                             command=lambda: apply_theme_and_restart(self.root, "dark", self))
    preferences_menu.add_separator()
    preferences_menu.add_command(label="Importar BD", command=self.fusionar_base_datos)
    preferences_menu.add_separator()
    preferences_menu.add_command(label="Buscar Actualizaciones", command=open_update_manager)  # Usar el argumento recibido
    preferences_menu.add_separator()
    preferences_menu.add_command(label="About", command=lambda: show_about(self.root, self.current_theme)) 
    menu_bar.add_cascade(label="Preferencias", menu=preferences_menu)

    # Menú Python
    menu_python = tk.Menu(menu_bar, tearoff=0)
    menu_python.add_command(label="Tutoriales Básicos", command=lambda: abrir_tutoriales(self.root))
    menu_python.add_separator()
    menu_python.add_command(label="Buscar en Documentación Python",  command=lambda: search_python_docs(self.root))
    menu_python.add_separator()
    menu_python.add_command(label="Buscar Paquetes Python",  command=lambda: search_python_packages(self.root)) 
    menu_bar.add_cascade(label="Python", menu=menu_python)

    # Guardar la referencia al menú
    self.root.menubar = menu_bar

    # Configurar el menú en la ventana principal
    self.root.config(menu=menu_bar)

    # Aplicar el tema a la ventana y a los menús de forma inmediata
    if hasattr(self.root, 'current_theme'):
        apply_theme(self.root, self.root.current_theme)
        apply_theme(menu_bar, self.root.current_theme)  # Asegurarse de aplicar el tema también a los menús
    else:
        # Si no tiene tema actual, se configura el predeterminado
        self.root.current_theme = "light"  # O "dark", según desees como predeterminado
        apply_theme(self.root, self.root.current_theme)
        apply_theme(menu_bar, self.root.current_theme)  # Asegurarse de aplicar el tema también a los menús
