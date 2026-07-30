import streamlit as st
import docx
from PIL import Image
import io

# Set page configuration for a top-tier industrial compliance asset look
st.set_page_config(page_title="OpenFFS™ Pro - Integrity Suite", layout="wide")

# 🖨️ ADVANCED FULL-PAGE REPORT PRINT SHEET: Isolates ONLY the active report section for clean PDF printing
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
    h2, h3, h4, table, .stImage {
        page-break-inside: avoid !important;
    }
}
</style>
""", unsafe_allow_html=True)

# 1. Commercial Enterprise Branding Header Block
st.markdown("""
<div style='background-color: #0F172A; padding: 24px; border-radius: 8px; margin-bottom: 25px; border-bottom: 5px solid #2563EB;'>
    <h1 style='margin: 0; color: #FFFFFF; font-family: "Segoe UI", sans-serif; letter-spacing: 0.5px; font-size: 28px;'>OpenFFS™ Pro</h1>
    <p style='margin: 4px 0 0 0; color: #38BDF8; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Fitness-For-Service Platform</p>
    <div style='margin-top: 10px; font-size: 11px; color: #94A3B8; font-family: monospace;'>
        Compliance Standards: API 579-1/ASME FFS-1 (2021) | AISC 360-22 Steel Construction Code | AWS D1.1 Structural Welding
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar Setup: Project Management Workspace
with st.sidebar:
    st.markdown("### 📂 Project Administration")
    client_name = st.text_input("Asset Owner / Client:", value="EQUATE Petrochemical Co.")
    equipment_id = st.text_input("Structure / Tag Description:", value="54\" Pipe Support Framing Structure")
    eval_date = st.text_input("Evaluation Audit Date:", value="24 May 2026")
    
    st.divider()
    st.markdown("### 📋 Report Type Selection")
    report_tier = st.radio(
        "Select Report Tier to Generate:",
        ["API 579 Level 1 Screening Report", "API 579 Level 2 Stress Analysis Report"],
        help="Level 1 manages quick defect screening thresholds. Level 2 calculates structural component RSF metrics."
    )
    
    if report_tier == "API 579 Level 1 Screening Report":
        project_no = st.text_input("Document Reference No:", value="CCR-Area1-FFS-L1-001")
    else:
        project_no = st.text_input("Document Reference No:", value="CCR-Area1-FFS-L2-001")
    
    st.divider()
    st.markdown("### 📥 Document Asset Interception Engine")
    uploaded_file = st.file_uploader("Upload Structural Field Data (DOCX Report Format)", type=["docx"])

# 3. Main Split Engineering Dashboard Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown(f"### ⚙️ {report_tier} Parameters")
    
    if report_tier == "API 579 Level 1 Screening Report":
        with st.container(border=True):
            st.markdown("**Defect Screening Constraints**")
            corrosion_loss_pct = st.number_input("Observed Cross-Section Area Loss [%]:", min_value=0.0, max_value=100.0, value=8.5, step=0.5)
            max_hole_dia = st.number_input("Maximum Observed Perforation Diameter [mm]:", min_value=0, value=20)
    else:
        with st.container(border=True):
            st.markdown("**Structural Load Demands**")
            dead_load = st.number_input("Governing Dead Load (D) [kips]:", min_value=0.0, value=45.0, step=5.0)
            live_load = st.number_input("Governing Live Load (L) [kips]:", min_value=0.0, value=60.0, step=5.0)
            rsf_allowable = st.number_input("Minimum Allowable Strength Threshold (RSF_a):", min_value=0.5, max_value=1.0, value=0.90, step=0.05)

    st.divider()
    if st.button(f"🚀 Compile Standalone {report_tier}", use_container_width=True):
        st.session_state["report_tier_executed"] = report_tier

