import os
from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def parse_all_docx_content(file_bytes):
    """
    Exhaustively extracts every table row from the document to build 
    a highly detailed, itemized structural component appendix.
    """
    try:
        doc = Document(BytesIO(file_bytes))
        parsed_blocks = []
        
        for idx, table in enumerate(doc.tables):
            table_rows = []
            for row in table.rows:
                cells_text = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
                if any(cells_text):
                    table_rows.append(cells_text)
            
            if table_rows:
                # Determine context headers based on content matching
                first_row_str = " ".join(table_rows[0]).lower()
                if "steel grade" in first_row_str or "parameter" in first_row_str:
                    title = f"Material Basis Matrix Summary"
                elif "verdict" in first_row_str or "replace" in first_row_str:
                    title = f"Overall Status Verdict Matrix (23 Components)"
                elif "defect id" in first_row_str or "dimensions" in first_row_str:
                    title = f"Flaw & Defect Characterisation Log"
                else:
                    title = f"Inspection Data Matrix Record {idx + 1}"
                
                parsed_blocks.append({
                    "title": title,
                    "rows": table_rows
                })
        return parsed_blocks
    except Exception:
        return []

def compile_compliance_pdf(report_metadata, uploaded_files_list):
    """
    Production core engineering report compilation engine.
    Renders corporate executive layout templates matching rigid reporting guidelines.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=45, 
        leftMargin=45, 
        topMargin=45, 
        bottomMargin=45
    )
    story = []
    
    # --- Corporate Executive Color Palette ---
    PRIMARY_COLOR = colors.HexColor('#0F172A')   # Slate Primary Blue-Black
    ACCENT_COLOR = colors.HexColor('#1E3A8A')    # Engineering Slate Blue
    TEXT_MAIN = colors.HexColor('#334155')       # Off-Black Body Text
    BG_LIGHT = colors.HexColor('#F8FAFC')        # Zebra Striping Light Gray
    BORDER_COLOR = colors.HexColor('#E2E8F0')    # Clean Subtle Border Gray
    
    # --- Layout Typography Configuration ---
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=PRIMARY_COLOR, fontName='Helvetica-Bold', spaceAfter=2)
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#64748B'), fontName='Helvetica-Bold', spaceAfter=10)
    h1_style = ParagraphStyle('SecHeader', parent=styles['Heading2'], fontSize=12, leading=15, textColor=ACCENT_COLOR, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6, keepWithNext=True)
    body_style = ParagraphStyle('BodyMain', parent=styles['Normal'], fontSize=9.5, leading=14, textColor=TEXT_MAIN, fontName='Helvetica')
    th_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=8.5, leading=10, textColor=colors.white, fontName='Helvetica-Bold')
    td_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=TEXT_MAIN, fontName='Helvetica')
    td_bold = ParagraphStyle('TableCellBold', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=PRIMARY_COLOR, fontName='Helvetica-Bold')

    # ==========================================
    # 1. PRIMARY DOCUMENT TITLE HEADER
    # ==========================================
    story.append(Paragraph("Fitness-For-Service (FFS) Level 1 Assessment Report", title_style))
    story.append(Paragraph(f"<b>DOCUMENT REFERENCE TRACK ID:</b> {report_metadata.get('doc_ref', 'FFS-LVL1-CCR-AREA1-REV1')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_COLOR, spaceBefore=0, spaceAfter=10))
    
    # ==========================================
    # 2. COMPREHENSIVE EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    exec_text = (
        "This Level 1 Fitness-for-Service (FFS) assessment evaluates structural steel members "
        "following structural impact anomalies and drone projectile shrapnel impact tracks. The assessment applies "
        "API 579-1/ASME FFS-1 Parts 4 (Local Metal Loss) and 5 (Gouges) as the primary methodology for flaw "
        "characterisation, combined with AISC 360-16 for cross-sectional capacity screening and buckling interaction checks. "
        "Based on the operational parameters logged below, an itemized component-wise evaluation framework has been compiled "
        "to define structural pass, fail, or immediate replacement metrics across all 23 key elements [source: 1]."
    )
    story.append(Paragraph(exec_text, body_style))
    story.append(Spacer(1, 10))
    
    # ==========================================
    # 3. STATUTORY MATERIAL GOVERNANCE BASIS
    # ==========================================
    story.append(Paragraph("2. Material Basis & Design Metrics", h1_style))
    material_data = [
        [Paragraph("Parameter Designation Description", th_style), Paragraph("Governing Specification Value / Finding Status", th_style)],
        [Paragraph("Steel Grade Basis", td_bold), Paragraph("ASTM A36 Carbon Steel, Hot-Dip Galvanized (ASTM A123/A153)", td_style)],
        [Paragraph("Yield / Tensile Strength (Fy / Fu)", td_bold), Paragraph("250 MPa / 400 MPa", td_style)],
        [Paragraph("Hardness Range Limits Logged", td_bold), Paragraph("120–165 HB — Consistent with A36 normal specification boundaries", td_style)],
        [Paragraph("Nondestructive Testing Protocol", td_bold), Paragraph("DPT / MPI — No surface-breaking cracks detected on accessible zones", td_style)],
        [Paragraph("Governing Design Standards", td_bold), Paragraph("API 579-1/ASME FFS-1 (2021) Parts 4 & 5; AISC 360-16 Steel Code", td_style)]
    ]
    mat_table = Table(material_data, colWidths=[180, 342])
    mat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(mat_table)
    story.append(Spacer(1, 10))
    
    # ==========================================
    # 4. SITE USER INPUT METRICS SCREENING
    # ==========================================
    story.append(Paragraph("3. Operational Parameter Screening Thresholds", h1_style))
    area_loss = float(report_metadata.get('cross_section_loss', 8.50))
    perf_diam = float(report_metadata.get('max_perforation', 20.0))
    area_status = "ACCEPTABLE" if area_loss <= 10.0 else "ACTION REQUIRED"
    perf_status = "ACCEPTABLE" if perf_diam <= 25.0 else "ACTION REQUIRED"
    
    param_table_data = [
        [Paragraph("Evaluation Boundary Component Field", th_style), Paragraph("Logged Operational Value", th_style), Paragraph("Level 1 Screening Status", th_style)],
        [Paragraph("Observed Cross-Section Area Loss (%)", td_style), Paragraph(f"{area_loss} %", td_style), Paragraph(f"<b>{area_status}</b>", td_style)],
        [Paragraph("Maximum Observed Perforation Limit (mm)", td_style), Paragraph(f"{perf_diam} mm", td_style), Paragraph(f"<b>{perf_status}</b>", td_style)]
    ]
    param_table = Table(param_table_data, colWidths=[200, 150, 172])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(param_table)
    
    # ==========================================
    # 5. DYNAMIC STRUCTURED PARSING APPENDIX
    # ==========================================
    story.append(Paragraph("4. Annex: Component Inspection Data Extraction Records", h1_style))
    story.append(Paragraph("Itemized extraction matrix tables cleanly read from attached field logging artifacts are parsed below:", body_style))
    story.append(Spacer(1, 6))
    
    if uploaded_files_list:
        for file_obj in uploaded_files_list:
            file_name = file_obj.name
            file_ext = "." + file_name.split(".")[-1].lower() if "." in file_name else ""
            file_bytes = file_obj.getvalue()
            
            if file_ext == '.docx':
                extracted_blocks = parse_all_docx_content(file_bytes)
                
                for block in extracted_blocks:
                    story.append(Paragraph(f"<b>Source Report: {block['title']} ({file_name})</b>", td_bold))
                    story.append(Spacer(1, 4))
                    
                    # Convert raw data strings to paragraphs with strict cell text auto-wrapping
                    formatted_rows = []
                    for raw_row in block['rows']:
                        formatted_rows.append([Paragraph(str(cell), td_style) for cell in raw_row])
                    
                    # Calculate strict safe column constraints dynamically
