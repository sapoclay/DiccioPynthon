import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import platform
from app.themes import apply_theme


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

def show_about(root, current_theme):
    """Abre una ventana de 'About' con información sobre la aplicación."""
    about_window = tk.Toplevel(root)
    about_window.title("Acerca de")
    about_window.geometry("400x400")

    # Aplica el tema a la ventana emergente
    apply_theme(about_window, current_theme)

    img = Image.open("img/logo.png")
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)
    label_img = tk.Label(about_window, image=img)
    label_img.image = img  # Necesario para mantener la referencia de la imagen
    label_img.pack(pady=10)

    def get_local_version():
        """Obtiene la versión local del archivo version.txt."""
        try:
            with open("version.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Versión no disponible"

    # Obtener la versión local
    local_version = get_local_version()

    # Descripción con la versión
    description = f"""Esta aplicación permite al usuario \ngestionar conceptos y códigos de Python.
    Permite añadir, editar, eliminar y ejecutar códigos Python asociados a los conceptos guardados.
    \nVersión: {local_version}"""
    label_description = tk.Label(about_window, text=description, justify="center", wraplength=350)
    label_description.pack(pady=10)

    # Aseguramos que la variable 'label_link' esté definida antes de configurarla
    label_link = tk.Label(about_window, text="Visita el repositorio en GitHub", fg="blue", cursor="hand2")
    label_link.pack(pady=10)
    label_link.bind(
        "<Button-1>", 
        lambda e: open_link("https://github.com/sapoclay/DiccioPynthon")
    )

    # Actualizar el color de fondo y texto de los labels según el tema
    if current_theme == "dark":
        label_description.configure(bg="#2e2e2e", fg="#ffffff")  # Tema oscuro
        label_link.configure(bg="#2e2e2e", fg="#ffffff")  # Tema oscuro
    else:
        label_description.configure(bg="#dcdcdc", fg="#000000")  # Tema claro
        label_link.configure(bg="#dcdcdc", fg="#000000")  # Tema claro