# pdf_generator.py
from io import BytesIO
from weasyprint import HTML, CSS
import markdown2

def generate_pdf_from_markdown(md_text: str) -> bytes:
    """
    Convert Markdown text to PDF using HTML rendering (WeasyPrint).
    Preserves bold, italics, lists, links, spacing, and overall layout.
    """
    # Convert Markdown to HTML
    html_content = markdown2.markdown(md_text, extras=["fenced-code-blocks", "tables", "strike", "cuddled-lists"])

    # Wrap in minimal HTML template
    html_template = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: "Times New Roman", serif;
                font-size: 12pt;
                line-height: 1.4;
                color: #000000;
                margin: 1in;
            }}
            h1 {{
                font-size: 24pt;
                font-weight: bold;
                text-align: center;
                margin-bottom: 0.2in;
            }}
            h2 {{
                font-size: 16pt;
                font-weight: bold;
                margin-top: 0.3in;
                margin-bottom: 0.1in;
                border-bottom: 1px solid #AAAAAA;
                padding-bottom: 2px;
            }}
            h3 {{
                font-size: 14pt;
                font-weight: bold;
                margin-top: 0.2in;
                margin-bottom: 0.05in;
            }}
            p {{
                margin: 0.05in 0;
            }}
            ul {{
                margin: 0.05in 0 0.05in 0.25in;
            }}
            a {{
                color: #0000EE;
                text-decoration: none;
            }}
            hr {{
                border: 0;
                border-top: 1px solid #AAAAAA;
                margin: 0.1in 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Generate PDF
    pdf_io = BytesIO()
    HTML(string=html_template).write_pdf(pdf_io)
    pdf_bytes = pdf_io.getvalue()
    pdf_io.close()
    return pdf_bytes
