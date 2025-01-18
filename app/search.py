from tkinter import simpledialog, messagebox
import webbrowser
import platform
import os


def open_link(url):

    """Abre un enlace en el navegador predeterminado del sistema."""
    try:
        if platform.system() == "Windows":
            os.startfile(url)  # Usa el navegador predeterminado en Windows
        else:
            webbrowser.open(url)  # Usa el navegador predeterminado en otros sistemas
    except Exception as e:
        print(f"Error al abrir el enlace: {e}")

def search_python_docs():

    """Abre una ventana para buscar en la documentación oficial de Python."""
    query = simpledialog.askstring("Buscar en la Documentación", "Introduce el término a buscar:")
    if query:
        search_url = f"https://docs.python.org/3/search.html?q={query}"
        open_link(search_url)
    else:
        messagebox.showinfo("Búsqueda cancelada", "No se introdujo ningún término.")

def search_python_packages():

    """Abre una ventana para buscar paquetes de Python."""
    query = simpledialog.askstring("Buscar en PyPi", "Introduce paquete Python a buscar:")
    if query:
        search_url = f"https://pypi.org/search/?q={query}"
        open_link(search_url)
    else:
        messagebox.showinfo("Búsqueda cancelada", "No se introdujo el nombre de ningún paquete.")

def abrir_tutoriales():

    """Abre un enlace de tutoriales en el navegador"""
    enlace_tutoriales = "https://github.com/sapoclay/basicos-python"
    open_link(enlace_tutoriales)
 