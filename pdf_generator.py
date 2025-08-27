from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch
from io import BytesIO
import markdown
from bs4 import BeautifulSoup


def generate_pdf_from_markdown(md_text: str) -> BytesIO:
    """
    Convert improved CV in Markdown into a modern black-and-white PDF.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="NameHeader", fontSize=18, leading=22, spaceAfter=10, alignment=1, bold=True))
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=12, leading=14, spaceBefore=16, spaceAfter=6, uppercase=True, bold=True))
    styles.add(ParagraphStyle(name="BodyText", fontSize=10, leading=13, spaceAfter=4))
    styles.add(ParagraphStyle(name="Contact", fontSize=9, leading=11, alignment=1, spaceAfter=12, textColor="grey"))

    flow = []

    # Convert Markdown → HTML → parse
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, "html.parser")

    for el in soup.children:
        if el.name == "h1":
            flow.append(Paragraph(el.get_text(), styles["NameHeader"]))
        elif el.name == "h2":
            flow.append(Paragraph(el.get_text().upper(), styles["SectionHeader"]))
        elif el.name == "p":
            flow.append(Paragraph(el.get_text(), styles["BodyText"]))
        elif el.name == "ul":
            items = [ListItem(Paragraph(li.get_text(), styles["BodyText"])) for li in el.find_all("li")]
            flow.append(ListFlowable(items, bulletType="bullet"))
        elif el.name == "hr":
            flow.append(Spacer(1, 0.2 * inch))

    doc.build(flow)
    buffer.seek(0)
    return buffer
