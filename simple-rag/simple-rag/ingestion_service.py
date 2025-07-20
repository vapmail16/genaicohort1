import os
from typing import List, Dict
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vector_store import VectorStore
from simple_text_cleaner import create_simple_text_cleaner
from config import CHUNK_SIZE, CHUNK_OVERLAP, REMOVE_STOPWORDS, REMOVE_NUMBERS

DATA_DIR = "data"


def load_pdfs_from_directory(directory: str) -> List[Dict]:
    """Load and extract text from all PDF files in the directory."""
    documents = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {filename}")
            try:
                reader = PdfReader(file_path)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                documents.append({
                    "text": text,
                    "metadata": {"source": filename}
                })
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return documents


def chunk_documents(documents: List[Dict], chunk_size: int, chunk_overlap: int) -> List[Dict]:
    """Chunk documents into smaller pieces for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunked = []
    for doc in documents:
        for chunk in splitter.split_text(doc["text"]):
            chunked.append({
                "text": chunk,
                "metadata": doc["metadata"]
            })
    return chunked


def main():
    print("Loading PDFs from data/ directory...")
    docs = load_pdfs_from_directory(DATA_DIR)
    if not docs:
        print("No PDF files found in data/ directory.")
        return
    
    # Initialize text cleaner
    print("Initializing text cleaner...")
    cleaner = create_simple_text_cleaner(remove_numbers=REMOVE_NUMBERS)
    
    # Clean the documents
    print("Cleaning documents...")
    cleaned_docs = cleaner.clean_documents(docs, remove_stopwords=REMOVE_STOPWORDS)
    print(f"Cleaned {len(cleaned_docs)} documents.")
    
    print("Chunking text...")
    chunked_docs = chunk_documents(cleaned_docs, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Created {len(chunked_docs)} text chunks. Ingesting into Qdrant...")
    vs = VectorStore()
    ids = vs.add_documents(chunked_docs)
    print(f"Ingested {len(ids)} chunks into Qdrant collection '{vs.collection_name}'.")


if __name__ == "__main__":
    main() 