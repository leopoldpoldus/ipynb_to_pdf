import os
import tempfile
import shutil
import base64
import streamlit as st
from nbconvert import PDFExporter
import nbformat

st.set_page_config(page_title="Jupyter Notebook to PDF Converter", page_icon=":books:")

st.title("Jupyter Notebook to PDF Converter")
st.write("Upload your Jupyter Notebook and convert it to a PDF file.")


def convert_notebook_to_pdf(notebook):
    pdf_data = None
    error_message = None

    try:
        nb_node = nbformat.reads(notebook, as_version=4)
        pdf_exporter = PDFExporter()
        pdf_data, resources = pdf_exporter.from_notebook_node(nb_node)

    except Exception as e:
        error_message = str(e)

    return pdf_data, error_message


def get_binary_file_downloader_link(file, file_label="Download", filename=None):
    if not filename:
        filename = f"{file_label}.pdf"
    with open(file, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/pdf;base64,{b64}" download="{filename}">{file_label}</a>'
    return href


uploaded_file = st.file_uploader("Upload a Jupyter Notebook (.ipynb)", type=["ipynb"])

if uploaded_file is not None:
    notebook_content = uploaded_file.read().decode("utf-8")
    pdf_data, error_message = convert_notebook_to_pdf(notebook_content)

    if error_message:
        st.error(f"An error occurred during the conversion process: {error_message}")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_data)
            temp_pdf.flush()
            st.success("Conversion completed!")
            st.markdown(get_binary_file_downloader_link(temp_pdf.name, "Download PDF"), unsafe_allow_html=True)
else:
    st.warning("Please upload a Jupyter Notebook to convert.")

