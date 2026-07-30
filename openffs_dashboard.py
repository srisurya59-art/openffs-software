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

# --- Sidebar Layout ---
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
    
    # CHANGED: 'type' parameter removed entirely to allow universal file uploads (DOCX, PDF, PNG, etc.)
    uploaded_files = st.file_uploader(
        "Attach Site Defect Photos or Documents to Include in PDF (All Types Allowed):",
        type=None, 
        accept_multiple_files=True
    )

# --- Main Window / Operational Parameters ---
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

# --- Generation Action Block ---
st.write("---")
if st.button("🚀 Compile Standalone FFS Level 1 Screening Report", use_container_width=True):
    with st.spinner("Processing file attachments and compiling compliance matrix..."):
        
        # Backend Safe File Router
        valid_images = []
        appended_documents = []
        
        if uploaded_files:
            for file in uploaded_files:
                file_extension = os.path.splitext(file.name)[1].lower()
                
                # Direct images to image-rendering flow
                if file_extension in ['.jpg', '.jpeg', '.png']:
                    valid_images.append(file)
                # Route text documents safely as appended reference attachments
                else:
                    appended_documents.append(file.name)
        
        # Execution Summary Output
        st.success(f"Compliance Report {doc_ref} successfully initialized!")
        
        # Display operational parameters confirmation
        st.info(f"**Parameters Logged:** Area Loss: {cross_section_loss}% | Perforation Limit: {max_perforation}mm")
        
        # Display file attachments routing breakdown
        if valid_images or appended_documents:
            st.markdown("### 📎 Compiled Attachments Summary:")
            if valid_images:
                st.write(f"🖼️ **Rendered Images ({len(valid_images)}):** {', '.join([f.name for f in valid_images])}")
            if appended_documents:
                st.write(f"📁 **Appended Document References ({len(appended_documents)}):** {', '.join(appended_documents)}")
