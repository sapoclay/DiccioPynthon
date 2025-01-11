import requests
import zipfile
import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk

GITHUB_REPO_URL = "https://github.com/sapoclay/DiccioPynthon"
VERSION_URL = f"{GITHUB_REPO_URL}/raw/main/version.txt"
ZIP_URL = f"{GITHUB_REPO_URL}/archive/refs/heads/main.zip"
LOCAL_VERSION_FILE = "version.txt"
TEMP_FOLDER = "temp_update"

def get_remote_version():
    """Obtiene la versión remota desde el repositorio."""
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener la versión remota.\n{e}")
        return None

def get_local_version():
    """Obtiene la versión local de la aplicación."""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as file:
            return file.read().strip()
    return None

def download_and_extract_zip(progress_bar):
    """Descarga y extrae el archivo ZIP de la actualización con barra de progreso."""
    try:
        response = requests.get(ZIP_URL, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        chunk_size = 1024
        downloaded = 0

        with open("update.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    progress = (downloaded / total_size) * 100
                    progress_bar["value"] = progress
                    progress_bar.update()

        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall(TEMP_FOLDER)
        messagebox.showinfo("Actualización", "Actualización descargada y extraída correctamente.")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error al descargar la actualización.\n{e}")
    except zipfile.BadZipFile as e:
        messagebox.showerror("Error", f"Error al extraer el archivo ZIP.\n{e}")
    finally:
        if os.path.exists("update.zip"):
            os.remove("update.zip")

def apply_update():
    """Reemplaza los archivos locales con los archivos actualizados."""
    update_folder = os.path.join(TEMP_FOLDER, "DiccioPynthon")  
    if os.path.exists(update_folder):
        for item in os.listdir(update_folder):
            src = os.path.join(update_folder, item)
            dest = os.path.join(os.getcwd(), item)

            if os.path.isdir(src):
                if os.path.exists(dest):
                    shutil.rmtree(dest)
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
        messagebox.showinfo("Actualización", "Actualización aplicada correctamente.")
    else:
        messagebox.showerror("Error", "No se encontró la carpeta de actualización.")
    shutil.rmtree(TEMP_FOLDER)

def check_for_updates():
    """Verifica si hay una actualización disponible y la aplica."""
    remote_version = get_remote_version()
    local_version = get_local_version()

    if not remote_version:
        return

    if local_version != remote_version:
        result = messagebox.askyesno("Actualización Disponible", 
                                     f"Hay una nueva versión disponible (v{remote_version}).\n"
                                     f"¿Deseas descargarla?")
        if result:
            # Crear ventana con barra de progreso
            progress_window = tk.Toplevel()
            progress_window.title("Descargando Actualización")
            progress_window.geometry("400x100")
            tk.Label(progress_window, text="Descargando la actualización...").pack(pady=10)
            progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
            progress_bar.pack(pady=10)
            
            # Descargar y aplicar la actualización
            download_and_extract_zip(progress_bar)
            progress_window.destroy()
            apply_update()

            # Actualizar el archivo de versión local
            with open(LOCAL_VERSION_FILE, "w") as file:
                file.write(remote_version)
            messagebox.showinfo("Actualización", "Actualización completada. Reinicia la aplicación.")
    else:
        messagebox.showinfo("Actualización", "La aplicación ya está actualizada.")

# Interfaz Gráfica Principal
def main():
    root = tk.Tk()
    root.title("Gestor de Actualizaciones")
    root.geometry("300x150")

    tk.Label(root, text="Gestor de Actualizaciones", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Buscar Actualizaciones", command=check_for_updates).pack(pady=10)
    tk.Button(root, text="Salir", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
