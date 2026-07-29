import streamlit as st

st.title("Open FFS Initiative Software Engineering")

# 1. Dropdown Selection
# 1. Dropdown Selection
module = st.selectbox(
    "Select an Engineering Track Module to Run:",
    [
        "API 579 Part 3 - Low-Temperature Brittle Fracture", 
        "API 579 Part 4 - General Metal Loss", 
        "API 579 Part 5 - Local Metal Loss",
        "AISC Structural FFS - Columns Assessment",
        "AISC Structural FFS - Beams Assessment",
        "AISC Structural FFS - Braces & Ties Assessment"
    ]
)

)

st.write(f"### Active Module: {module}")

# 2. File Uploader Widget
uploaded_file = st.file_uploader("Upload your Site Inspection Report (TXT, CSV, or PDF)", type=["txt", "csv", "pdf"])

if uploaded_file is not None:
    st.success("Report uploaded successfully!")

# 3. Numeric Inputs for FFS Calculation
st.subheader("Engineering Design Parameters")
pressure = st.number_input("Enter Design Operating Pressure (psi):", min_value=0.0, value=100.0)
depth = st.number_input("Enter Local Crack/Flaw Depth (inches):", min_value=0.0, value=0.1)

# 4. Action Button
if st.button("Run FFS Assessment"):
    st.info("Running Fitness-For-Service calculations...")
    st.metric(label="Calculated Reduced MAWP (psi)", value=f"{pressure * 0.85:.2f}")
