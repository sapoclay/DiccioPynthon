import sqlite3


class DatabaseConnection:
    """Clase para manejar la conexión a la base de datos SQLite."""
    
    def __init__(self, db_name="conceptos.db"):
        """
        Inicializa la conexión con la base de datos.

        :param db_name: Nombre del archivo de la base de datos.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establece la conexión con la base de datos."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.connection:
            self.connection.close()

    def commit(self):
        """Guarda los cambios en la base de datos."""
        if self.connection:
            self.connection.commit()

    def execute(self, query, params=None):
        """
        Ejecuta una consulta SQL.

        :param query: Consulta SQL a ejecutar.
        :param params: Parámetros para la consulta.
        :return: Cursor con el resultado de la consulta.
        """
        if not self.connection:
            raise Exception("No hay conexión activa con la base de datos.")
        if params:
            return self.cursor.execute(query, params)
        return self.cursor.execute(query)
