import tkinter as tk
import jedi

import re

def get_code_context(code, cursor_pos):
    """Obtiene el contexto completo del código hasta la posición del cursor y devuelve el nivel de indentación adecuado."""
    row, col = cursor_pos
    lines = code.split("\n")

    # Verificar las líneas anteriores para ver si pertenecen a una estructura de control
    indentation = "    "  # Valor por defecto para la indentación (4 espacios)

    for line in reversed(lines[:row]):
        stripped_line = line.strip()

        if stripped_line.endswith(":"):  # Detectamos estructuras de control como if, for, etc.
            # Si encontramos una estructura de control, asignamos una indentación mayor
            indentation = "    "  # Incrementamos la indentación (por defecto, 4 espacios)
            break
        elif stripped_line == "":
            # Si encontramos una línea vacía, dejamos de buscar
            break

    return indentation

def on_enter(event, code_entry):
    """Gestiona la acción de presionar Enter para aplicar la sangría dinámica."""
    # Obtener la posición del cursor
    cursor_pos = code_entry.index(tk.INSERT)
    row, col = map(int, cursor_pos.split('.'))

    # Obtener el código completo. 1.0 hace referencia a la posición de inicio en el widget de texto. Línea 1, columna 0. tk.ed se refiere al final del texto en el widget.
    code_text = code_entry.get("1.0", tk.END)

    # Obtener la indentación adecuada basada en el contexto
    new_indentation = get_code_context(code_text, (row-1, col))

    # Insertar la nueva línea con la indentación calculada
    code_entry.insert(tk.INSERT, f"\n{new_indentation}")

    return "break"  # Evitar que se ejecute el comportamiento predeterminado de Enter
