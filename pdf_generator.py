import os
from io import BytesIO
from docx import Document
from pypdf import PdfReader
# Note: Keep your existing PDF creation imports here (e.g., reportlab, fpdf, etc.)

def extract_docx_tables(file_bytes):
    """
    Extracts structured text from all tables within an uploaded .docx file.
    """
    try:
        doc = Document(BytesIO(file_bytes))
        extracted_data = []
        
        for table_idx, table in enumerate(doc.tables):
            table_text = [f"--- Table {table_idx + 1} ---"]
            for row in table.rows:
                # Collect and clean text from every cell in the row
                row_cells = [cell.text.strip() for cell in row.cells]
                table_text.append(" | ".join(row_cells))
            extracted_data.append("\n".join(table_text))
            
        return "\n\n".join(extracted_data) if extracted_data else "No tables found in document."
    except Exception as e:
        return f"[Error parsing DOCX content: {str(e)}]"

def extract_pdf_text(file_bytes):
    """
    Extracts text blocks from an uploaded .pdf file reference.
    """
    try:
        reader = PdfReader(BytesIO(file_bytes))
        extracted_text = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(f"--- PDF Page {idx + 1} ---\n{text.strip()}")
        return "\n\n".join(extracted_text) if extracted_text else "No extractable text found in PDF."
    except Exception as e:
        return f"[Error parsing PDF content: {str(e)}]"

def compile_compliance_pdf(report_metadata, uploaded_files_list):
    """
    Your core engine compiled report constructor function.
    Retains all your existing design metrics calculation loops.
    """
    print(f"Initializing document compilation pipeline for: {report_metadata.get('doc_ref')}")
    
    # 1. Base Structure Setup
    # [Retain your existing canvas initialization / background code here]
    
    # 2. Append Structural Operational Parameters 
    # [Retain your existing layout construction for Cross-Section Loss and Perforation Diameters]
    
    # 3. Dynamic Multi-Format Reference Attachment Router
    extracted_appendices = {}
    
    if uploaded_files_list:
        for file_obj in uploaded_files_list:
            file_name = file_obj.name
            file_extension = os.path.splitext(file_name)[1].lower()
            file_bytes = file_obj.read()  # Safely read Streamlit file wrapper bytes memory buffer
            
            if file_extension in ['.jpg', '.jpeg', '.png']:
                # ROUTE IMAGES: Keep your original image-handling layout injection logic here
                # example_render_image_element(file_bytes)
                pass
                
            elif file_extension == '.docx':
                # ROUTE WORD FILES: Parse text table records
                table_content = extract_docx_tables(file_bytes)
                extracted_appendices[file_name] = table_content
                
            elif file_extension == '.pdf':
                # ROUTE PDF FILES: Parse structural document text contents 
                pdf_content = extract_pdf_text(file_bytes)
                extracted_appendices[file_name] = pdf_content
                
            else:
                # ROUTE OTHERS: Log general unknown raw attachment configurations safely without breaking 
                extracted_appendices[file_name] = f"Attached raw resource binary file asset reference ({len(file_bytes)} bytes)."

    # 4. Write Extracted Document Appendices to the Final PDF Canvas Layout
    if extracted_appendices:
        # [Use your existing framework flow to append a new page/section layout titled 'ANNEX: External References Data']
        for doc_title, content in extracted_appendices.items():
            print(f"Injecting text logs from reference document source: {doc_title}")
            # Target implementation snippet:
            # your_pdf_text_write_method(f"Source File Name: {doc_title}")
            # your_pdf_text_write_method(content)
            
    # 5. Final Output Canvas Compilation
    # return final_compiled_pdf_stream
    print("Report document successfully generated.")
