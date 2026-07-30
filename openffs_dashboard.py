import streamlit as st
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="OpenFFS™ Pro - Advanced Fitness-For-Service",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Title Header ---
st.title("OpenFFS™ Pro")
st.caption("Fitness-For-Service Production Platform | Compliance Tiers: API 579-1/ASME FFS-1 | AISC 360 Steel Code")

# --- Sidebar Configuration Layout ---
with st.sidebar:
    st.header("📋 Standard & Part Selection")
    design_code = st.selectbox(
        "Applicable Design Code / Part Track:",
        ["AISC Structural FFS Comprehensive", "API 579 Level 1 Assessment", "ASME FFS-1 Core Track"]
    )
    
    st.header("📄 Report Output Protocol")
    report_type = st.radio(
        "Select Report Deliverable to Compile:",
        ("FFS Level 1 Screening Report", "FFS Level 2 Stress Analysis Report")
    )
    
    doc_ref = st.text_input("Document Reference No:", value="CCR-Area1-FFS-L1-001")

    st.header("📎 Field Asset Photography Link")
    # Universal file uploader configuration
    uploaded_files = st.file_uploader(
        "Attach Site Defect Photos or Documents to Include in PDF (All Types Allowed):",
        type=None, 
        accept_multiple_files=True
    )

# --- Main Canvas Application Parameters ---
st.header("⚙️ Operational Parameters")
with st.container():
    st.subheader("Defect Geometry Screening Boundaries")
    
    col1, col2 = st.columns(2)
    with col1:
        cross_section_loss = st.number_input(
            "Observed Cross-Section Area Loss (%):", 
            min_value=0.00, max_value=100.00, value=8.50, step=0.01
        )
    with col2:
        max_perforation = st.number_input(
            "Maximum Observed Perforation Diameter (mm):", 
            min_value=0, max_value=1000, value=20, step=1
        )

# --- Separation Line & Compilation Trigger Interaction Block ---
st.write("---")

if st.button("🚀 Compile Standalone FFS Level 1 Screening Report", use_container_width=True):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one document or photo file to compile the assessment report.")
    else:
        with st.spinner("Processing file attachments and compiling compliance matrix..."):
            try:
                # Import your backend processing engine pipeline safely inside execution context
                from pdf_generator import compile_compliance_pdf
                
                report_metadata = {
                    "doc_ref": doc_ref,
                    "cross_section_loss": cross_section_loss,
                    "max_perforation": max_perforation
                }
                
                # Directly hand off files array to the backend engine to build the bytes buffer stream
                pdf_bytes = compile_compliance_pdf(report_metadata, uploaded_files)
                
                # Print clean, production-grade interface confirmation cards
                st.success(f"✅ Compliance Report {doc_ref} successfully initialized!")
                st.info(f"📊 **Parameters Logged:** Area Loss: {cross_section_loss}% | Perforation Limit: {max_perforation}mm")
                
                # Display clean file attachments summary directly out of safe runtime definitions
                st.markdown("### 📎 Compiled Attachments Summary:")
                for file in uploaded_files:
                    f_ext = os.path.splitext(file.name)[1].lower()
                    icon = "🖼️" if f_ext in ['.jpg', '.jpeg', '.png'] else "📁"
                    st.write(f"{icon} **File Registered:** {file.name} ({f_ext.upper()} asset layout layout format)")
                
                # Expose the download widget link to send file asset back to user web browser
                st.write("---")
                st.download_button(
                    label="📥 Download Completed Assessment Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"{doc_ref}_FFS_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Failed to execute download compilation script breakdown pipeline: {str(e)}")
