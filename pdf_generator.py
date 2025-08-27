from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
import markdown2


def generate_pdf_from_markdown(md_text: str) -> bytes:
    buffer = BytesIO()

    # Create PDF doc
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

    # Custom styles
    styles.add(ParagraphStyle(
        name="NameHeader",
        fontSize=22,
        leading=26,
        spaceAfter=14,
        alignment=1,  # center
        textColor=colors.black,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=13,
        leading=15,
        spaceAfter=6,
        textColor=colors.black,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="BodyTextCustom",
        fontSize=10.5,
        leading=12.5,  # slightly tighter
        spaceAfter=5,
        textColor=colors.black,
        fontName="Times-Roman",
        alignment=4  # justify text
    ))

    styles.add(ParagraphStyle(
        name="Contact",
        fontSize=9.5,
        leading=11,
        alignment=1,  # center
        spaceAfter=8,
        textColor=colors.grey,
        fontName="Times-Italic"
    ))

    flow = []

    # Convert Markdown → HTML
    html = markdown2.markdown(md_text)

    # Split block by lines
    for block in html.splitlines():
        block = block.strip()
        if not block:
            flow.append(Spacer(1, 6))
            continue

        if block.startswith("<h1>"):
            content = block.replace("<h1>", "").replace("</h1>", "")
            flow.append(Paragraph(content, styles["NameHeader"]))
            flow.append(HRFlowable(width="100%", thickness=0.7, color=colors.grey, spaceBefore=6, spaceAfter=10))

        elif block.startswith("<h2>"):
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=10, spaceAfter=6))
            content = block.replace("<h2>", "").replace("</h2>", "")
            flow.append(Paragraph(content, styles["SectionHeader"]))
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=4, spaceAfter=8))

        elif "@" in block or "linkedin" in block.lower() or "github" in block.lower():
            # Contacts
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=8, spaceAfter=4))
            flow.append(Paragraph(block, styles["Contact"]))
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=4, spaceAfter=10))

        else:
            flow.append(Paragraph(block, styles["BodyTextCustom"]))

    doc.build(flow)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
