import tkinter as tk
from app.themes import THEMES

def create_buttons(self, button_frame, theme_name):
    """Crea los botones en la interfaz y aplica el tema."""
    # Obtener el diccionario del tema basado en el nombre
    theme = THEMES.get(theme_name, THEMES["light"])

    # Destruir los botones existentes en el frame
    for widget in button_frame.winfo_children():
        widget.grid_forget()  # Forzar la eliminación del botón sin destruirlo
        print(f"Botón destruido: {widget}")  # Verificar destrucción

    # Crear los botones
    buttons = [
        ("Añadir Concepto", self.add_category),
        ("Editar Concepto", self.edit_category),
        ("Eliminar Concepto", self.delete_category),
        ("Ejecutar Código", self.run_category_code),
        ("Buscar Concepto", self.search_category_dialog),
    ]

    # Crear los botones en el frame
    for i, (text, command) in enumerate(buttons):
        row, col = divmod(i, 2)  # Dividir en filas y columnas
        button = tk.Button(button_frame, text=text, command=command)
        button.grid(row=row, column=col, pady=5)

        # Aplicar el tema a cada botón individualmente
        button.configure(bg=theme["button_bg"], fg=theme["button_fg"])

    # Asegurarnos de que los cambios se reflejan
    button_frame.update_idletasks()  # Actualizar la interfaz para reflejar el cambio
