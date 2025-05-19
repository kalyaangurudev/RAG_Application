from langchain_community.document_loaders import PDFPlumberLoader

def pdfLoader(pdf_path):
    # Load the PDF file
    loader = PDFPlumberLoader(pdf_path)
    docs = loader.load()

    return docs
