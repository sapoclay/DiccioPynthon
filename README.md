## DiccioPynthon

![DiccioPynthon](https://github.com/user-attachments/assets/0c165807-7a4c-42f1-9149-e8a9ddc49038)

DiccioPynthon es una aplicación de gestión de categorías y conceptos de Python. Permite añadir, editar, eliminar y ejecutar fragmentos de código Python asociados a diferentes categorías. Además, ofrece la posibilidad de exportar las categorías a un archivo PDF y administrar el contenido de manera eficiente con una interfaz gráfica basada en Tkinter.

## Funcionalidades

- Añadir Categoría: Permite agregar una nueva categoría con su respectivo fragmento de código.
- Editar Categoría: Puedes modificar tanto el nombre como el código de las categorías existentes.
- Eliminar Categoría: Elimina una categoría previamente creada.
- Ejecutar Categoría: Ejecuta el código asociado a una categoría en una terminal separada.
- Exportar a PDF: Exporta la lista de categorías y sus códigos a un archivo PDF con formato.
- Interfaz Gráfica: Interfaz de usuario sencilla y fácil de usar, construida con Tkinter, y con soporte para imágenes.
- Base de Datos: Utiliza SQLite para almacenar las categorías y sus códigos de manera persistente.
- Ollama: Si tienes instalado Ollama en tu sistema te va permitir abrir una terminal para interactuar con el modelo llama3.2. 
- Importar BD: El programa permite ahora importar otra base de datos creada con este mismo problema. La base de datos importada se fusionará con la actual.

### Requisitos

- Python 3.x
- Tkinter (generalmente incluido con Python)
- Pillow: Librería de Python para trabajar con imágenes.
- ReportLab: Librería para generar archivos PDF.
- SQLite: Base de datos integrada en Python para almacenar categorías y códigos.

## Uso

En una terminal escribir:

```
python3 run_app.py
```

Las dependencias que están incluidas en el archivo requirements.txt deberían instalarse de forma automática. Por lo que en la primera ejecución puede tardar un poco en iniciarse la aplicación ya que tendrá que crear el entorno virtual en el que se va a crear e instalar todas las dependencias necesarias. En las siguientes ejecuciones el tiempo debería ser menor.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar esta aplicación, por favor sigue estos pasos:

- Haz un fork de este repositorio.
- Crea una nueva rama (git checkout -b feature-nueva-funcionalidad).
- Realiza los cambios y haz commit de tus modificaciones (git commit -am 'Añadir nueva funcionalidad').
- Haz push a la rama (git push origin feature-nueva-funcionalidad).
- Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
