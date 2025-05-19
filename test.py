from pdf_fetcher import pdfLoader
from split_documents import pdf_splitter

documents = pdfLoader("/Users/tejassaiprashad/Desktop/blackjack.pdf")
print (documents[0])
chunks = pdf_splitter (documents)
# print ( chunks [0])

last_page_id = None
current_chunk_index = 0
for chunk in chunks:
    source = chunk. metadata. get ("source")
    page = chunk. metadata. get ("page" )
    current_page_id = f"{source}: {page}"

    if current_page_id == last_page_id:
            current_chunk_index += 1
    else:
        current_chunk_index = 0

    chunk.metadata["id"] = current_chunk_index