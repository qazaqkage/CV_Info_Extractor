import streamlit as st
from pathlib import Path
from main import process_last_cv

# Directory to store uploaded CVs
CVS_DIR = Path("data/cvs")
CVS_DIR.mkdir(parents=True, exist_ok=True)

st.title("📄 CV Uploader and Key Info Extractor")

# Upload CV
uploaded_cv = st.file_uploader("Upload your CV (PDF only):", type=["pdf"])

if uploaded_cv:
    # Save the uploaded file
    cv_path = CVS_DIR / uploaded_cv.name
    with open(cv_path, "wb") as f:
        f.write(uploaded_cv.getbuffer())
    st.success(f"Uploaded CV saved as: {uploaded_cv.name}")

    # Process the last uploaded CV
    if st.button("Extract Key Information"):
        with st.spinner("Processing the CV with LLM..."):
            try:
                key_info = process_last_cv()
                st.write("### Extracted Information:")
                st.json(key_info)
            except Exception as e:
                st.error(f"An error occurred: {e}")
