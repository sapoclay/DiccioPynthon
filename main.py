import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import subprocess
import os
from app.code_editor import open_code_editor
from app.menu import create_menu
from app.updates import check_for_updates
from app.db_actions import DatabaseActions

class PythonConceptManagerApp:
    """
    Aplicación gráfica para gestionar categorías y conceptos de Python.

    Permite añadir, editar, eliminar y ejecutar fragmentos de código Python 
    asociados a diferentes categorías.
    """
    def __init__(self, root):
        """
        Inicializa la aplicación, configura la base de datos y crea los widgets de la interfaz.

        :param root: La ventana principal de la aplicación.
        """
        self.root = root
        self.root.title("DiccioPython")  # Título de la aplicación

        # Conexión a la base de datos
        self.db_actions = DatabaseActions("conceptos.db")

        # Variable para búsqueda
        self.search_var = tk.StringVar()
        self.filtered_categories = []

        # Configurar interfaz gráfica
        self.create_widgets()
        self.update_category_list()

        # Crear el menú de la aplicación
        self.create_menu()
    
    def create_menu(self):
        create_menu(self, self.open_update_manager)
                
    def open_update_manager(self):
        """Inicia el gestor de actualizaciones."""
        check_for_updates()
        

    def create_widgets(self):
        """
        Crea los widgets de la interfaz gráfica para mostrar la lista de categorías
        y los botones de acción.
        """
        # Caja de búsqueda
        tk.Label(self.root, text="Buscar Categorías:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        search_entry = tk.Entry(self.root, textvariable=self.search_var)
        search_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        search_entry.bind("<<KeyRelease>>", self.filter_categories)

        # Listbox para las categorías
        self.category_listbox = tk.Listbox(self.root, height=15, width=40)
        self.category_listbox.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")  # Expande en todas direcciones

        # Configurar la expansión de las filas y columnas
        self.root.grid_rowconfigure(0, weight=1, minsize=200)  # La primera fila donde está el Listbox
        self.root.grid_columnconfigure(0, weight=1, minsize=200)  # La columna donde está el Listbox

        # Crear un marco para los botones en dos columnas
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

        tk.Button(button_frame, text="Añadir Concepto", command=self.add_category).grid(row=0, column=0, pady=5)
        tk.Button(button_frame, text="Editar Concepto", command=self.edit_category).grid(row=1, column=0, pady=5)
        tk.Button(button_frame, text="Eliminar Concepto", command=self.delete_category).grid(row=0, column=1, pady=5)
        tk.Button(button_frame, text="Ejecutar Código", command=self.run_category_code).grid(row=1, column=1, pady=5)
        tk.Button(button_frame, text="Buscar Concepto", command=self.search_category_dialog).grid(row=2, column=0, pady=5)

        # Asegúrate de que el resto de las filas y columnas también puedan expandirse según sea necesario
        self.root.grid_rowconfigure(1, weight=0)  # Fila para la entrada de búsqueda
        self.root.grid_rowconfigure(2, weight=0)  # Fila para los botones
        self.root.grid_columnconfigure(1, weight=0)  # Columna para los botones
        self.root.grid_columnconfigure(2, weight=0)  # Columna para los botones

        
    def search_category_dialog(self):
        """Muestra un cuadro de diálogo para buscar categorías por nombre."""
        search_term = simpledialog.askstring("Buscar Concepto", "Introduce el término de búsqueda:")
        if search_term:
            self.search_category(search_term)
    
    def filter_categories(self, event=None):
        """Filtra las categorías según el texto ingresado en la búsqueda."""
        search_text = self.search_var.get().lower()
        categories = self.db_actions.fetch_categories_from_db()
        self.category_listbox.delete(0, tk.END)
        for name, _ in categories:
            if search_text in name.lower():
                self.category_listbox.insert(tk.END, name)


    def update_category_list(self):
        """Actualiza la lista de categorías en la interfaz."""
        self.category_listbox.delete(0, tk.END)
        categories = self.db_actions.fetch_categories_from_db()
        for name, _ in categories:
            self.category_listbox.insert(tk.END, name)
            

    def search_category(self, search_term):
        categories = self.db_actions.search_category(search_term)
        self.category_listbox.delete(0, tk.END)
        for category in categories:
            self.category_listbox.insert(tk.END, category[0])
        if not categories:
            messagebox.showinfo("Sin resultados", "No se encontraron categorías que coincidan con la búsqueda.")

    def update_category_list(self):
        self.category_listbox.delete(0, tk.END)
        categories = self.db_actions.update_category_list()
        for category in categories:
            self.category_listbox.insert(tk.END, category[0])

    def add_category(self):
        """Añade una nueva categoría con código opcional."""
        category_name = simpledialog.askstring("Añadir Concepto", "Introduce el nombre del concepto:")
        if category_name:
            title, code_snippet = open_code_editor(self.root, category_name)
            try:
                self.db_actions.add_category(title, code_snippet)
                messagebox.showinfo("Éxito", f"Concepto '{title}' añadido.")
                self.update_category_list()
            except ValueError as e:
                messagebox.showerror("Error", str(e))


    def edit_category(self):
        """Edita el título o el código de un concepto seleccionado."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un concepto para editar.")
            return

        old_name = self.category_listbox.get(selected[0])
        categories = self.db_actions.fetch_categories_from_db()
        current_code = next((code for name, code in categories if name == old_name), "")

        title, new_code = open_code_editor(self.root, old_name, current_code)

        if title:
            try:
                self.db_actions.edit_category(old_name, title, new_code)
                messagebox.showinfo("Éxito", f"Concepto '{old_name}' actualizado.")
                self.update_category_list()
            except ValueError as e:
                messagebox.showerror("Error", str(e))


    def delete_category(self):
        """Elimina la categoría seleccionada."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un concepto para eliminar.")
            return

        category_name = self.category_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el concepto '{category_name}'?")
        if confirm:
            self.db_actions.delete_category(category_name)
            messagebox.showinfo("Éxito", f"Concepto '{category_name}' eliminado.")
            self.update_category_list()


    def run_category_code(self):
        """Ejecuta el código asociado al concepto seleccionado en una nueva terminal."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un concepto para ejecutar el código asociado.")
            return

        category_name = self.category_listbox.get(selected[0])
        
        # Obtener las categorías de la base de datos mediante la función fetch_categories_from_db
        categories = self.db_actions.fetch_categories_from_db()
        
        # Buscar el código correspondiente al nombre de la categoría seleccionada
        code_snippet = next((code for name, code in categories if name == category_name), None)

        if code_snippet:
            try:
                temp_filename = "temp_code.py"
                # Asegurarse de que el código sea una cadena de texto antes de escribirlo
                with open(temp_filename, "w", encoding="utf-8") as temp_file:
                    temp_file.write(str(code_snippet))  # Convertimos el código a str si es necesario

                if os.name == "nt":  # Para Windows
                    subprocess.Popen(["start", "cmd", "/c", f"python {temp_filename} & pause"], shell=True)
                else:  # Para Linux/MacOS
                    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"python3 {temp_filename}; read -p 'Press any key to continue...'"], shell=False)

            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar el código: {e}")
        else:
            messagebox.showinfo("Info", f"El concepto '{category_name}' no tiene código asociado que se puede ejecutar.")

    def fusionar_base_datos(self):
        """Llama al método para fusionar bases de datos y actualiza el listado de conceptos."""
        # Ruta de la base de datos actual (conceptos.db) en el mismo directorio que main.py
        db_path = os.path.join(os.path.dirname(__file__), "conceptos.db")
        
        # Abrir el selector de archivos para que el usuario seleccione la base de datos a importar
        imported_db_path = filedialog.askopenfilename(
            title="Seleccionar base de datos a importar",
            filetypes=[("Archivos de base de datos", "*.db")]
        )
        
        # Verificar si se seleccionó una base de datos
        if not imported_db_path:
            messagebox.showwarning("No seleccionada", "No se seleccionó ninguna base de datos para importar.")
            return

        # Llamar a la función fusionar_base_datos con las rutas adecuadas
        result = self.db_actions.fusionar_base_datos(db_path, imported_db_path)
        
        # Mostrar el resultado en un mensaje
        messagebox.showinfo("Resultado de la fusión", result)
        
        # Después de la fusión, actualizamos el Listbox con los nuevos conceptos
        self.actualizar_listado_conceptos()

    def actualizar_listado_conceptos(self):
        """Recarga los conceptos desde la base de datos y actualiza el Listbox."""
        # Limpiar el Listbox
        self.category_listbox.delete(0, tk.END)
        
        # Recuperar todos los conceptos de la base de datos
        categories = self.db_actions.fetch_categories_from_db()
        
        # Agregar los conceptos al Listbox
        for category in categories:
            self.category_listbox.insert(tk.END, category[0])  # `category[0]` es el nombre de la categoría



if __name__ == "__main__":
    """
    Punto de entrada principal para ejecutar la aplicación.

    Si el archivo es ejecutado directamente, crea una ventana principal de Tkinter,
    instancia la aplicación `PythonConceptManagerApp` y entra en el bucle principal de la interfaz gráfica.

    Este bloque asegura que la aplicación solo se ejecute cuando el script es ejecutado directamente,
    y no cuando se importa como un módulo.
    """
    root = tk.Tk()  # Crea la ventana principal de la aplicación.
    app = PythonConceptManagerApp(root)  # Crea una instancia de la aplicación.
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica.
