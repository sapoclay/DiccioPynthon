import tkinter as tk
from tkinter import messagebox
import os
import sys
from app.config import save_config  

THEMES = {
    "light": {
        "bg": "#dcdcdc",
        "fg": "#000000",
        "button_bg": "#e0e0e0",
        "button_fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "menu_bg": "#f0f0f0",
        "menu_fg": "#000000",
        "menu_active_bg": "#bdbdbd",
        "menu_active_fg": "#000000",
    },
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "button_bg": "#3b3b3b",
        "button_fg": "#ffffff",
        "entry_bg": "#3b3b3b",
        "entry_fg": "#ffffff",
        "menu_bg": "#3b3b3b",
        "menu_fg": "#ffffff",
        "menu_active_bg": "#2e2e2e",
        "menu_active_fg": "#ffffff",
    }
}


def apply_theme(root, theme_name):
    """Aplica el tema a la ventana y widgets."""
    theme = THEMES.get(theme_name, THEMES["light"])

    # Configurar fondo de la ventana principal
    root.configure(bg=theme["bg"])

    def apply_to_widgets(widget):
        """Aplica el tema a los widgets contenidos en la ventana principal y subventanas."""
        for child in widget.winfo_children():
            if isinstance(child, (tk.Label, tk.Button)):
                child.configure(bg=theme["button_bg"], fg=theme["button_fg"])
            elif isinstance(child, tk.Entry):
                child.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
            elif isinstance(child, tk.Listbox):
                child.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
            elif isinstance(child, tk.Frame):
                child.configure(bg=theme["bg"])
            elif isinstance(child, tk.Toplevel):
                child.configure(bg=theme["bg"])
                apply_to_widgets(child)  # Recursivo para aplicar a subventanas
            else:
                try:
                    child.configure(bg=theme["bg"], fg=theme["fg"])
                except tk.TclError:
                    pass

    # Aplicar el tema a widgets en la ventana principal
    apply_to_widgets(root)

    # Forzar actualización para reflejar cambios visuales
    root.update_idletasks()
        
def apply_menu_theme(menu_bar, theme):
    """Aplica el tema a los menús."""
    # Configurar fondo y texto del menú bar
    menu_bar.configure(bg=theme.get("menu_bg", "#f0f0f0"), fg=theme.get("menu_fg", "#000000"))

    # Iterar sobre los elementos del menú bar
    for index in range(menu_bar.index("end") + 1):  # Itera sobre las entradas del menú
        try:
            # Intentar obtener el menú asociado a este índice
            menu_name = menu_bar.entrycget(index, "menu")
            if menu_name:  # Verifica que sea un submenú válido
                menu_widget = menu_bar.nametowidget(menu_name)
                menu_widget.configure(bg=theme.get("menu_bg", "#f0f0f0"), fg=theme.get("menu_fg", "#000000"))

                # Configurar cada entrada del submenú
                for item_index in range(menu_widget.index("end") + 1):
                    try:
                        # Cambiar los colores del elemento del menú
                        menu_widget.entryconfig(item_index, background=theme.get("menu_bg", "#f0f0f0"), foreground=theme.get("menu_fg", "#000000"))
                        # Cambiar los colores activos
                        menu_widget.entryconfig(item_index, activebackground=theme.get("menu_active_bg", "#bdbdbd"))
                        menu_widget.entryconfig(item_index, activeforeground=theme.get("menu_active_fg", "#000000"))
                    except tk.TclError:
                        pass  # Ignorar errores para separadores o elementos no configurables
        except tk.TclError:
            pass  # Ignorar índices no configurables o inválidos

def apply_theme_and_restart(root, theme_name, app_instance):
    """Aplica el tema, guarda la configuración y reinicia la aplicación."""
    # Mostrar mensaje de confirmación para reiniciar
    response = messagebox.askyesno("Reiniciar aplicación", 
                                   "¿Deseas cambiar el tema? La aplicación se reiniciará.")

    if response:
        # Guardar el tema en el archivo config.json
        save_config(theme_name)  # Solo se pasa el nombre del tema

        # Actualizar el tema actual en la instancia de la aplicación
        app_instance.current_theme = theme_name

        # Aplicar el tema a la ventana principal
        theme = THEMES.get(theme_name, THEMES["light"])
        root.configure(bg=theme["bg"])

        def apply_to_widgets(widget):
            """Aplica el tema a los widgets contenidos en la ventana principal y subventanas."""
            for child in widget.winfo_children():
                if isinstance(child, (tk.Label, tk.Button)):
                    child.configure(bg=theme["button_bg"], fg=theme["button_fg"])
                elif isinstance(child, tk.Entry):
                    child.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
                elif isinstance(child, tk.Listbox):
                    child.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
                elif isinstance(child, tk.Frame):
                    child.configure(bg=theme["bg"])
                elif isinstance(child, tk.Toplevel):
                    child.configure(bg=theme["bg"])
                    apply_to_widgets(child)  # Recursivo para aplicar a subventanas
                else:
                    try:
                        child.configure(bg=theme["bg"], fg=theme["fg"])
                    except tk.TclError:
                        pass

        apply_to_widgets(root)
        root.update_idletasks()

        # Cerrar la ventana y reiniciar la aplicación
        root.quit()  # Cerrar la ventana actual
        python = sys.executable
        os.execl(python, python, *sys.argv)  # Reiniciar la aplicación

    else:
        return  # Si el usuario cancela, no hace nada