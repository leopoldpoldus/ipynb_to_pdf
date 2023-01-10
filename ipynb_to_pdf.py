import streamlit as st
import nbconvert


def convert_notebook():
    uploaded_file = st.file_uploader("Choose a Jupyter notebook to convert to PDF", type=["ipynb"])
    if uploaded_file is not None:
        pdf_exporter = nbconvert.PDFExporter()
        pdf_exporter.exclude_input = True
        pdf_exporter.exclude_output_prompt = True
        pdf, resources = pdf_exporter.from_file(uploaded_file)

        # Save the PDF to a file
        with open("notebook.pdf", "wb") as f:
            f.write(pdf)

        # Show the generated PDF
        st.success("Notebook converted to PDF!")
        st.markdown("The generated PDF is attached below")
        st.pdf("notebook.pdf")


def main():
    st.set_page_config(page_title="Jupyter Notebook to PDF Converter", page_icon=":guardsman:", layout="wide")
    st.title("Jupyter Notebook to PDF Converter")

    st.markdown("This app allows you to upload a Jupyter notebook and convert it to a PDF.")

    convert_notebook()


if __name__ == "__main__":
    main()
