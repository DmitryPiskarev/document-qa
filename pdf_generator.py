from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
import markdown2

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

    # Custom styles (renamed to avoid clashes)
    styles.add(ParagraphStyle(name="NameHeader",
                              fontSize=18,
                              leading=22,
                              spaceAfter=12,
                              alignment=1,  # centered
                              textColor=colors.black,
                              fontName="Times-Bold"))

    styles.add(ParagraphStyle(name="SectionHeader",
                              fontSize=12,
                              leading=14,
                              spaceAfter=6,
                              textColor=colors.black,
                              fontName="Times-Bold"))

    styles.add(ParagraphStyle(name="BodyTextCustom",
                              fontSize=10,
                              leading=13,
                              spaceAfter=6,
                              textColor=colors.black,
                              fontName="Times-Roman"))

    styles.add(ParagraphStyle(name="Contact",
                              fontSize=9,
                              leading=11,
                              alignment=1,  # centered
                              spaceAfter=10,
                              textColor=colors.grey,
                              fontName="Times-Italic"))

    flow = []

    # Convert Markdown → HTML
    html = markdown2.markdown(md_text)

    # Split by <h1>, <h2>, etc. and handle differently
    for block in html.splitlines():
        block = block.strip()
        if not block:
            flow.append(Spacer(1, 8))
            continue

        # Detect headers
        if block.startswith("<h1>"):
            content = block.replace("<h1>", "").replace("</h1>", "")
            flow.append(Paragraph(content, styles["NameHeader"]))
        elif block.startswith("<h2>"):
            content = block.replace("<h2>", "").replace("</h2>", "")
            flow.append(Paragraph(content, styles["SectionHeader"]))
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceBefore=4, spaceAfter=6))
        else:
            # Normal text or <ul><li>
            flow.append(Paragraph(block, styles["BodyTextCustom"]))

    doc.build(flow)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
