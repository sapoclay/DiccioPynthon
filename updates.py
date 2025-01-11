import requests
import zipfile
import os
import shutil
import sys
import tkinter as tk
from tkinter import messagebox


class GitHubUpdater:
    def __init__(self, repo_owner, repo_name, local_commit_hash):
        """
        Inicializa el actualizador de GitHub.
        :param repo_owner: El propietario del repositorio (nombre de usuario u organización).
        :param repo_name: El nombre del repositorio.
        :param local_commit_hash: El hash del último commit local.
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.local_commit_hash = local_commit_hash
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/main"
        self.download_url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/main.zip"
        self.temp_zip_path = "latest_version.zip"
        self.temp_extract_path = "latest_version"

    def show_message(self, title, message):
        """
        Muestra un mensaje en una ventana emergente.
        :param title: El título de la ventana.
        :param message: El mensaje a mostrar.
        """
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        messagebox.showinfo(title, message)

    def check_for_updates(self):
        """
        Verifica si hay actualizaciones disponibles en el repositorio.
        :return: True si hay actualizaciones, False si el código local está actualizado.
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            latest_commit = response.json()["sha"]

            if latest_commit != self.local_commit_hash:
                self.show_message("Actualización disponible", "Hay una nueva actualización disponible.")
                return True
            else:
                self.show_message("Sin actualizaciones", "No hay actualizaciones disponibles.")
                return False
        except requests.RequestException as e:
            self.show_message("Error", f"Error al verificar actualizaciones: {e}")
            return False

    def download_latest_version(self):
        """
        Descarga la última versión del repositorio como un archivo ZIP.
        """
        try:
            response = requests.get(self.download_url, stream=True)
            response.raise_for_status()
            with open(self.temp_zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            self.show_message("Descarga completada", f"Última versión descargada en {self.temp_zip_path}")
        except requests.RequestException as e:
            self.show_message("Error", f"Error al descargar la última versión: {e}")
            return False
        return True

    def extract_and_update_files(self):
        """
        Extrae el archivo ZIP descargado, sobrescribe los archivos locales y elimina temporales.
        """
        try:
            with zipfile.ZipFile(self.temp_zip_path, "r") as zip_ref:
                zip_ref.extractall(self.temp_extract_path)

            extracted_folder = os.path.join(self.temp_extract_path, f"{self.repo_name}-main")

            for item in os.listdir(extracted_folder):
                s = os.path.join(extracted_folder, item)
                d = os.path.join(os.getcwd(), item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            self.show_message("Actualización completada", "Los archivos locales se actualizaron con éxito.")
        except Exception as e:
            self.show_message("Error", f"Error al actualizar archivos locales: {e}")
        finally:
            self.clean_up()

    def clean_up(self):
        """
        Elimina archivos temporales generados durante la actualización.
        """
        if os.path.exists(self.temp_zip_path):
            os.remove(self.temp_zip_path)
        if os.path.exists(self.temp_extract_path):
            shutil.rmtree(self.temp_extract_path)
        self.show_message("Limpieza completada", "Los archivos temporales se eliminaron correctamente.")

    def restart_application(self):
        """
        Reinicia la aplicación cerrándola y volviéndola a ejecutar.
        """
        try:
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except Exception as e:
            self.show_message("Error", f"Error al reiniciar la aplicación: {e}")

    def update(self):
        """
        Realiza el proceso completo de actualización: verifica, descarga, actualiza y reinicia.
        """
        if self.check_for_updates():
            if self.download_latest_version():
                self.extract_and_update_files()
                self.show_message("Reiniciando", "La aplicación se reiniciará ahora.")
                self.restart_application()
        else:
            self.show_message("Sin actualizaciones", "No se encontraron actualizaciones.")
