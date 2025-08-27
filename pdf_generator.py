from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors

def generate_pdf_from_markdown(md_text: str) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="NameHeader",
        fontSize=28,
        leading=32,
        alignment=1,  # center
        spaceAfter=6,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="Contact",
        fontSize=10,
        leading=12,
        alignment=1,
        textColor=colors.grey,
        fontName="Times-Italic",
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=14,
        leading=16,
        spaceBefore=12,
        spaceAfter=4,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="PositionHeader",
        fontSize=12,
        leading=14,
        spaceBefore=6,
        spaceAfter=2,
        fontName="Times-Bold"
    ))

    styles.add(ParagraphStyle(
        name="BodyTextCustom",
        fontSize=10.5,
        leading=12.5,
        spaceAfter=4,
        alignment=4,  # justify
        fontName="Times-Roman"
    ))

    flow = []

    contact_inserted = False

    for line in md_text.splitlines():
        line = line.strip()
        if not line:
            flow.append(Spacer(1, 4))
            continue

        # Name
        if line.startswith("# "):
            flow.append(Paragraph(line[2:], styles["NameHeader"]))
            flow.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey, spaceBefore=6, spaceAfter=10))

        # Contacts
        elif line.startswith("📧") or line.startswith("📞") or line.startswith("🌐"):
            flow.append(Paragraph(line, styles["Contact"]))
            if not contact_inserted:
                flow.append(HRFlowable(width="100%", thickness=0.6, color=colors.grey, spaceBefore=4, spaceAfter=10))
                contact_inserted = True

        # Section headers
        elif line.startswith("### ") or line.startswith("## "):
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=6, spaceAfter=2))
            flow.append(Paragraph(line.lstrip("# ").strip(), styles["SectionHeader"]))

        # Position + company detection (bold + dash)
        elif line.startswith("**") and "—" in line:
            clean_line = line.replace("*", "")
            flow.append(Paragraph(clean_line, styles["PositionHeader"]))
            flow.append(Spacer(1, 2))

        # Body text
        else:
            flow.append(Paragraph(line, styles["BodyTextCustom"]))

    doc.build(flow)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
