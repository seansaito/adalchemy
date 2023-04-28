
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportlabImage

pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

def create_pdf(image, text, topic):
    # Create a buffer for the PDF content
    buffer = BytesIO()

    # Set up the SimpleDocTemplate and styles
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create a custom style for Japanese text
    custom_style = ParagraphStyle(
        name="CustomStyle",
        fontName="HeiseiKakuGo-W5",
        fontSize=12,
        leading=14,
        spaceAfter=10,
    )
    styles.add(custom_style)

    elements = []

    # Add the topic as a title
    title_style = styles["Heading1"]
    title_style.fontName = "HeiseiKakuGo-W5"
    title = Paragraph(topic, title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Add the image
    image_file = BytesIO(image)
    pdf_image = ReportlabImage(image_file)
    pdf_image.drawHeight = 250
    pdf_image.drawWidth = 250
    elements.append(pdf_image)
    elements.append(Spacer(1, 12))

    # Add the text
    text_style = styles["CustomStyle"]

    list_texts = text.split('\n')
    for text in list_texts:
        pdf_text = Paragraph(text, text_style)
        elements.append(pdf_text)

    # Build the PDF
    doc.build(elements)
    pdf = buffer.getvalue()

    # Close the buffer
    buffer.close()

    return pdf
