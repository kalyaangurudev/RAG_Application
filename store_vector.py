from embedding import get_embeddings
from langchain_chroma import Chroma
from langchain. schema. document import Document

CHROMA_PATH = "/Users/tejassaiprashad/Documents/my_workspace/RAG_Application/RAG_Application/chroma_directory"

def add_to_chroma(chunks: list[Document]):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embeddings())
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Filter out already existing documents
    new_chunks = [chunk for chunk in chunks if chunk.metadata["id"] not in existing_ids]

    if not new_chunks:
        print("No new chunks to add.")
        return

    new_chunks_ids = [chunk.metadata["id"] for chunk in new_chunks]
    db.add_documents(new_chunks, ids=new_chunks_ids)
    print(f"Added {len(new_chunks)} new chunks.")
