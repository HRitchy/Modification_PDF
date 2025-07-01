import streamlit as st
import fitz  # PyMuPDF
import tempfile
import io
from PyPDF2 import PdfWriter

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_text = []
    for page in doc:
        all_text.append(page.get_text())
    doc.close()
    return all_text

# Fonction pour remplacer un texte dans toutes les pages d'un PDF
def replace_text_in_pdf(pdf_bytes, search_text, replace_text):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        text_instances = page.search_for(search_text)
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(255,255,255))
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
        for inst in text_instances:
            page.insert_textbox(inst, replace_text, fontsize=12, color=(0,0,0))
    temp_pdf = io.BytesIO()
    doc.save(temp_pdf)
    doc.close()
    temp_pdf.seek(0)
    return temp_pdf

st.title("Modifier le texte d'un PDF")

uploaded_pdf = st.file_uploader("Importer un PDF", type=["pdf"])

if uploaded_pdf:
    pdf_bytes = uploaded_pdf.read()
    st.subheader("Aperçu du texte extrait :")
    all_text = extract_text_from_pdf(pdf_bytes)
    for i, page_text in enumerate(all_text):
        st.markdown(f"**Page {i+1}:**")
        st.write(page_text)
    
    search_text = st.text_input("Texte à remplacer")
    replace_text_val = st.text_input("Nouveau texte")

    if st.button("Remplacer et Exporter") and search_text and replace_text_val:
        result_pdf = replace_text_in_pdf(pdf_bytes, search_text, replace_text_val)
        st.success("Texte remplacé. Cliquez ci-dessous pour télécharger le PDF modifié.")
        st.download_button(
            label="Télécharger le PDF modifié",
            data=result_pdf,
            file_name="pdf_modifie.pdf",
            mime="application/pdf"
        )
