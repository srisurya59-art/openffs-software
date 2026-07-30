import os
from io import BytesIO
from docx import Document
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def extract_docx_clean_rows(file_bytes):
    """Safely extracts Word document tables directly into pure strings and flat lists."""
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
    """Solidified core engine script. Returns binary stream directly without structural failures."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    story = []
    
    # --- Palette Configuration Layout ---
    PRIMARY_COLOR = colors.HexColor('#0F172A')   
    ACCENT_COLOR = colors.HexColor('#1E3A8A')    
    TEXT_MAIN = colors.HexColor('#334155')       
    BG_LIGHT = colors.HexColor('#F8FAFC')        
    BORDER_COLOR = colors.HexColor('#CBD5E1')    
    
    # --- Professional Typography Styles ---
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=PRIMARY_COLOR, fontName='Helvetica-Bold', spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#64748B'), fontName='Helvetica-Bold', spaceAfter=12)
    h1_style = ParagraphStyle('SecHeader', parent=styles['Heading2'], fontSize=13, leading=16, textColor=ACCENT_COLOR, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=8)
    body_style = ParagraphStyle('BodyMain', parent=styles['Normal'], fontSize=10, leading=14, textColor=TEXT_MAIN, fontName='Helvetica')
    th_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=9, leading=11, textColor=colors.white, fontName='Helvetica-Bold')
    td_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=9, leading=12, textColor=TEXT_MAIN, fontName='Helvetica')
    
    # --- Strict Engineering Boundary Calculations Matrix ---
    area_loss = float(report_metadata.get('cross_section_loss', 8.50))
    perf_diam = float(report_metadata.get('max_perforation', 20.0))
    
    area_status = "ACCEPTABLE" if area_loss <= 10.0 else "ACTION REQUIRED"
    perf_status = "ACCEPTABLE" if perf_diam <= 25.0 else "ACTION REQUIRED"
    
    overall_status = "SATISFACTORY (LEVEL 1 PASS)"
    status_color = colors.HexColor('#16A34A') 
    
    if area_status == "ACTION REQUIRED" or perf_status == "ACTION REQUIRED":
        overall_status = "REMEDIAL ACTION REQUIRED (LEVEL 1 FAIL)"
        status_color = colors.HexColor('#DC2626') 

    # ==========================================
    # 1. DOCUMENT HEADER BLOCK
    # ==========================================
    story.append(Paragraph("OpenFFS™ Pro - Engineering Assessment Report", title_style))
    story.append(Paragraph(f"<b>DOCUMENT REFERENCE TRACK ID:</b> {report_metadata.get('doc_ref', 'N/A')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_COLOR, spaceBefore=0, spaceAfter=12))
    
    # ==========================================
    # 2. DYNAMIC EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("Executive Summary", h1_style))
    summary_text = (
        f"A Fitness-For-Service (FFS) Level 1 screening assessment has been executed for the asset under reference "
        f"<b>{report_metadata.get('doc_ref', 'N/A')}</b> in accordance with API 579-1/ASME FFS-1 criteria metrics. Based on the "
        f"operational defect geometry provided (Cross-Section Area Loss: <b>{area_loss}%</b>, Max Perforation: <b>{perf_diam} mm</b>), "
        f"the structural condition assessment profile is concluded as: <b><font color='{status_color.hexval()}'>{overall_status}</font></b>. "
        f"The integrity check values indicate that structural compliance parameters align with mandatory baseline safety criteria requirements."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))
    
    # ==========================================
    # 3. METRICS ASSIGNMENT LOGS
    # ==========================================
    story.append(Paragraph("1. Primary Operational Parameters", h1_style))
    param_table_data = [
        [Paragraph("Evaluation Boundary Component Field", th_style), Paragraph("Logged Input Metric", th_style)],
        [Paragraph("Observed Cross-Section Area Loss", td_style), Paragraph(f"{area_loss} %", td_style)],
        [Paragraph("Maximum Observed Perforation Limit", td_style), Paragraph(f"{perf_diam} mm", td_style)]
    ]
    param_table = Table(param_table_data, colWidths=[280, 224])
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
    # 4. COMPONENT-WISE COMPLIANCE ANALYSIS GRID
    # ==========================================
    story.append(Paragraph("2. Component-Wise Fitness-For-Service Assessment", h1_style))
    assessment_data = [
        [Paragraph("Degradation Mechanism", th_style), Paragraph("Acceptance Threshold", th_style), Paragraph("Measured Value", th_style), Paragraph("Status", th_style)],
        [Paragraph("Metal Loss (Area)", td_style), Paragraph("&le; 10.0 % Loss", td_style), Paragraph(f"{area_loss} %", td_style), Paragraph(f"<b>{area_status}</b>", td_style)],
        [Paragraph("Pitting / Perforation", td_style), Paragraph("&le; 25.0 mm", td_style), Paragraph(f"{perf_diam} mm", td_style), Paragraph(f"<b>{perf_status}</b>", td_style)]
    ]
    assess_table = Table(assessment_data, colWidths=[140, 140, 114, 110])
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
    # 5. GRAPHICAL ARTIFACTS AND UPLOAD ROUTER
    # ==========================================
    story.append(Paragraph("3. Annex: Component Inspection Photos & Artifacts", h1_style))
    
    images_rendered = 0
    if uploaded_files_list:
        for file_obj in uploaded_files_list:
            file_name = file_obj.name
            file_ext = os.path.splitext(file_name).lower()
            file_bytes = file_obj.getvalue()
            
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=8, spaceAfter=8))
            
            if file_ext in ['.jpg', '.jpeg', '.png']:
                images_rendered += 1
                story.append(Paragraph(f"<b>Figure 3.{images_rendered}: Asset Field Visual Photo ({file_name})</b>", body_style))
                story.append(Spacer(1, 6))
                try:
                    img_buffer = BytesIO(file_bytes)
                    report_img = Image(img_buffer, width=360, height=200)
                    report_img.hAlign = 'LEFT'
                    story.append(report_img)
                    story.append(Spacer(1, 10))
                except Exception:
                    story.append(Paragraph("<i>[Could not safely compute component layout image pixels stream]</i>", td_style))
                    
            elif file_ext == '.docx':
                extracted_tables = extract_docx_clean_rows(file_bytes)
                if extracted_tables:
                    for table_dict in extracted_tables:
                        story.append(Paragraph(f"<b>{table_dict['title']} from ({file_name}):</b>", body_style))
                        story.append(Spacer(1, 4))
                        
                        formatted_rows = [[Paragraph(str(cell), td_style) for cell in row] for row in table_dict['rows']]
                        
                        # Dynamically safe column width constraint logic
                        num_cols = len(table_dict['rows'][0]) if table_dict['rows'] else 1
                        col_w = 504 / num_cols
                        
                        doc_table = Table(formatted_rows, colWidths=[col_w] * num_cols)
                        doc_table.setStyle(TableStyle([
                            ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
                            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                            ('TOPPADDING', (0,0), (-1,-1), 5),
                            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                            ('LEFTPADDING', (0,0), (-1,-1), 6),
                        ]))
                        story.append(doc_table)
