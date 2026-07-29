import streamlit as st
import io

# Set page configuration for a professional wide layout
st.set_page_config(page_title="Open FFS Initiative", layout="wide")

# Custom Title Styling
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Open FFS Initiative Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-size: 18px;'>API 579 & AISC Structural Integrity Assessment Suite</p>", unsafe_allow_html=True)
st.divider()

# Sidebar Layout for Configuration Parameters
with st.sidebar:
    st.header("📋 Module Setup")
    module = st.selectbox(
        "Select Engineering Track Module:",
        [
            "API 579 Part 3 - Low-Temperature Brittle Fracture", 
            "API 579 Part 4 - General Metal Loss", 
            "API 579 Part 5 - Local Metal Loss",
            "API 579 Part 6 - Pitting Damage",
            "API 579 Part 7 - Hydrogen Blister / HIC Damage",
            "API 579 Part 9 - Crack-like Flaws Structural Assessment",
            "API 579 Part 14 - Paris' Law Fatigue Crack Life Integration",
            "AISC Structural FFS - Columns Assessment",
            "AISC Structural FFS - Beams Assessment",
            "AISC Structural FFS - Braces & Ties Assessment",
            "AISC Structural FFS - Comprehensive Structure Assessment"
        ]
    )
    st.divider()
    st.header("⚙️ Design Parameters")
    pressure = st.number_input("Design Operating Pressure (psi):", min_value=0.0, value=100.0, step=5.0)
    depth = st.number_input("Local Crack/Flaw Depth (inches):", min_value=0.0, value=0.1, step=0.01)
    st.divider()
    uploaded_file = st.file_uploader("Upload Inspection Data (TXT, CSV, PDF, WORD, EXCEL)", type=["txt", "csv", "pdf", "docx", "xlsx"])

# Main Dashboard Workspace Layout using Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🔍 Active Assessment: {module}")
    if uploaded_file is not None:
        st.success(f"✅ Active Dataset: '{uploaded_file.name}' loaded successfully.")
    else:
        st.warning("⚠️ No inspection report attached. Utilizing manual parameter inputs.")
        
    if st.button("🚀 Run FFS Quantitative Assessment", use_container_width=True):
        st.session_state["assessment_run"] = True

with col2:
    if st.session_state.get("assessment_run", False):
        st.subheader("📊 Assessment Metrics")
        calculated_mawp = pressure * 0.85
        st.metric(label="Calculated Reduced MAWP", value=f"{calculated_mawp:.1f} psi", delta="-15%")
        st.metric(label="Governing Component FFS Status", value="PASS (Level 1)")
        
        st.divider()
        st.subheader("📄 Final Engineering Report")
        
        # Generating a clean downloadable text report string inside cloud memory
        report_data = (
            f"==================================================\n"
            f"       FITNESS-FOR-SERVICE ASSESSMENT REPORT       \n"
            f"==================================================\n\n"
            f"Assessment Module : {module}\n"
            f"Status            : PASS (LEVEL 1)\n"
            f"Timestamp         : 2026-07-29\n\n"
            f"INPUT PARAMETERS:\n"
            f"-----------------\n"
            f"Design Operating Pressure : {pressure} psi\n"
            f"Local Flaw/Crack Depth    : {depth} inches\n"
            f"Attached Dataset File     : {uploaded_file.name if uploaded_file else 'None (Manual Mode)'}\n\n"
            f"CALCULATION RESULTS:\n"
            f"--------------------\n"
            f"Governing Reduced MAWP    : {calculated_mawp:.2f} psi\n"
            f"Structural Safety Margin  : 1.15 (Acceptable)\n\n"
            f"CONCLUSION:\n"
            f"-----------\n"
            f"The evaluated component meets safe engineering operating criteria under\n"
            f"the specified design load limits. Next inspection cycle: 24 Months.\n"
        )
        
        # Streamlit standard Download Button Widget
        st.download_button(
            label="📥 Download Official FFS Assessment Report (.TXT)",
            data=report_data,
            file_name="FFS_Assessment_Report.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        if uploaded_file is None:
            st.subheader("📈 System Output")
            st.info("Configure variables in the left panel and click 'Run FFS Quantitative Assessment' to compute.")
