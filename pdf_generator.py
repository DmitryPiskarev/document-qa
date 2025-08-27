from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import LETTER

def generate_pdf_from_markdown(md_text: str) -> bytes:
    buffer = BytesIO()

    # Create the PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    # Base styles
    styles = getSampleStyleSheet()

    # Custom styles (avoid name clashes by renaming)
    styles.add(ParagraphStyle(name="NameHeader", fontSize=18, leading=22, spaceAfter=12, alignment=1, textColor="black"))
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=12, leading=14, spaceAfter=8, textColor="black", underlineWidth=1))
    styles.add(ParagraphStyle(name="CustomBodyText", fontSize=10, leading=13, spaceAfter=6, textColor="black"))
    styles.add(ParagraphStyle(name="Contact", fontSize=9, leading=11, alignment=1, spaceAfter=10, textColor="gray"))

    flow = []

    # Naive markdown parsing: treat lines starting with ## as headers, others as body text
    for line in md_text.splitlines():
        line = line.strip()
        if not line:
            flow.append(Spacer(1, 8))
            continue
        if line.startswith("# "):  # Big header (Name)
            flow.append(Paragraph(line[2:], styles["NameHeader"]))
        elif line.startswith("## "):  # Section
            flow.append(Paragraph(line[3:], styles["SectionHeader"]))
        elif line.startswith("📧") or line.startswith("📞") or line.startswith("🌐"):  # Contacts
            flow.append(Paragraph(line, styles["Contact"]))
        else:  # Normal text
            flow.append(Paragraph(line, styles["CustomBodyText"]))

    doc.build(flow)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
