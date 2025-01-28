import subprocess
import os
from tkinter import messagebox

def run_ollama(self):
        """Verifica si 'ollama' está instalado y ejecuta 'ollama run deepseek-r1:8b'."""
        try:
            # Verificar si el comando 'ollama' está disponible
            subprocess.run(["ollama", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            # Ejecutar 'ollama run llama3.2' en una nueva terminal
            if os.name == "nt":  # Windows
                subprocess.Popen(["start", "cmd", "/c", "ollama run deepseek-r1:8b"], shell=True)
            else:  # Linux/Unix
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "ollama run deepseek-r1:8b"], shell=False)

        except FileNotFoundError:
            # Mostrar mensaje si 'ollama' no está instalado
            messagebox.showerror(
                "Ollama no disponible",
                "Ollama no está disponible en este sistema.\nPuedes descargarlo desde: https://ollama.com\n"
                "Después descarga el motor DeepSeek escribiendo en la terminal: ollama pull deepseek-r1:8b. \n"
                "Vuelve a ejecutar de nuevo esta opción."
                
            )
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al intentar ejecutar Ollama:\n{e}")