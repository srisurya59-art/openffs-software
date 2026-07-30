# --- Generation Action Block ---
st.write("---")

if st.button("🚀 Compile Standalone FFS Level 1 Screening Report", use_container_width=True):
    with st.spinner("Processing file attachments and compiling compliance matrix..."):
        
        # 1. Router Logic for files (Kept from previous step)
        valid_images = []
        appended_documents = []
        if uploaded_files:
            for file in uploaded_files:
                import os
                file_extension = os.path.splitext(file.name).lower()
                if file_extension in ['.jpg', '.jpeg', '.png']:
                    valid_images.append(file)
                else:
                    appended_documents.append(file.name)
        
        # 2. Trigger the actual PDF backend compilation
        # (Assuming your pdf_generator script outputs bytes or a file stream)
        try:
            from pdf_generator import compile_compliance_pdf
            
            report_metadata = {
                "doc_ref": doc_ref,
                "cross_section_loss": cross_section_loss,
                "max_perforation": max_perforation
            }
            
            # This calls your generator script and builds the PDF data into memory
            pdf_bytes = compile_compliance_pdf(report_metadata, uploaded_files)
            
            # 3. UI Confirmation Messages
            st.success(f"Compliance Report {doc_ref} successfully initialized!")
            st.info(f"**Parameters Logged:** Area Loss: {cross_section_loss}% | Perforation Limit: {max_perforation}mm")
            
            if valid_images or appended_documents:
                st.markdown("### 📎 Compiled Attachments Summary:")
                if valid_images:
                    st.write(f"🖼️ **Rendered Images ({len(valid_images)}):** {', '.join([f.name for f in valid_images])}")
                if appended_documents:
                    st.write(f"📁 **Appended Document References ({len(appended_documents)}):** {', '.join(appended_documents)}")
            
            # 4. ADDED: The download button widget that exposes the file to your web browser
            st.write("---")
            st.download_button(
                label="📥 Download Completed Assessment Report (PDF)",
                data=pdf_bytes,
                file_name=f"{doc_ref}_FFS_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Failed to generate download link: {str(e)}")
