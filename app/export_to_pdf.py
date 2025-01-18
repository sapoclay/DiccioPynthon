from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import tkinter.filedialog as filedialog
from tkinter import messagebox   
from app.themes import apply_theme

def export_to_pdf(db_actions):
    """
    Exporta el contenido de la base de datos a un archivo PDF.
    
    Recupera todas las categorías y sus códigos asociados y crea un archivo
    PDF con el contenido formateado.
    """
    # Usar la instancia 'db_actions' para llamar a 'fetch_categories_from_db'
    categories = db_actions.fetch_categories_from_db()

    # Cuadro de diálogo para seleccionar la ubicación y nombre del archivo
    pdf_filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Guardar PDF como..."
    )

    if not pdf_filename:
        return

    # Crear el archivo PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    y_position = height - 40

    for category in categories:
        title = category[0]
        code = category[1] if category[1] else "No hay código asociado"
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_position, f"Título: {title}")
        y_position -= 20

        c.setFont("Helvetica", 10)
        c.drawString(40, y_position, f"Código:")
        y_position -= 15

        lines = code.splitlines()

        for line in lines:
            if y_position < 40:
                c.showPage()  # Si llegamos al final de la página, creamos una nueva
                c.setFont("Helvetica", 10)
                y_position = height - 40

            c.drawString(40, y_position, line)
            y_position -= 15

        y_position -= 20

    c.save()
    messagebox.showinfo("Exportación Completa", f"El contenido se ha exportado a {pdf_filename}")
