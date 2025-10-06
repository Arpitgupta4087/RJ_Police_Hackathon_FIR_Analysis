import os
import streamlit as st
from ocr_utils import extract_text_from_pdf
from translate_utils import translate_hi_en
from ipc_predictor import predict_ipc_sections
from database import init_db, save_fir_data

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

try:
    init_db()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

st.title("⚖️ FIR → IPC Analysis Tool")

uploaded_file = st.file_uploader("Upload FIR PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Analyzing PDF... This may take a moment."):
        hindi_text = extract_text_from_pdf(uploaded_file)

        if not hindi_text:
            st.error("No text could be extracted from the PDF.")
            st.stop()

        english_summary = translate_hi_en(hindi_text)
        ipc_predictions = predict_ipc_sections(english_summary, top_k=3)

    st.subheader("📌 Case Summary (English)")
    st.text_area("Summary:", english_summary, height=200)

    if ipc_predictions:
        st.subheader("📖 Suggested IPC Sections")
        for ipc in ipc_predictions:
            st.markdown(f"""
            **IPC Section:** {ipc['Offense']}  
            **Description:** {ipc['Description']}
            """)
            st.markdown("---")
    else:
        st.warning("Could not predict relevant IPC sections.")

    if st.button("Save Analysis to Database"):
        try:
            pdf_bytes = uploaded_file.getvalue()
            save_fir_data(uploaded_file.name, pdf_bytes, english_summary, ipc_predictions)
            st.success("✅ Case data successfully saved to the database!")
        except Exception as e:
            st.error(f"❌ Failed to save data to the database. Error: {e}")
