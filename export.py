import io
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def export_docx(text: str) -> bytes:
    """Export improved CV to DOCX."""
    buffer = io.BytesIO()
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def export_pdf(text: str) -> bytes:
    """Export improved CV to PDF."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 15
        if y < 40:  # new page
            c.showPage()
            y = height - 40
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
