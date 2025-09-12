import os
import streamlit as st
from ocr_utils import extract_text_from_pdf
from translate_utils import translate_hi_en
from ipc_predictor import predict_ipc_sections

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

st.title("FIR Analysis Tool")


uploaded_file = st.file_uploader("Upload FIR PDF", type=["pdf"])

if uploaded_file:
    st.info("⏳ Extracting text from PDF...")
    hindi_text = extract_text_from_pdf(uploaded_file)

    if hindi_text:
        st.info("⏳ Translating + Summarizing with Groq...")
        english_summary = translate_hi_en(hindi_text)

       
        st.subheader("📌 Case Summary (English)")
        st.text_area("Summary:", english_summary, height=200)

        st.info("⏳ Predicting IPC Sections...")
        ipc_predictions = predict_ipc_sections(english_summary, top_k=3)

    
        if ipc_predictions:
            st.subheader("📖 Suggested IPC Sections")
            for ipc in ipc_predictions:
                st.markdown(f"""
                **IPC Section**  
                {ipc['Offense']}  

                **Description**  
                {ipc['Description']}  
                """)
                st.markdown("---")
        else:
            st.error("No relevant IPCs found.")

    else:
        st.error("No text extracted from the PDF.")


