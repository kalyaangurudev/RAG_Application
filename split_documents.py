from langchain.text_splitter import MarkdownTextSplitter
from langchain.schema.document import Document 

def pdf_splitter(docs: list[Document]):
    # Split the text into chunks
    splitter = MarkdownTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    all_chunks = []
    for doc in docs:
        chunks = splitter.split_text(doc.page_content)
        for chunk in chunks:
            all_chunks.append(Document(page_content=chunk, metadata=doc.metadata)) 

    return all_chunks
