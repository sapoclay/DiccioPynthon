import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage
from tkinter import ttk
import tkinter.filedialog as filedialog
import sqlite3
import subprocess
import os
import webbrowser
from PIL import Image, ImageTk  # Necesario para redimensionar la imagen
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from updates import GitHubUpdater

class PythonConceptManagerApp:
    """
    Aplicación gráfica para gestionar categorías y conceptos de Python.

    Permite añadir, editar, eliminar y ejecutar fragmentos de código Python 
    asociados a diferentes categorías. También permite exportar la lista de 
    categorías y códigos a un archivo PDF.

    Atributos:
        root (Tk): Ventana principal de la aplicación.
        conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        cursor (sqlite3.Cursor): Cursor para ejecutar consultas SQL.
        category_listbox (tk.Listbox): Lista de categorías en la interfaz.
    """
    def __init__(self, root):
        """
        Inicializa la aplicación, configura la base de datos y crea los widgets de la interfaz.

        Parámetros:
            root (Tk): La ventana principal de la aplicación.
        """
        try:
            with open("version.txt", "r") as version_file:
                self.local_commit_hash = version_file.read().strip()
        except FileNotFoundError:
            self.local_commit_hash = ""
            messagebox.showwarning(
                "Advertencia",
                "No se encontró el archivo 'version.txt'. El sistema no podrá verificar actualizaciones correctamente."
            )
                    
        self.root = root
        self.root.title("DiccioPynthon")  # Título de la aplicación

        # Configurar la base de datos
        self.conn = sqlite3.connect("conceptos.db")
        self.cursor = self.conn.cursor()
        self.setup_database()
        
        # Variable para controlar la búsqueda
        self.search_var = tk.StringVar()
        self.filtered_categories = []  # Almacena las categorías filtradas


        # Widgets de la interfaz
        self.create_widgets()
        self.update_category_list()

        # Crear el menú superior
        self.create_menu()

    def setup_database(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT
            )
        """)
        self.conn.commit()

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
        self.category_listbox.grid(row=0, column=0, rowspan=4, padx=10, pady=10)

        # Crear un marco para los botones en dos columnas
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

        tk.Button(button_frame, text="Añadir Concepto", command=self.add_category).grid(row=0, column=0, pady=5)
        tk.Button(button_frame, text="Editar Concepto", command=self.edit_category).grid(row=1, column=0, pady=5)
        tk.Button(button_frame, text="Eliminar Concepto", command=self.delete_category).grid(row=0, column=1, pady=5)
        tk.Button(button_frame, text="Ejecutar Código", command=self.run_category_code).grid(row=1, column=1, pady=5)
        tk.Button(button_frame, text="Buscar Concepto", command=self.search_category_dialog).grid(row=2, column=0, pady=5)

    def search_category_dialog(self):
        """Muestra un cuadro de diálogo para buscar categorías por nombre."""
        search_term = simpledialog.askstring("Buscar Concepto", "Introduce el término de búsqueda:")
        if search_term:
            self.search_category(search_term)
    
    def search_category(self, search_term):
        """Filtra la lista de categorías según el término de búsqueda."""
        self.category_listbox.delete(0, tk.END)
        search_term = f"%{search_term.lower()}%"
        self.cursor.execute("SELECT name FROM categories WHERE LOWER(name) LIKE ?", (search_term,))
        categories = self.cursor.fetchall()
        for category in categories:
            self.category_listbox.insert(tk.END, category[0])
        if not categories:
            messagebox.showinfo("Sin resultados", "No se encontraron categorías que coincidan con la búsqueda.")
            
    def filter_categories(self, event=None):
        """
        Filtra las categorías en función del texto ingresado en la caja de búsqueda.
        """
        search_text = self.search_var.get().lower()
        self.filtered_categories = []

        # Filtrar las categorías que coinciden con el texto ingresado
        self.cursor.execute("SELECT name FROM categories")
        categories = [category[0] for category in self.cursor.fetchall()]

        self.filtered_categories = [
            category for category in categories if search_text in category.lower()
        ]

        # Actualizar el contenido de la lista
        self.category_listbox.delete(0, tk.END)
        for category in self.filtered_categories:
            self.category_listbox.insert(tk.END, category)

    def update_category_list(self):
        """
        Actualiza la lista de categorías en la interfaz, recuperando los nombres
        desde la base de datos.
        """
        self.category_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name FROM categories")
        categories = self.cursor.fetchall()
        for category in categories:
            self.category_listbox.insert(tk.END, category[0])
            
    def create_menu(self):
        """Crea el menú superior con las opciones Archivo y Preferencias."""
        menu_bar = tk.Menu(self.root)

        # Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Ollama", command=self.run_ollama) 
        file_menu.add_separator()
        file_menu.add_command(label="Exportar a PDF", command=self.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Preferencias
        preferences_menu = tk.Menu(menu_bar, tearoff=0)
        preferences_menu.add_command(label="Tutoriales Básicos", command=self.abrir_tutoriales)
        preferences_menu.add_separator()
        preferences_menu.add_command(label="Importar BD", command=self.fusionar_base_datos)
        preferences_menu.add_separator()
        preferences_menu.add_command(label="Buscar Actualizaciones", command=self.buscar_actualizaciones)
        preferences_menu.add_separator()
        preferences_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Preferencias", menu=preferences_menu)

        # Configurar el menú en la ventana principal
        self.root.config(menu=menu_bar)
    
    def run_ollama(self):
        """Verifica si 'ollama' está instalado y ejecuta 'ollama run llama3.2'."""
        try:
            # Verificar si el comando 'ollama' está disponible
            subprocess.run(["ollama", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            # Ejecutar 'ollama run llama3.2' en una nueva terminal
            if os.name == "nt":  # Windows
                subprocess.Popen(["start", "cmd", "/c", "ollama run llama3.2"], shell=True)
            else:  # Linux/Unix
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "ollama run llama3.2"], shell=False)

        except FileNotFoundError:
            # Mostrar mensaje si 'ollama' no está instalado
            messagebox.showerror(
                "Ollama no disponible",
                "Ollama no está disponible en este sistema.\nPuedes descargarlo desde: https://ollama.com"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al intentar ejecutar Ollama:\n{e}")

    def abrir_tutoriales(self):
        """Abre un enlace de tutoriales en el navegador"""
        enlace_tutoriales = "https://github.com/sapoclay/basicos-python"
        webbrowser.open(enlace_tutoriales)
        
    def export_to_pdf(self):
        """
        Exporta el contenido de la base de datos a un archivo PDF.
        
        Recupera todas las categorías y sus códigos asociados y crea un archivo
        PDF con el contenido formateado.
        """
        categories = self.fetch_categories_from_db()

        # Cuadro de diálogo para seleccionar la ubicación y nombre del archivo
        pdf_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Guardar PDF como..."
        )

        if not pdf_filename:
            # Si el usuario cancela, no hacemos nada
            return

        # Crear el archivo PDF
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        y_position = height - 40  # Posición inicial de la primera categoría

        for category in categories:
            title = category[0]
            code = category[1] if category[1] else "No hay código asociado"
            
            # Escribir el título de la categoría
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y_position, f"Título: {title}")
            y_position -= 20

            # Escribir el código de la categoría (si existe)
            c.setFont("Helvetica", 10)
            c.drawString(40, y_position, f"Código:")
            y_position -= 15

            # Asegurarse de que el código no se salga de la página
            lines = code.splitlines()

            for line in lines:
                if y_position < 40:
                    c.showPage()  # Si llegamos al final de la página, creamos una nueva
                    c.setFont("Helvetica", 10)
                    y_position = height - 40

                try:
                    # Asegurarse de que line es una cadena de texto (str)
                    c.drawString(40, y_position, line)
                    y_position -= 15
                except Exception as e:
                    print(f"Error al escribir línea: {line}. Detalles: {e}")

            # Espacio entre categorías
            y_position -= 20

        # Guardar el PDF
        c.save()
        messagebox.showinfo("Exportación Completa", f"El contenido se ha exportado a {pdf_filename}")

    def fetch_categories_from_db(self):
        """
        Recupera todas las categorías y su código de la base de datos.
        
        Devuelve una lista de tuplas con el nombre de la categoría y su código asociado.
        
        Retorno:
            list: Lista de tuplas con el nombre de la categoría y su código.
        """
        self.cursor.execute("SELECT name, code FROM categories")
        return self.cursor.fetchall()
    
    def show_about(self):
        """Abre una ventana de 'About' con información sobre la aplicación."""
        about_window = tk.Toplevel(self.root)
        about_window.title("Acerca de")
        about_window.geometry("400x400")

        img = Image.open("img/logo.png")
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)
        label_img = tk.Label(about_window, image=img)
        label_img.image = img  # Necesario para mantener la referencia de la imagen
        label_img.pack(pady=10)

        description = """Esta aplicación permite al usuario gestionar conceptos y códigos de Python.
