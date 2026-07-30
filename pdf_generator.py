import os
from io import BytesIO
from docx import Document
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def extract_docx_tables(file_bytes):
    try:
        doc = Document(BytesIO(file_bytes))
        extracted_data = []
        for table_idx, table in enumerate(doc.tables):
            table_text = [f"[Table {table_idx + 1} Content Extraction Log]"]
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    table_text.append(" | ".join(row_cells))
            extracted_data.append("\n".join(table_text))
        return "\n\n".join(extracted_data) if extracted_data else "No text data records found in Word Document tables."
    except Exception as e:
        return f"[Failed to extract raw data logs from .docx resource structure: {str(e)}]"

def extract_pdf_text(file_bytes):
    try:
        reader = PdfReader(BytesIO(file_bytes))
        extracted_text = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(f"[Page {idx + 1} Parsing Log]\n{text.strip()}")
        return "\n\n".join(extracted_text) if extracted_text else "No parseable string content discovered in PDF pages."
    except Exception as e:
        return f"[Failed to extract structural content logs from .pdf asset structure: {str(e)}]"

def compile_compliance_pdf(report_metadata, uploaded_files_list):
    """
    Production core rendering engine. Computes data objects and returns 
    raw document download stream bytes directly to the application layer.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E3A8A'), spaceAfter=15)
    section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1F2937'), spaceBefore=12, spaceAfter=8)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#374151'))
    code_style = ParagraphStyle('CodeStyle', parent=styles['Code'], fontSize=9, leading=12, textColor=colors.HexColor('#0F172A'), backColor=colors.HexColor('#F1F5F9'), borderPadding=6)

    # Document Header Title Layout Banner
    story.append(Paragraph("OpenFFS™ Pro - Engineering Assessment Report", title_style))
    story.append(Paragraph(f"<b>Document Reference Track ID:</b> {report_metadata.get('doc_ref')}", body_style))
    story.append(Spacer(1, 15))
    
    # Structural Calculation Criteria Metrics Section
    story.append(Paragraph("1. Primary Operational Parameters", section_style))
    param_data = [
        ["Evaluation Boundary Component Field", "Logged Value Metric Status"],
        ["Observed Cross-Section Area Loss", f"{report_metadata.get('cross_section_loss')}%"],
        ["Maximum Observed Perforation Limit", f"{report_metadata.get('max_perforation')} mm"]
    ]
    t = Table(param_data, colWidths=[250, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # Process Universal Input Reference Attachments Appendices
    story.append(Paragraph("2. Annex: Associated Resource Reference Logs", section_style))
    
    for file_obj in uploaded_files_list:
        file_name = file_obj.name
        file_ext = os.path.splitext(file_name)[1].lower()
        file_bytes = file_obj.getvalue() # Extract safe, isolated stream buffer arrays
        
        story.append(Paragraph(f"<b>Source Reference Attached File Asset:</b> {file_name}", body_style))
        story.append(Spacer(1, 4))
        
        if file_ext in ['.jpg', '.jpeg', '.png']:
            story.append(Paragraph("<i>[Image asset attached. File binary logged inside master assessment verification log bundle.]</i>", body_style))
        elif file_ext == '.docx':
            text_extracted = extract_docx_tables(file_bytes)
            story.append(Paragraph(text_extracted.replace('\n', '<br/>'), code_style))
        elif file_ext == '.pdf':
            text_extracted = extract_pdf_text(file_bytes)
            story.append(Paragraph(text_extracted.replace('\n', '<br/>'), code_style))
        else:
            story.append(Paragraph(f"<i>[Raw unstructured generic attachment file format data loaded into pipeline: {len(file_bytes)} bytes]</i>", body_style))
        
        story.append(Spacer(1, 10))

    # Build document and extract binary object arrays
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
