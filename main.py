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
        self.root = root
        self.root.title("DiccioPynthon")  # Título de la aplicación

        # Configurar la base de datos
        self.conn = sqlite3.connect("conceptos.db")
        self.cursor = self.conn.cursor()
        self.setup_database()

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
        self.category_listbox = tk.Listbox(self.root, height=15, width=40)
        self.category_listbox.grid(row=0, column=0, rowspan=4, padx=10, pady=10)

        # Crear un marco para los botones en dos columnas
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

        tk.Button(button_frame, text="Añadir Categoría", command=self.add_category).grid(row=0, column=0, pady=5)
        tk.Button(button_frame, text="Editar Categoría", command=self.edit_category).grid(row=1, column=0, pady=5)
        tk.Button(button_frame, text="Eliminar Categoría", command=self.delete_category).grid(row=0, column=1, pady=5)
        tk.Button(button_frame, text="Ejecutar Categoría", command=self.run_category_code).grid(row=1, column=1, pady=5)

    def create_menu(self):
        """Crea el menú superior con las opciones Archivo y Preferencias."""
        menu_bar = tk.Menu(self.root)

        # Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exportar a PDF", command=self.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Preferencias
        preferences_menu = tk.Menu(menu_bar, tearoff=0)
        preferences_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Preferencias", menu=preferences_menu)

        # Configurar el menú en la ventana principal
        self.root.config(menu=menu_bar)

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

        description = """Esta aplicación gestiona categorías y conceptos de Python.
Permite añadir, editar, eliminar y ejecutar código Python asociado a diferentes categorías."""
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
        title_scrollbar = tk.Scrollbar(title_frame, orient=tk.VERTICAL)
        title_entry = tk.Text(title_frame, wrap="word", height=10, width=30, yscrollcommand=title_scrollbar.set)
        title_scrollbar.config(command=title_entry.yview)
        title_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        title_entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        title_entry.insert("1.0", category_name)
        paned_window.add(title_frame)

        # Código con barra de desplazamiento vertical
        code_frame = tk.Frame(paned_window)
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
        category_name = simpledialog.askstring("Añadir Categoría", "Introduce el nombre de la categoría:")
        if category_name:
            title, code_snippet = self.open_code_editor(category_name)

            try:
                self.cursor.execute("INSERT INTO categories (name, code) VALUES (?, ?)", 
                                    (category_name, code_snippet))
                self.conn.commit()
                messagebox.showinfo("Éxito", f"Categoría '{category_name}' añadida.")
                self.update_category_list()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"La categoría '{category_name}' ya existe.")

    def edit_category(self):
        """Edita el título o el código de una categoría seleccionada."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una categoría para editar.")
            return

        old_name = self.category_listbox.get(selected[0])
        self.cursor.execute("SELECT code FROM categories WHERE name = ?", (old_name,))
        current_code = self.cursor.fetchone()[0] or ""
        title, new_code = self.open_code_editor(old_name, current_code)

        # Verificar si el usuario cerró la ventana sin realizar cambios
        if title == "" or new_code == "":
            messagebox.showwarning("Advertencia", "El título o el código no pueden estar vacíos.")
            return

        # Verificar si el nuevo título ya existe
        if title != old_name:  # Solo verificar si el título ha cambiado
            self.cursor.execute("SELECT COUNT(*) FROM categories WHERE name = ?", (title,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"La categoría '{title}' ya existe. Elige un nombre diferente.")
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
            messagebox.showwarning("Advertencia", "Selecciona una categoría para eliminar.")
            return

        category_name = self.category_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar la categoría '{category_name}'?")
        if confirm:
            self.cursor.execute("DELETE FROM categories WHERE name = ?", (category_name,))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Categoría '{category_name}' eliminada.")
            self.update_category_list()

    def run_category_code(self):
        """Ejecuta el código asociado a la categoría seleccionada en una nueva terminal."""
        selected = self.category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una categoría para ejecutar el código.")
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
                    subprocess.Popen(["start", "cmd", "/k", f"python {temp_filename} && pause"], shell=True)
                else:
                    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"python3 {temp_filename} && read -p 'Press any key to continue...'"], shell=False)

            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar el código: {e}")
        else:
            messagebox.showinfo("Info", f"La categoría '{category_name}' no tiene código asociado.")



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