Permite añadir, editar, eliminar y ejecutar códigos Python asociados los conceptos guardados."""
        label_description = tk.Label(about_window, text=description, justify="center", wraplength=350)
        label_description.pack(pady=10)

        label_link = tk.Label(about_window, text="Visita el repositorio en GitHub", fg="blue", cursor="hand2")
        label_link.pack(pady=10)
        label_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/sapoclay/DiccioPynthon"))

    def update_category_list(self):
        """
        Actualiza la lista de categorías en la interfaz, recuperando los nombres
        desde la base de datos.
        """
        self.category_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name FROM categories")
        categories = self.cursor.fetchall()
        for category in categories:
            self.category_listbox.insert(tk.END, category[0])

    def open_code_editor(self, category_name="", initial_code=""):
        """Abre una ventana dividida para editar tanto el título como el código con formato."""
        editor_window = tk.Toplevel(self.root)
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


    def add_category(self):
        """Añade una nueva categoría con código opcional."""
        category_name = simpledialog.askstring("Añadir Concepto", "Introduce el nombre del concepto:")
        if category_name:
            title, code_snippet = self.open_code_editor(category_name)

            try:
                self.cursor.execute("INSERT INTO categories (name, code) VALUES (?, ?)", 
                                    (category_name, code_snippet))
                self.conn.commit()
                messagebox.showinfo("Éxito", f"Concepto '{category_name}' añadido.")
                self.update_category_list()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"El concepto '{category_name}' ya existe.")

    def edit_category(self):
        """Edita el título o el código de un concepto seleccionado."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un concepto para editar.")
            return

        old_name = self.category_listbox.get(selected[0])
        self.cursor.execute("SELECT code FROM categories WHERE name = ?", (old_name,))
        current_code = self.cursor.fetchone()[0] or ""
        title, new_code = self.open_code_editor(old_name, current_code)

        # Verificar si el usuario cerró la ventana sin realizar cambios
        if title == "":
            messagebox.showwarning("Advertencia", "El título no pueden estar vacíos.")
            return

        # Verificar si el nuevo título ya existe
        if title != old_name:  # Solo verificar si el título ha cambiado
            self.cursor.execute("SELECT COUNT(*) FROM categories WHERE name = ?", (title,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"El concepto '{title}' ya existe. Elige un nombre diferente.")
                return

        # Si el título y el código no están vacíos y el título es único, proceder con la actualización
        self.cursor.execute("UPDATE categories SET name = ?, code = ? WHERE name = ?", (title, new_code, old_name))
        self.conn.commit()
        messagebox.showinfo("Éxito", f"Categoría '{old_name}' actualizada.")
        self.update_category_list()



    def delete_category(self):
        """Elimina la categoría seleccionada."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un concepto para eliminar.")
            return

        category_name = self.category_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el concepto '{category_name}'?")
        if confirm:
            self.cursor.execute("DELETE FROM categories WHERE name = ?", (category_name,))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Concepto '{category_name}' eliminado.")
            self.update_category_list()

    def run_category_code(self):
        """Ejecuta el código asociado al concepto seleccionado en una nueva terminal."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un concepto para ejecutar el código asociado.")
            return

        category_name = self.category_listbox.get(selected[0])
        self.cursor.execute("SELECT code FROM categories WHERE name = ?", (category_name,))
        result = self.cursor.fetchone()
        if result and result[0]:
            code_snippet = result[0]
            try:
                temp_filename = "temp_code.py"
                # Asegurarse de que el código sea una cadena de texto antes de escribirlo
                with open(temp_filename, "w", encoding="utf-8") as temp_file:
                    temp_file.write(str(code_snippet))  # Convertimos el código a str si es necesario

                if os.name == "nt": 
                    subprocess.Popen(["start", "cmd", "/c", f"python {temp_filename}  & pause"], shell=True)
                else:
                    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"python3 {temp_filename} && read -p 'Press any key to continue...'"], shell=False)

            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar el código: {e}")
        else:
            messagebox.showinfo("Info", f"El concepto '{category_name}' no tiene código asociado que se puede ejecutar.")

    def fusionar_base_datos(self):
        """Permite importar los datos de un archivo .db y fusionarlos con la base de datos actual."""
        from tkinter import filedialog, messagebox

        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo .db",
            filetypes=[("Archivos SQLite", "*.db"), ("Todos los archivos", "*.*")]
        )

        if not file_path:
            messagebox.showinfo("Info", "No se seleccionó ningún archivo.")
            return

        try:
            # Conectar con la base de datos importada
            imported_conn = sqlite3.connect(file_path)
            imported_cursor = imported_conn.cursor()

            # Obtener las tablas de la base de datos importada
            imported_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = imported_cursor.fetchall()

            for table_name, in tables:
                # Leer datos de cada tabla
                imported_cursor.execute(f"SELECT * FROM {table_name}")
                rows = imported_cursor.fetchall()

                # Obtener las columnas de la tabla
                imported_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in imported_cursor.fetchall()]
                column_list = ", ".join(columns)
                placeholders = ", ".join(["?"] * len(columns))

                # Insertar datos en la base de datos actual
                for row in rows:
                    self.cursor.execute(f"INSERT OR IGNORE INTO {table_name} ({column_list}) VALUES ({placeholders})", row)

            self.conn.commit()
            imported_conn.close()

            # Recargar los datos en la lista de categorías
            self.update_category_list()


            messagebox.showinfo("Éxito", "Los datos de la base de datos importada se fusionaron correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al fusionar la base de datos: {e}")


    def buscar_actualizaciones(self):
        """Busca actualizaciones desde el repositorio de GitHub."""
        # Configuración del actualizador
        repo_owner = "sapoclay"  # Reemplaza con tu usuario de GitHub.
        repo_name = "DiccioPynthon"  # Reemplaza con el nombre del repositorio.

        updater = GitHubUpdater(repo_owner, repo_name, self.local_commit_hash)
        try:
            hay_actualizaciones = updater.check_for_updates()

            if hay_actualizaciones:
                respuesta = messagebox.askyesno(
                    "Actualización Disponible",
                    "Hay una nueva versión disponible. ¿Deseas descargarla?"
                )
                if respuesta:
                    updater.download_latest_version()
                    messagebox.showinfo("Actualización", "La última versión ha sido descargada.")
            else:
                messagebox.showinfo("Actualización", "El código está actualizado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar actualizaciones: {str(e)}")


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