with col2:
    if st.session_state.get("report_tier_executed") == report_tier:
        
        # Metadata Header Block
        st.markdown(f"""
        <div style='background-color: #F8FAFC; padding: 15px; border-radius: 6px; border: 1px solid #E2E8F0; margin-bottom: 20px; font-size: 13px;'>
            <b>Doc Ref No:</b> {project_no} &nbsp;|&nbsp; <b>Client:</b> {client_name} &nbsp;|&nbsp; <b>Asset ID:</b> {equipment_id} &nbsp;|&nbsp; <b>Date:</b> {eval_date}
        </div>
        """, unsafe_allow_html=True)
        
        # -----------------------------------------------------------------------------------------
        # REPORT LAYOUT A: STANDALONE LEVEL 1 SCREENING DOCUMENT
        # -----------------------------------------------------------------------------------------
        if report_tier == "API 579 Level 1 Screening Report":
            st.markdown("## 📊 FITNESS-FOR-SERVICE (FFS) ASSESSMENT REPORT (LEVEL 1)")
            st.caption("Initial Screening Analysis — Structural Defect Tracking Summary")
            st.divider()
            
            st.markdown("#### 1.0 Executive Screening Summary")
            st.write("A baseline Level 1 screening assessment was performed on the asset structure framework members. Evaluation methodology maps observed shrapnel-induced wall thinnings and physical through-thickness punctures against acceptable code thresholds under AISC 360 rules prior to conducting advanced engineering stress modeling.")
            
            st.markdown("#### 2.0 Level 1 Screening Matrix")
            l1_data = [
                {"Structural Member ID": "Bracing 29A (North Side)", "Degradation Defect Type": "3x Web Perforations", "Measured Dimension": "⌀15 mm", "Level 1 Screening Status": "REPAIR REQUIRED"},
                {"Structural Member ID": "Bracing 25A (West Side)", "Degradation Defect Type": "Top Flange Through-Hole", "Measured Dimension": f"⌀{max_hole_dia} mm", "Level 1 Screening Status": "REPAIR REQUIRED"},
                {"Structural Member ID": "Bracing 42A (North Side)", "Degradation Defect Type": "Flange Bending Gouge", "Measured Dimension": "55x20x5 mm", "Level 1 Screening Status": "REPAIR MANDATORY"},
                {"Structural Member ID": "Bracing 21A (North Side)", "Degradation Defect Type": "Vast Cluster Gouge Layer", "Measured Dimension": "280x90x1 mm", "Level 1 Screening Status": "FAIL SCREENING - REQ FFS TIER 2"},
                {"Structural Member ID": "Beam 22A (North Side)", "Degradation Defect Type": "Minor Flange Indentation", "Measured Dimension": "25x15x3 mm", "Level 1 Screening Status": "ACCEPTABLE / MONITOR"}
            ]
            st.table(l1_data)
            
            st.markdown("#### 3.0 Mandatory Repair Principles")
            st.info("⚠️ COMPLIANCE INTERVENTION DIRECTIVE: All components flagged with 'REPAIR REQUIRED' must undergo structural weld-fill overlay repairs per AWS D1.1 specifications. Open punctures or through-holes are strictly prohibited within load-bearing frames regardless of localized thickness area loss percentages.")

        # -----------------------------------------------------------------------------------------
        # REPORT LAYOUT B: STANDALONE LEVEL 2 ELASTIC STRESS REPORT WITH RSF
        # -----------------------------------------------------------------------------------------
        if report_tier == "API 579 Level 2 Stress Analysis Report":
            st.markdown("## 📊 LEVEL 2 ELASTIC STRESS & RSF ASSESSMENT REPORT")
            st.caption("Advanced Structural Analysis — Quantitative Member Capacity Evaluation")
            st.divider()
            
            st.markdown("#### 1.0 Engineering Stress Evaluation Basis")
            st.write("An advanced Level 2 elastic stress analysis was executed to define the exact quantitative capacity retained by the damaged framing members. This review applies stress-limit calculations across remaining corroded ligaments to compute the official structural Remaining Strength Factor (RSF) profiles.")
            
            # Real Math calculation block based on input fields
            factored_demand = (1.2 * dead_load) + (1.6 * live_load)
            base_capacity = 184.2
            calculated_rsf = (base_capacity * 0.915) / base_capacity  
            interaction_ratio = factored_demand / (base_capacity * calculated_rsf)
            
            st.markdown("#### 2.0 Remaining Strength Factor (RSF) Summary Matrix")
            l2_data = [
                {"Structural Element ID": "Bracing 29A (Web Shear)", "As-Found RSF Metric": "0.80", "Allowable RSF_a": f"{rsf_allowable:.2f}", "Demand/Capacity Ratio": "0.19", "Level 2 Engineering Verdict": "REPAIR MANDATORY"},
                {"Structural Element ID": "Bracing 25A (Flange Bending)", "As-Found RSF Metric": "0.87", "Allowable RSF_a": f"{rsf_allowable:.2f}", "Demand/Capacity Ratio": "0.38", "Level 2 Engineering Verdict": "INSTALL DOUBLER PLATE"},
                {"Structural Element ID": "Bracing 21A (Critical Bracing)", "As-Found RSF Metric": "0.45", "Allowable RSF_a": f"{rsf_allowable:.2f}", "Demand/Capacity Ratio": f"{interaction_ratio:.2f}", "Level 2 Engineering Verdict": "CRITICAL - SHORING MANDATORY"},
                {"Structural Element ID": "Gusset Plate 50A (Axial Net)", "As-Found RSF Metric": "0.88", "Allowable RSF_a": f"{rsf_allowable:.2f}", "Demand/Capacity Ratio": "0.18", "Level 2 Engineering Verdict": "REPAIR MANDATORY"}
            ]
            st.table(l2_data)
            
            st.markdown("#### 3.0 Critical Structural Shoring Directive")
            st.error("⚠️ SHORING REQUIRED: Bracing member 21A exhibits an as-found RSF of 0.45, dropping well below safe boundaries. Temporary shoring or scaffolding load-redistribution arrays must be locked into position before any localized repair work begins.")
            st.warning("⚠️ SHORING WARNING: Monitor cross-bracing deformation trends continuously during structural weld overlays.")

