from embedding import get_embeddings
from langchain_chroma import Chroma
from langchain.schema.document import Document
from langchain.prompts import ChatPromptTemplate
from pdf_fetcher import pdfLoader
from split_documents import pdf_splitter
from store_vector import add_to_chroma
from langchain_ollama import OllamaLLM

# Load and split documents
documents = pdfLoader("/Users/tejassaiprashad/Desktop/blackjack.pdf")
chunks = pdf_splitter(documents)

# Process chunks and assign unique IDs
last_page_id = None
current_chunk_index = 0
for chunk in chunks:
    source = chunk.metadata.get("source")
    page = chunk.metadata.get("page")
    current_page_id = f"{source}:{page}"
    
    if current_page_id == last_page_id:
        current_chunk_index += 1
    else:
        current_chunk_index = 0
        last_page_id = current_page_id  # Bug fix: update last_page_id
        
    chunk.metadata["id"] = f"{source}:{page}:{current_chunk_index}"

# Add all processed chunks to Chroma
add_to_chroma(chunks)

# Constants
CHROMA_PATH = "/Users/tejassaiprashad/Documents/my_workspace/RAG_Application/RAG_Application/chroma_directory"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
Answer the question based on the above context: {question}
"""

# Query function
def get_query(query_text:str):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embeddings())
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    return prompt

# Example query
prompt = get_query("What are the payouts and odds of the game?")

model = OllamaLLM(
    model="mistral",
    base_url="http://localhost:11434",
    temperature=0.5
)
response_text = model. invoke(prompt)
print (response_text)