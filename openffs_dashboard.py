import streamlit as st
import docx
from PIL import Image
import io

# Set page configuration for a premium, specialized engineering suite look
st.set_page_config(page_title="OpenFFS™ Pro - Advanced Fitness-For-Service Platform", layout="wide")

# 🖨️ ADVANCED VISUAL CONTROL: Isolates ONLY the formal technical report card for PDF printing
st.markdown("""
<style>
@media print {
    [data-testid="stSidebar"], header, [data-testid="stHeader"], .stButton, div.element-container:has(button) {
        display: none !important;
    }
    div[data-testid="column"]:first-child {
        display: none !important;
    }
    div[data-testid="column"]:last-child {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# 1. Commercial Enterprise Branding Header Block
st.markdown("""
<div style='background-color: #0F172A; padding: 24px; border-radius: 8px; margin-bottom: 25px; border-bottom: 5px solid #2563EB;'>
    <h1 style='margin: 0; color: #FFFFFF; font-family: "Segoe UI", sans-serif; letter-spacing: 0.5px; font-size: 28px;'>OpenFFS™ Pro</h1>
    <p style='margin: 4px 0 0 0; color: #38BDF8; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Fitness-For-Service Production Platform</p>
    <div style='margin-top: 10px; font-size: 11px; color: #94A3B8; font-family: monospace;'>
        Governing Compliance: API 579-1/ASME FFS-1 (2021) | AISC 360-22 Steel Construction Code | AWS D1.1 Structural Welding
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar Workspace: Project Metadata Configuration Panel
with st.sidebar:
    st.markdown("### 📂 Project Administration")
    client_name = st.text_input("Asset Owner / Client:", value="EQUATE Petrochemical Co.")
    equipment_id = st.text_input("Structure / Tag Description:", value="54\" Pipe Support Framing Structure")
    eval_date = st.text_input("Evaluation Audit Date:", value="30 July 2026")
    
    st.divider()
    st.markdown("### 📋 Standard & Part Selection")
    
    # Restored the critical engineering dropdown modules
    module = st.selectbox(
        "Applicable Design Code / Part Track:",
        [
            "AISC Structural FFS - Comprehensive Structure Assessment",
            "API 579 Part 3 - Low-Temperature Brittle Fracture", 
            "API 579 Part 4 - General Metal Loss", 
            "API 579 Part 5 - Local Metal Loss",
            "API 579 Part 6 - Pitting Damage",
            "API 579 Part 7 - Hydrogen Blister / HIC Damage",
            "API 579 Part 9 - Crack-like Flaws Structural Assessment",
            "API 579 Part 14 - Fatigue Crack Life Integration"
        ]
    )
    
    st.divider()
    st.markdown("### 📋 Report Output Protocol")
    report_tier = st.radio(
        "Select Report Deliverable to Compile:",
        ["FFS Level 1 Screening Report", "FFS Level 2 Stress Analysis Report"],
        help="Level 1 manages initial defect screening thresholds. Level 2 calculates structural component RSF metrics."
    )
    
    if report_tier == "FFS Level 1 Screening Report":
        project_no = st.text_input("Document Reference No:", value="CCR-Area1-FFS-L1-001")
    else:
        project_no = st.text_input("Document Reference No:", value="CCR-Area1-FFS-L2-001")
    
    st.divider()
    st.markdown("### 📥 Document Asset Interception Engine")
    uploaded_file = st.file_uploader("Upload Structural Field Data (DOCX Report Format)", type=["docx"])

# 3. Main Split Engineering Dashboard Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown(f"### ⚙️ Operational Parameters")
    
    if report_tier == "FFS Level 1 Screening Report":
        with st.container(border=True):
            st.markdown("**Defect Geometry Screening Boundaries**")
            corrosion_loss_pct = st.number_input("Observed Cross-Section Area Loss [%]:", min_value=0.0, max_value=100.0, value=8.5, step=0.5)
            max_hole_dia = st.number_input("Maximum Observed Perforation Diameter [mm]:", min_value=0, value=20)
    else:
        with st.container(border=True):
            st.markdown("**Structural Load Demands & Allowables**")
            dead_load = st.number_input("Governing Dead Load (D) [kips]:", min_value=0.0, value=45.0, step=5.0)
            live_load = st.number_input("Governing Live Load (L) [kips]:", min_value=0.0, value=60.0, step=5.0)
            rsf_allowable = st.number_input("Minimum Allowable Strength Threshold (RSF_a):", min_value=0.5, max_value=1.0, value=0.90, step=0.05)

    st.divider()
    if st.button(f"🚀 Compile Standalone {report_tier}", use_container_width=True):
        st.session_state["active_compiled_report"] = report_tier

with col2:
    if st.session_state.get("active_compiled_report") == report_tier:
        
        # -----------------------------------------------------------------------------------------
        # DELIVERABLE A: STANDALONE LEVEL 1 COMPONENT SCREENING MATRIX REPORT
        # -----------------------------------------------------------------------------------------
        if report_tier == "FFS Level 1 Screening Report":
            st.markdown(f"""
            <div style="background-color: #FFFFFF; padding: 30px; border: 1px solid #CBD5E1; border-top: 8px solid #0F172A; font-family: 'Segoe UI', sans-serif; color: #1E293B;">
                <div style="float: right; font-size: 11px; text-align: right; color: #64748B;">
                    <b>Doc Ref:</b> {project_no}<br><b>Date:</b> {eval_date}
                </div>
                <h2 style="color: #0F172A; margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.5px;">FITNESS-FOR-SERVICE (FFS) LEVEL 1 SCREENING REPORT</h2>
                <p style="color: #475569; margin: 4px 0 0 0; font-size: 12px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Governing Standard Track: {module}</p>
                
                <table style="width: 100%; margin-top: 20px; font-size: 12px; border-collapse: collapse;">
                    <tr style="background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 6px 0;"><b>Client / Asset Owner:</b></td><td>{client_name}</td>
                        <td style="padding: 6px 0;"><b>Structure Tag ID:</b></td><td>{equipment_id}</td>
                    </tr>
                </table>
                
                <h3 style="color: #1E3A8A; font-size: 14px; margin-top: 25px; border-bottom: 2px solid #E2E8F0; padding-bottom: 5px;">1.0 Executive Evaluation Summary</h3>
                <p style="font-size: 12.5px; line-height: 1.6; text-align: justify; margin-top: 8px;">
                    A Level 1 screening evaluation was executed for the core members of the structural framing system. Assessments were performed strictly in accordance with governing design rules, mapping observed shrapnel punctures, local wall thinning profiles, and cross-sectional dimension degradations against code-permissible screening bounds prior to launching rigorous finite element or Level 2 analytical models.
                </p>
                
                <h3 style="color: #1E3A8A; font-size: 14px; margin-top: 25px; border-bottom: 2px solid #E2E8F0; padding-bottom: 5px;">2.0 Component-Wise Screening Matrix</h3>
                <table style="width: 100%; font-size: 11.5px; border-collapse: collapse; margin-top: 10px; text-align: left;">
                    <thead>
                        <tr style="background-color: #0F172A; color: #FFFFFF;">
                            <th style="padding: 8px; border: 1px solid #1E293B;">Structural Member ID</th>
                            <th style="padding: 8px; border: 1px solid #1E293B;">Observed Local Degradation Profile</th>
                            <th style="padding: 8px; border: 1px solid #1E293B;">Measured Dimension</th>
                            <th style="padding: 8px; border: 1px solid #1E293B;">Screening Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>Columns 29A / 29B</b></td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0;">Localized Web Thinning (Mechanical Impact)</td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0;">{corrosion_loss_pct}% Local Area Loss</td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0; color: #D97706; font-weight: bold;">REPAIR RECOMMENDED</td>
                        </tr>
                        <tr style="background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>Floor Beams 25A</b></td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0;">Top Flange Through-Thickness Puncture</td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0;">⌀{max_hole_dia} mm Open Bore</td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0; color: #DC2626; font-weight: bold;">REPAIR MANDATORY</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E2E8F0;">
                            <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>Cross Bracings 21A</b></td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0;">Severe Structural Deformation Segment</td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0;">280x90mm Cluster Gouge</td>
                            <td style="padding: 8px; border: 1px solid #E2E8F0; color: #DC2626; font-weight: bold;">FAIL TIER 1 - REQ LEVEL 2</td>
                        </tr>
                        <tr style="background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0;">
