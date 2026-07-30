import os
from io import BytesIO
from docx import Document
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def extract_docx_clean_rows(file_bytes):
    try:
        doc = Document(BytesIO(file_bytes))
        structured_tables = []
        for idx, table in enumerate(doc.tables):
            table_rows = []
            for row in table.rows:
                cells_text = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
                if any(cells_text):
                    table_rows.append(cells_text)
            if table_rows:
                structured_tables.append((f"Extracted Reference Data (Table {idx + 1})", table_rows))
        return structured_tables
    except Exception:
        return []

def compile_compliance_pdf(report_metadata, uploaded_files_list):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    story = []
    
    # --- Color Palette ---
    PRIMARY_COLOR = colors.HexColor('#0F172A')   # Navy / Slate
    ACCENT_COLOR = colors.HexColor('#1E3A8A')    # Engineering Blue
    TEXT_MAIN = colors.HexColor('#334155')       # Charcoal Body
    BG_LIGHT = colors.HexColor('#F8FAFC')        # Off-white rows
    BORDER_COLOR = colors.HexColor('#CBD5E1')    # Border gray
    
    # --- Styles Hierarchy ---
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=PRIMARY_COLOR, fontName='Helvetica-Bold', spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#64748B'), fontName='Helvetica-Bold', spaceAfter=12)
    h1_style = ParagraphStyle('SecHeader', parent=styles['Heading2'], fontSize=13, leading=16, textColor=ACCENT_COLOR, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=8)
    body_style = ParagraphStyle('BodyMain', parent=styles['Normal'], fontSize=10, leading=14, textColor=TEXT_MAIN, fontName='Helvetica')
    th_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=9, leading=11, textColor=colors.white, fontName='Helvetica-Bold')
    td_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=9, leading=12, textColor=TEXT_MAIN, fontName='Helvetica')
    
    # --- Engineering Assessment Logic (API 579 / AISC Criteria) ---
    area_loss = float(report_metadata.get('cross_section_loss', 0.0))
    perf_diam = float(report_metadata.get('max_perforation', 0.0))
    
    # Evaluate limits
    area_status = "ACCEPTABLE" if area_loss <= 10.0 else "ACTION REQUIRED"
    perf_status = "ACCEPTABLE" if perf_diam <= 25.0 else "ACTION REQUIRED"
    
    overall_status = "SATISFACTORY (LEVEL 1 PASS)"
    status_color = colors.HexColor('#16A34A') # Green
    
    if area_status == "ACTION REQUIRED" or perf_status == "ACTION REQUIRED":
        overall_status = "REMEDIAL ACTION REQUIRED (LEVEL 1 FAIL)"
        status_color = colors.HexColor('#DC2626') # Red

    # ==========================================
    # 1. HEADER SECTION
    # ==========================================
    story.append(Paragraph("OpenFFS™ Pro - Engineering Assessment Report", title_style))
    story.append(Paragraph(f"<b>DOCUMENT REFERENCE TRACK ID:</b> {report_metadata.get('doc_ref')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_COLOR, spaceBefore=0, spaceAfter=12))
    
    # ==========================================
    # 2. EXECUTIVE SUMMARY (NEW)
    # ==========================================
    story.append(Paragraph("Executive Summary", h1_style))
    summary_text = (
        f"A Fitness-For-Service (FFS) Level 1 screening assessment has been executed for the asset under reference "
        f"<b>{report_metadata.get('doc_ref')}</b> in accordance with API 579-1/ASME FFS-1 criteria metrics. Based on the "
        f"operational defect geometry provided (Cross-Section Area Loss: <b>{area_loss}%</b>, Max Perforation: <b>{perf_diam} mm</b>), "
        f"the structural condition assessment profile is concluded as: <b><font color='{status_color.hexval()}'>{overall_status}</font></b>. "
        f"The integrity check values indicate that localized corrosion degradation is currently within acceptable compliance boundary margins."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))
    
    # ==========================================
    # 3. PRIMARY OPERATIONAL PARAMETERS
    # ==========================================
    story.append(Paragraph("1. Primary Operational Parameters", h1_style))
    param_table_data = [
        [Paragraph("Evaluation Boundary Component Field", th_style), Paragraph("Logged Input Metric", th_style)],
        [Paragraph("Observed Cross-Section Area Loss", td_style), Paragraph(f"{area_loss} %", td_style)],
        [Paragraph("Maximum Observed Perforation Limit", td_style), Paragraph(f"{perf_diam} mm", td_style)]
    ]
    param_table = Table(param_table_data, colWidths=[300, 204])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(param_table)
    
    # ==========================================
    # 4. COMPONENT-WISE ASSESSMENT MATRIX (NEW)
    # ==========================================
    story.append(Paragraph("2. Component-Wise Fitness-For-Service Assessment", h1_style))
    assessment_data = [
        [Paragraph("Degradation Mechanism", th_style), Paragraph("Acceptance Threshold", th_style), Paragraph("Measured Value", th_style), Paragraph("Status", th_style)],
        [Paragraph("Metal Loss (Area)", td_style), Paragraph("&le; 10.0 % Loss", td_style), Paragraph(f"{area_loss} %", td_style), Paragraph(f"<b>{area_status}</b>", td_style)],
        [Paragraph("Pitting / Perforation", td_style), Paragraph("&le; 25.0 mm", td_style), Paragraph(f"{perf_diam} mm", td_style), Paragraph(f"<b>{perf_status}</b>", td_style)]
    ]
    assess_table = Table(assessment_data, colWidths=[140, 130, 110, 124])
    assess_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(assess_table)
    
    # ==========================================
    # 5. IMAGES & ATTACHMENTS SECTION (UPDATED WITH IMAGE INJECTION)
    # ==========================================
    story.append(Paragraph("3. Annex: Component Inspection Photos & Artifacts", h1_style))
    
    images_rendered = 0
    for file_obj in uploaded_files_list:
        file_name = file_obj.name
        file_ext = os.path.splitext(file_name).lower()
        
        # Pull file data bytes from the Streamlit UploadedFile wrapper
        file_bytes = file_obj.getvalue()
        
        if file_ext in ['.jpg', '.jpeg', '.png']:
            images_rendered += 1
            story.append(Paragraph(f"<b>Figure 3.{images_rendered}: Asset Field Photo Asset ({file_name})</b>", body_style))
            story.append(Spacer(1, 6))
            
            try:
                # Wrap bytes into an in-memory buffer array stream for ReportLab to construct
                img_buffer = BytesIO(file_bytes)
                # Render scaling constraints to fit letter page neatly (Max 400 width, scale height to 220)
                report_img = Image(img_buffer, width=380, height=210)
                report_img.hAlign = 'LEFT'
                story.append(report_img)
                story.append(Spacer(1, 14))
            except Exception as e:
                story.append(Paragraph(f"<i>[Error embedding photo component: {str(e)}]</i>", td_style))
                
        elif file_ext == '.docx':
            extracted_tables = extract_docx_clean_rows(file_bytes)
            if extracted_tables:
                story.append(Paragraph(f"<b>Extracted Document Tables from ({file_name}):</b>", body_style))
                story.append(Spacer(1, 6))
                for title, rows in extracted_tables:
                    formatted_rows = [[Paragraph(str(cell), td_style) for cell in row] for row in rows]
                    col_w = 504 / len(rows[0]) if rows else 504
                    doc_table = Table(formatted_rows, colWidths=[col_w] * len(rows[0]))
                    doc_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
                        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                        ('TOPPADDING', (0,0), (-1,-1), 5),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                    ]))
                    story.append(doc_table)
                    story.append(Spacer(1, 10))
                    
    if images_rendered == 0:
        story.append(Paragraph("<i>No graphical component photo files (.jpg/.png) were supplied for visual logging extraction.</i>", td_style))

    # --- Close and return binary string compilation streams ---
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
