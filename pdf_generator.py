from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors


def generate_pdf_from_markdown(md_text: str) -> bytes:
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name="NameHeader",
        fontSize=30,
        leading=32,
        alignment=1,  # center
        fontName="Times-Bold",
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name="Contact",
        fontSize=10,
        leading=12,
        alignment=1,  # center
        textColor=colors.grey,
        fontName="Times-Italic",
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=14,
        leading=16,
        fontName="Times-Bold",
        spaceBefore=12,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name="PositionHeader",
        fontSize=11,
        leading=13,
        fontName="Times-Bold",
        spaceBefore=4,
        spaceAfter=2
    ))

    styles.add(ParagraphStyle(
        name="BodyTextCustom",
        fontSize=10.5,
        leading=13,
        fontName="Times-Roman",
        spaceAfter=4,
        alignment=4  # justify
    ))

    flow = []
    contact_inserted = False

    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            flow.append(Spacer(1, 4))
            continue

        # Name header
        if line.startswith("# "):
            flow.append(Paragraph(line[2:].strip(), styles["NameHeader"]))
            flow.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey, spaceBefore=6, spaceAfter=10))

        # Contacts
        elif line.startswith(("📧", "📞", "🌐")):
            flow.append(Paragraph(line, styles["Contact"]))
            if not contact_inserted:
                flow.append(HRFlowable(width="100%", thickness=0.6, color=colors.grey, spaceBefore=4, spaceAfter=10))
                contact_inserted = True

        # Section headers (Career Objective, Core Competencies, Professional Experience, etc.)
        elif line.startswith("## "):
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=6, spaceAfter=4))
            flow.append(Paragraph(line[3:].strip(), styles["SectionHeader"]))

        # Position / Company
        elif line.startswith("### ") or ("—" in line and line.startswith("**")):
            clean_line = line.replace("*", "").replace("### ", "").strip()
            flow.append(Paragraph(clean_line, styles["PositionHeader"]))
            flow.append(Spacer(1, 2))

        # Body text or bullets
        else:
            # Standardize bullet lists
            if line.startswith("- "):
                flow.append(Paragraph(line, styles["BodyTextCustom"]))
            else:
                flow.append(Paragraph(line, styles["BodyTextCustom"]))

    doc.build(flow)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
