import subprocess
import os
from tkinter import messagebox

def run_ollama(self):
        """Verifica si 'ollama' está instalado y ejecuta 'ollama run llama3.2'."""
        try:
            # Verificar si el comando 'ollama' está disponible
            subprocess.run(["ollama", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            # Ejecutar 'ollama run llama3.2' en una nueva terminal
            if os.name == "nt":  # Windows
                subprocess.Popen(["start", "cmd", "/c", "ollama run llama3.2"], shell=True)
            else:  # Linux/Unix
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "ollama run llama3.2"], shell=False)

        except FileNotFoundError:
            # Mostrar mensaje si 'ollama' no está instalado
            messagebox.showerror(
                "Ollama no disponible",
                "Ollama no está disponible en este sistema.\nPuedes descargarlo desde: https://ollama.com"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al intentar ejecutar Ollama:\n{e}")