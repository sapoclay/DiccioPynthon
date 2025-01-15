from tkinter import simpledialog, messagebox
import webbrowser
import platform

def open_link(url):
    """Abre un enlace en el navegador dependiendo del sistema operativo."""
    system_name = platform.system()
    try:
        if system_name == "Windows":
            webbrowser.get("windows-default").open(url)
        else:
            webbrowser.open(url)
    except webbrowser.Error as e:
        print(f"Error al abrir el navegador: {e}")

def search_python_docs(self):
    """Abre una ventana para buscar en la documentación oficial de Python."""
    query = simpledialog.askstring("Buscar en la Documentación", "Introduce el término a buscar:")
    if query:
        search_url = f"https://docs.python.org/3/search.html?q={query}"
        open_link(search_url)
    else:
        messagebox.showinfo("Búsqueda cancelada", "No se introdujo ningún término.")
    
def search_python_packages(self):
    """Abre una ventana para buscar paquetes de Python."""
    query = simpledialog.askstring("Buscar en PyPi", "Introduce paquete Python a buscar:")
    if query:
        search_url = f"https://pypi.org/search/?q={query}"
        open_link(search_url)
    else:
        messagebox.showinfo("Búsqueda cancelada", "No se introdujo el nombre de ningún paquete.")
        
def abrir_tutoriales(self):
    """Abre un enlace de tutoriales en el navegador"""
    enlace_tutoriales = "https://github.com/sapoclay/basicos-python"
    open_link(enlace_tutoriales)