import sqlite3  # Importación de sqlite3
from .db_connection import DatabaseConnection

class DatabaseActions:
    """Clase para manejar acciones específicas en la base de datos."""
    
    def __init__(self, db_name="conceptos.db"):
        """
        Inicializa las acciones de base de datos con una conexión establecida.

        :param db_name: Nombre del archivo de la base de datos.
        """
        self.db = DatabaseConnection(db_name)
        self.db.connect()
        self.setup_database()

    def setup_database(self):
        """Crea las tablas necesarias si no existen."""
        query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            code TEXT
        )
        """
        self.db.execute(query)
        self.db.commit()

    def add_category(self, name, code=""):
        """
        Añade una nueva categoría a la base de datos.

        :param name: Nombre de la categoría.
        :param code: Código asociado a la categoría (opcional).
        """
        query = "INSERT INTO categories (name, code) VALUES (?, ?)"
        try:
            self.db.execute(query, (name, code))
            self.db.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"La categoría '{name}' ya existe.")

    def edit_category(self, old_name, new_name, new_code):
        """
        Edita una categoría existente.

        :param old_name: Nombre actual de la categoría.
        :param new_name: Nuevo nombre de la categoría.
        :param new_code: Nuevo código asociado a la categoría.
        """
        query = "UPDATE categories SET name = ?, code = ? WHERE name = ?"
        self.db.execute(query, (new_name, new_code, old_name))
        self.db.commit()

    def delete_category(self, name):
        """
        Elimina una categoría de la base de datos.

        :param name: Nombre de la categoría a eliminar.
        """
        query = "DELETE FROM categories WHERE name = ?"
        self.db.execute(query, (name,))
        self.db.commit()

    def fetch_categories_from_db(self):
        """
        Recupera todas las categorías de la base de datos.

        :return: Lista de tuplas con (nombre, código).
        """
        query = "SELECT name, code FROM categories"
        return self.db.execute(query).fetchall()

    def search_category(self, search_term):
        """
        Busca categorías por nombre.

        :param search_term: Término de búsqueda.
        :return: Lista de tuplas con los nombres de las categorías que coinciden.
        """
        query = "SELECT name FROM categories WHERE LOWER(name) LIKE ?"
        return self.db.execute(query, (f"%{search_term.lower()}%",)).fetchall()
    
    def update_category_list(self):
        """Actualiza la lista de categorías en la interfaz, recuperando los nombres desde la base de datos."""
        query = "SELECT name FROM categories"
        return self.db.execute(query).fetchall()

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.db.close()

    def fusionar_base_datos(self, db_path, imported_db_path):
        """
        Fusiona los datos de una base de datos SQLite importada con la base de datos actual.

        Parámetros:
            db_path (str): Ruta de la base de datos actual.
            imported_db_path (str): Ruta de la base de datos importada.

        Retorno:
            str: Mensaje de éxito o error para informar el resultado de la operación.
        """
        try:
            # Conectar a la base de datos actual
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Conectar a la base de datos importada
            imported_conn = sqlite3.connect(imported_db_path)
            imported_cursor = imported_conn.cursor()

            # Obtener todas las tablas de la base de datos importada
            imported_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in imported_cursor.fetchall()]

            for table_name in tables:
                # Leer datos de la tabla importada
                imported_cursor.execute(f"SELECT * FROM {table_name}")
                rows = imported_cursor.fetchall()

                # Obtener columnas de la tabla
                imported_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in imported_cursor.fetchall()]
                column_list = ", ".join(columns)
                placeholders = ", ".join(["?"] * len(columns))

                # Insertar datos en la base de datos actual, evitando duplicados
                for row in rows:
                    cursor.execute(
                        f"INSERT OR IGNORE INTO {table_name} ({column_list}) VALUES ({placeholders})", 
                        row
                    )

            # Guardar los cambios y cerrar conexiones
            conn.commit()
            imported_conn.close()
            conn.close()

            return "Los datos de la base de datos importada se fusionaron correctamente."
        except Exception as e:
            return f"Ocurrió un error al fusionar la base de datos: {e}"
