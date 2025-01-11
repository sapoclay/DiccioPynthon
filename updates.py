import requests
import os
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys
import subprocess

class GitHubUpdater:
    def __init__(self, repo_owner, repo_name, local_commit_hash):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.local_commit_hash = local_commit_hash
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/main"

    def check_for_updates(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            latest_commit = response.json()["sha"]

            if latest_commit != self.local_commit_hash:
                self.show_message("Actualización disponible", "Hay una nueva actualización disponible.")
                return True
            else:
                self.show_message("Sin actualizaciones", "El código local está actualizado.")
                return False
        except requests.RequestException as e:
            self.show_message("Error", f"Error al verificar actualizaciones: {e}")
            return False

    def download_latest_version(self, download_path="latest_code.zip"):
        url = f"https://github.com/{self.repo_owner}/{self.repo_name}/archive/refs/heads/main.zip"
        download_path = Path(download_path)
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(download_path, "wb") as file:
                file.write(response.content)
            self.show_message("Descarga completada", f"Última versión descargada en {download_path}")
            return download_path
        except requests.RequestException as e:
            self.show_message("Error", f"Error al descargar la última versión: {e}")
            return None

    def install_update(self, zip_path):
        try:
            # Descomprimir el archivo
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall("update_temp")
            
            # Sobrescribir archivos
            src_dir = Path("update_temp").joinpath(f"{self.repo_name}-main")
            for item in src_dir.iterdir():
                target = Path.cwd() / item.name
                if target.is_dir():
                    shutil.rmtree(target)
                shutil.move(str(item), str(target))

            # Eliminar archivos temporales
            shutil.rmtree("update_temp")
            zip_path.unlink()

            self.show_message("Actualización completada", "La actualización se instaló correctamente. El programa se reiniciará.")
            self.restart_program()

        except Exception as e:
            self.show_message("Error", f"Error al instalar la actualización: {e}")

    def restart_program(self):
        try:
            if sys.platform == "win32":
                subprocess.Popen(f"python {sys.argv[0]}", shell=True)
            else:
                os.execv(sys.executable, ['python'] + sys.argv)
            sys.exit()
        except Exception as e:
            self.show_message("Error", f"No se pudo reiniciar la aplicación: {e}")

    def show_message(self, title, message):
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        messagebox.showinfo(title, message)
