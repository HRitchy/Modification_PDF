import streamlit as st
import fitz  # PyMuPDF
import io

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_text = []
    for page in doc:
        all_text.append(page.get_text())
    doc.close()
    return all_text

def erase_text_in_pdf(pdf_bytes, search_text):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        text_instances = page.search_for(search_text)
        for inst in text_instances:
            # Ajouter une annotation de rédaction (blanc) pour effacer le texte
            page.add_redact_annot(inst, fill=[1,1,1])
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
    temp_pdf = io.BytesIO()
    doc.save(temp_pdf)
    doc.close()
    temp_pdf.seek(0)
    return temp_pdf

st.title("Effacer un texte d'un PDF")

uploaded_pdf = st.file_uploader("Importer un PDF", type=["pdf"])

if uploaded_pdf:
    pdf_bytes = uploaded_pdf.read()
    st.subheader("Aperçu du texte extrait :")
    all_text = extract_text_from_pdf(pdf_bytes)
    for i, page_text in enumerate(all_text):
        st.markdown(f"**Page {i+1}:**")
        st.write(page_text)
    
    search_text = st.text_input("Texte à effacer")

    if st.button("Effacer et Exporter") and search_text:
        result_pdf = erase_text_in_pdf(pdf_bytes, search_text)
        st.success("Texte effacé. Cliquez ci-dessous pour télécharger le PDF modifié.")
        st.download_button(
            label="Télécharger le PDF modifié",
            data=result_pdf,
            file_name="pdf_texte_efface.pdf",
            mime="application/pdf"
        )
