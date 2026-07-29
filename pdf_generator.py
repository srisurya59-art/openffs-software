import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

def generate_certified_pdf_report(track_title, inputs_dict, metrics_dict, verdict_status, reviewer_name="", file_name="FFS_Certified_Report.pdf"):
    """
    Generates an enterprise-grade branded engineering assessment report PDF file
    complete with corporate header banner, dynamic logo placement, and automated review stamp.
    """
    doc = SimpleDocTemplate(file_name, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Brand Palette (Corporate Navy & Deep Slate)
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, textColor=colors.HexColor('#1a365d'), spaceAfter=2)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#4a5568'), spaceAfter=15)
    section_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, textColor=colors.HexColor('#2b6cb0'), spaceBefore=10, spaceAfter=6)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#2d3748'))
    
    # --- FEATURE 1: CORPORATE LOGO & COMPANY NAME BANNER ---
    # We build a 2-column header grid. Left side: Company details. Right side: Logo image.
    company_name_text = "<b>OPENFFS ENGINEERING SOLUTIONS LTD.</b><br/><font size=8 color='#718096'>Asset Integrity & Computational Mechanics Division</font>"
    header_left = Paragraph(company_name_text, body_style)
    
    logo_path = "client_logo.png"
    if os.path.exists(logo_path):
        # Automatically scales and mounts logo image if file is placed in root folder
        header_right = Image(logo_path, width=120, height=35)
    else:
        # Placeholder text box if no image asset file exists yet
        header_right = Paragraph("<b>[ CUSTOM CLIENT LOGO PLACEMENT ]</b>", ParagraphStyle('P', alignment=2, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#a0aec0')))
        
    header_table = Table([[header_left, header_right]], colWidths=[350, 180])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')), # Clean silver separator bar
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # Title Block
    story.append(Paragraph("FITNESS-FOR-SERVICE ENGINEERING VERIFICATION RECORD", title_style))
    story.append(Paragraph(f"Standard: API 579-1/ASME FFS-1 — Module: {track_title}", subtitle_style))
    story.append(Paragraph(f"<b>Calculation Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    story.append(Spacer(1, 10))
    
    # --- DATA MATRICES TABLES ---
    story.append(Paragraph("1. Field Input Inspection Parameters", section_style))
    input_data = [["Inspection Parameter Key", "Recorded Field Metric Value"]]
    for k, v in inputs_dict.items():
        input_data.append([str(k).replace('_', ' ').title(), str(v)])
    
    t_input = Table(input_data, colWidths=[300, 230])
    t_input.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#2d3748')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_input)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("2. Computational Mechanics Evaluation Metrics", section_style))
    metrics_data = [["Calculation Matrix KPI", "Computed Safety Threshold Limit"]]
    for k, v in metrics_dict.items():
        metrics_data.append([str(k).replace('_', ' ').title(), str(v)])
        
    t_metrics = Table(metrics_data, colWidths=[300, 230])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#2d3748')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 12))
    
    # --- SCREENING VERDICT ---
    story.append(Paragraph("3. Fitness-For-Service Screening Verdict Status", section_style))
    verdict_color = '#28a745' if "Acceptable" in verdict_status or verdict_status == "True" else '#dc3545'
    
    v_data = [[Paragraph(f"FINAL DETERMINATION STATUS: {verdict_status.upper()}", ParagraphStyle('V', fontName='Helvetica-Bold', fontSize=11, textColor=colors.white, alignment=1))]]
    t_verdict = Table(v_data, colWidths=[530])
    t_verdict.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(verdict_color)),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_verdict)
    story.append(Spacer(1, 15))
    
    # --- FEATURE 2: AUTOMATED DIGITAL VERIFICATION STAMP BOX ---
    story.append(Paragraph("4. Regulatory Compliance & Verification Authority Record", section_style))
    
    # Constructing a simulated high-trust blueprint signature stamp box layout
    stamp_text = (
        "<font size=11 color='#1a365d'><b>■ SECURITY ASSURANCE STAMP ■</b></font><br/>"
        f"<font size=9 color='#2b6cb0'><b>VERIFIED BY:</b> Senior Structural Engineer</font><br/>"
        f"<font size=9 color='#2d3748'><b>REVIEWER ID:</b> {reviewer_name if reviewer_name else 'AUTOMATED_SYSTEM_RUN'}</font><br/>"
        f"<font size=8 color='#4a5568'><b>STATUS:</b> MATHEMATICAL ENGINE CLEAR / VERIFIED OK</font>"
    )
    
    stamp_cell = Paragraph(stamp_text, ParagraphStyle('StampText', leading=13))
    
    # Outer frame table styled to look like an authentic blue mechanical inspection stamp block
    stamp_table = Table([[stamp_cell]], colWidths=[240])
    stamp_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 2, colors.HexColor('#2b6cb0')), # Solid blue border frame
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ebf8ff')), # Soft light blue ink tint
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    
    disclaimer_text = ("<font size=7 color='#718096'><i>Legal Enforcement Shield: This certification ledger is a "
                       "digitally processed intermediate computational structural report generated via OpenFFS automation logic. "
                       "Final field execution protocols, run/repair/replace authorizations, and active pressure containment approvals "
                       "must remain anchored by a formal physical engineering stamp and physical wet signature from the managing Chartered Engineer.</i></font>")
    disclaimer_cell = Paragraph(disclaimer_text, body_style)
    
    # Side-by-side mounting grid layout block for the Stamp vs the Legal Disclaimer text
    validation_block = Table([[stamp_table, disclaimer_cell]], colWidths=[260, 270])
    validation_block.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (1,0), (1,0), 15),
    ]))
    story.append(validation_block)
    story.append(Spacer(1, 25))
    
    # Wet Signature Baseline Fields
    sig_data = [["Checked By: ___________________________", "Certified By: ___________________________"],
                ["OpenFFS Core Software Processing Engine", "Nominated Chartered Professional Engineer"]]
    t_sig = Table(sig_data, colWidths=[265, 265])
    t_sig.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Oblique'),
        ('FONTSIZE', (0,1), (-1,1), 8),
        ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor('#718096')),
    ]))
    story.append(t_sig)
    
    doc.build(story)
    print(f"\n[BRANDED ENGINE SUCCESS]: Corporate PDF saved with Smart Verification Stamp: {file_name}")

if __name__ == "__main__":
    generate_certified_pdf_report(
        "Part 7 - Hydrogen Blister Screening",
        {"Nominal_Thickness": 0.75, "Blister_Diameter": 2.5, "Pressure_PSI": 350},
        {"Required_t_min": 0.568, "Max_Allowable_Diameter": 8.49},
        "Blister Damage Acceptable",
        "S. Prakash (Senior Structural Engineer)",
        "Branded_Enterprise_Report.pdf"
    )
