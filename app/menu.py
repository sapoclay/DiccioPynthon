import tkinter as tk
from .about import show_about  
from .ollama import run_ollama 
from .search import search_python_docs, search_python_packages, abrir_tutoriales
from .export_to_pdf import export_to_pdf

def create_menu(self, open_update_manager):
        """Crea el menú superior con las opciones Archivo y Preferencias."""
        menu_bar = tk.Menu(self.root)

        # Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff=0) # tearoff=0 elimina la línea punteada
        file_menu.add_command(label="Ollama", command=lambda: run_ollama(self.root)) 
        file_menu.add_separator()
        file_menu.add_command(label="Exportar a PDF", command=lambda: export_to_pdf(self.db_actions))
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Preferencias
        preferences_menu = tk.Menu(menu_bar, tearoff=0)

        preferences_menu.add_command(label="Importar BD", command=self.fusionar_base_datos)
        preferences_menu.add_separator()
        preferences_menu.add_command(label="Buscar Actualizaciones", command=open_update_manager)  # Usar el argumento recibido
        preferences_menu.add_separator()
        preferences_menu.add_command(label="About", command=lambda: show_about(self.root))
        menu_bar.add_cascade(label="Preferencias", menu=preferences_menu)
        
        # Menú Python
        menu_python = tk.Menu(menu_bar, tearoff=0)
        menu_python.add_command(label="Tutoriales Básicos", command=lambda: abrir_tutoriales(self.root))
        menu_python.add_separator()
        menu_python.add_command(label="Buscar en Documentación Python",  command=lambda: search_python_docs(self.root))
        menu_python.add_separator()
        menu_python.add_command(label="Buscar Paquetes Python",  command=lambda: search_python_packages(self.root)) 
        menu_bar.add_cascade(label="Python", menu=menu_python)

        # Configurar el menú en la ventana principal
        self.root.config(menu=menu_bar)
        

