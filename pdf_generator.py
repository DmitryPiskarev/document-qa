from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors

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
        fontSize=30,
        leading=26,
        spaceAfter=12,
        alignment=1,  # center
        textColor=colors.black,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="PositionHeader",
        fontSize=22,
        leading=26,
        spaceAfter=12,
        alignment=1,  # center
        textColor=colors.black,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=14,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.black,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="BodyTextCustom",
        fontSize=10.5,
        leading=12.5,
        spaceAfter=6,
        textColor=colors.black,
        fontName="Times-Roman",
        alignment=4  # justify
    ))

    styles.add(ParagraphStyle(
        name="Contact",
        fontSize=10,
        leading=11,
        alignment=1,  # center
        spaceAfter=10,
        textColor=colors.grey,
        fontName="Times-Italic"
    ))

    flow = []

    for line in md_text.splitlines():
        line = line.strip()
        if not line:
            flow.append(Spacer(1, 6))
            continue

        if line.startswith("# "):  # Name
            flow.append(Paragraph(line[2:], styles["NameHeader"]))
            flow.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey, spaceBefore=6, spaceAfter=10))

        elif line.startswith("📧") or line.startswith("📞") or line.startswith("🌐"):  # Contacts
            flow.append(Paragraph(line, styles["Contact"]))

        elif line.startswith("## "):  # Section header
            flow.append(HRFlowable(width="100%", thickness=0.6, color=colors.grey, spaceBefore=6, spaceAfter=2))
            flow.append(Paragraph(line[3:], styles["SectionHeader"]))

        elif line.startswith("** "):  # Role header
            flow.append(HRFlowable(width="100%", thickness=0.6, color=colors.grey, spaceBefore=10, spaceAfter=2))
            flow.append(Paragraph(line[3:], styles["PositionHeader"]))

        else:  # Body text
            flow.append(Paragraph(line, styles["BodyTextCustom"]))

    # Add a line after contacts section if contacts exist
    for i, line in enumerate(md_text.splitlines()):
        if any(line.startswith(s) for s in ["📧", "📞", "🌐"]):
            flow.insert(i+2, HRFlowable(width="100%", thickness=0.6, color=colors.grey, spaceBefore=6, spaceAfter=10))
            break

    doc.build(flow)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
