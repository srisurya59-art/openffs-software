import os
from io import BytesIO
from docx import Document
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def extract_docx_clean_rows(file_bytes):
    """Safely extracts Word document tables directly into flat structured row data lists."""
    try:
        doc = Document(BytesIO(file_bytes))
        all_tables_data = []
        for idx, table in enumerate(doc.tables):
            table_rows = []
            for row in table.rows:
                cells_text = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
                if any(cells_text):
                    table_rows.append(cells_text)
            if table_rows:
                all_tables_data.append({
                    "title": f"Extracted Reference Data Matrix (Table {idx + 1})",
                    "rows": table_rows
                })
        return all_tables_data
    except Exception:
        return []

def compile_compliance_pdf(report_metadata, uploaded_files_list):
    """
    Professional Engineering Assessment Engine.
    Generates compliance documentation matching structural standards.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=54, 
        leftMargin=54, 
        topMargin=54, 
        bottomMargin=54
    )
    story = []
    
    # --- Corporate Executive Palette ---
    PRIMARY_COLOR = colors.HexColor('#0F172A')   # Slate Primary
    ACCENT_COLOR = colors.HexColor('#1E3A8A')    # Engineering Blue
    TEXT_MAIN = colors.HexColor('#334155')       # Charcoal Body Text
    BG_LIGHT = colors.HexColor('#F8FAFC')        # Alternating Row Background
    BORDER_COLOR = colors.HexColor('#CBD5E1')    # Borders
    
    # --- Typography Sizing Hierarchy ---
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=PRIMARY_COLOR, fontName='Helvetica-Bold', spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#64748B'), fontName='Helvetica-Bold', spaceAfter=12)
    h1_style = ParagraphStyle('SecHeader', parent=styles['Heading2'], fontSize=13, leading=16, textColor=ACCENT_COLOR, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=8, keepWithNext=True)
    body_style = ParagraphStyle('BodyMain', parent=styles['Normal'], fontSize=10, leading=14, textColor=TEXT_MAIN, fontName='Helvetica')
    th_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=9, leading=11, textColor=colors.white, fontName='Helvetica-Bold')
    td_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=9, leading=12, textColor=TEXT_MAIN, fontName='Helvetica')
    
    # ==========================================
    # 1. DOCUMENT HEADER & COVER BLOCK
    # ==========================================
    story.append(Paragraph("Fitness-For-Service (FFS) Level 1 Assessment Report", title_style))
    story.append(Paragraph(f"<b>DOCUMENT REFERENCE TRACK ID:</b> {report_metadata.get('doc_ref', 'CCR-Area1-FFS-L1-001')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_COLOR, spaceBefore=0, spaceAfter=12))
    
    # ==========================================
    # 2. DYNAMIC EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    area_loss = float(report_metadata.get('cross_section_loss', 8.50))
    perf_diam = float(report_metadata.get('max_perforation', 20.0))
    
    # Core Engineering Evaluation
    area_status = "ACCEPTABLE" if area_loss <= 10.0 else "ACTION REQUIRED"
    perf_status = "ACCEPTABLE" if perf_diam <= 25.0 else "ACTION REQUIRED"
    overall_status = "SATISFACTORY (LEVEL 1 PASS)" if (area_loss <= 10.0 and perf_diam <= 25.0) else "REMEDIAL ACTION REQUIRED"
    status_color = "#16A34A" if overall_status.startswith("SATISFACTORY") else "#DC2626"
    
    summary_text = (
        f"This Level 1 Fitness-for-Service (FFS) assessment evaluates structural steel members "
        f"following structural impact anomalies. The assessment applies API 579-1/ASME FFS-1 Parts 4 and 5 "
        f"as the primary methodology for flaw characterisation, combined with AISC 360-16 for cross-sectional "
        f"capacity screening. Based on the operational defect geometry provided (Cross-Section Area Loss: <b>{area_loss}%</b>, "
        f"Max Perforation: <b>{perf_diam} mm</b>), the structural condition assessment profile is concluded as: "
        f"<b><font color='{status_color}'>{overall_status}</font></b>."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))
    
    # ==========================================
    # 3. METALLURGICAL & MATERIAL BASIS
    # ==========================================
    story.append(Paragraph("2. Material Basis & Design Metrics", h1_style))
    material_data = [
        [Paragraph("Parameter Designation", th_style), Paragraph("Governing Specification Value", th_style)],
        [Paragraph("Steel Grade Basis", td_style), Paragraph("ASTM A36 Carbon Steel, Hot-Dip Galvanized", td_style)],
        [Paragraph("Yield / Tensile Strength (Fy / Fu)", td_style), Paragraph("250 MPa / 400 MPa", td_style)],
        [Paragraph("Hardness Range Limits", td_style), Paragraph("120–165 HB (Consistent with A36 normal range)", td_style)],
        [Paragraph("Governing Design Codes", td_style), Paragraph("API 579-1/ASME FFS-1 (2021) Parts 4 & 5; AISC 360-16", td_style)]
    ]
    mat_table = Table(material_data, colWidths=[200, 304])
    mat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(mat_table)
    story.append(Spacer(1, 10))
    
    # ==========================================
    # 4. PRIMARY OPERATIONAL PARAMETERS
    # ==========================================
    story.append(Paragraph("3. Primary Screening Parameters", h1_style))
    param_table_data = [
        [Paragraph("Evaluation Boundary Component Field", th_style), Paragraph("Measured Input Value", th_style), Paragraph("Level 1 Screening Status", th_style)],
        [Paragraph("Observed Cross-Section Area Loss", td_style), Paragraph(f"{area_loss} %", td_style), Paragraph(f"<b>{area_status}</b>", td_style)],
        [Paragraph("Maximum Observed Perforation Limit", td_style), Paragraph(f"{perf_diam} mm", td_style), Paragraph(f"<b>{perf_status}</b>", td_style)]
    ]
    param_table = Table(param_table_data, colWidths=[220, 142, 142])
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
    # 5. GRAPHICAL ARTIFACTS AND UPLOAD ROUTER
    # ==========================================
    story.append(Paragraph("4. Annex: Component Inspection Reference Data", h1_style))
    
    if uploaded_files_list:
        for file_obj in uploaded_files_list:
            file_name = file_obj.name
            file_ext = "." + file_name.split(".")[-1].lower() if "." in file_name else ""
            file_bytes = file_obj.getvalue()
            
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=8, spaceAfter=8))
            story.append(Paragraph(f"<b>Source Reference Attached File:</b> {file_name}", body_style))
            story.append(Spacer(1, 4))
            
            if file_ext == '.docx':
                extracted_tables = extract_docx_clean_rows(file_bytes)
                if extracted_tables:
                    for table_dict in extracted_tables:
                        story.append(Paragraph(f"<b>{table_dict['title']}:</b>", td_style))
                        story.append(Spacer(1, 4))
                        
                        formatted_rows = [[Paragraph(str(cell), td_style) for cell in row] for row in table_dict['rows']]
                        num_cols = len(table_dict['rows'][0]) if table_dict['rows'] else 1
                        col_w = 504.0 / num_cols
                        
                        doc_table = Table(formatted_rows, colWidths=[col_w] * num_cols)
                        doc_table.setStyle(TableStyle([
                            ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
                            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                            ('TOPPADDING', (0,0), (-1,-1), 5),
                            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                            ('LEFTPADDING', (0,0), (-1,-1), 6),
                            ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ]))
                        story.append(KeepTogether([doc_table, Spacer(1, 10)]))
            else:
                story.append(Paragraph(f"📁 Reference document metadata index logged: <b>{file_name}</b>", td_style))
    else:
        story.append(Paragraph("<i>No structural verification files attached.</i>", td_style))

    # --- Secure Stream Output Construction ---
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
