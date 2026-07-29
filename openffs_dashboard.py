import streamlit as st

st.title("Open FFS Initiative Software Engineering")

module = st.selectbox(
    "Select an API 579 Engineering Track Module to Run:",
    [
        "Part 3 - Low-Temperature Brittle Fracture", 
        "Part 4 - General Metal Loss", 
        "Part 5 - Local Metal Loss",
        "Part 6 - Pitting Damage",
        "Part 7 - Hydrogen Blister and HIC Damage",
        "Part 9 - Crack-like Flaws Structural Assessment",
        "Part 14 - Paris' Law Fatigue Crack Life Integration"
    ]
)

st.write(f"### Active Module: {module}")
st.info("The application interface is now running smoothly in the cloud.")
