import os
import logging
from typing import List, Dict, Any
from pypdf import PdfReader
from vector_store_simple import SimpleVectorStore
from simple_text_cleaner import create_simple_text_cleaner
from config import CHUNK_SIZE, CHUNK_OVERLAP, REMOVE_STOPWORDS, REMOVE_NUMBERS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_pdf(file_path: str) -> str:
    """Read text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    if not text.strip():
        return []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If this is not the first chunk, include some overlap
        if start > 0:
            start = start - chunk_overlap
        
        # Extract the chunk
        chunk = text[start:end].strip()
        
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        start = end
    
    return chunks

def process_documents(data_dir: str = "data") -> List[Dict[str, Any]]:
    """Process all PDF documents in the data directory."""
    documents = []
    
    if not os.path.exists(data_dir):
        logger.error(f"Data directory {data_dir} does not exist")
        return documents
    
    # Get text cleaner
    text_cleaner = create_simple_text_cleaner(remove_numbers=REMOVE_NUMBERS)
    
    # Process each PDF file
    for filename in os.listdir(data_dir):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(data_dir, filename)
            logger.info(f"Processing {filename}")
            
            # Read PDF
            raw_text = read_pdf(file_path)
            if not raw_text:
                logger.warning(f"No text extracted from {filename}")
                continue
            
            # Clean text
            cleaned_text = text_cleaner.clean_text(raw_text, remove_stopwords=REMOVE_STOPWORDS)
            
            # Split into chunks
            chunks = chunk_text(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)
            
            # Create documents
            for i, chunk in enumerate(chunks):
                document = {
                    'text': chunk,
                    'metadata': {
                        'source': filename,
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    },
                    'source': filename
                }
                documents.append(document)
            
            logger.info(f"Created {len(chunks)} chunks from {filename}")
    
    return documents

def main():
    """Main function to ingest documents into the vector store."""
    try:
        # Initialize vector store
        vector_store = SimpleVectorStore()
        
        # Process documents
        documents = process_documents()
        
        if not documents:
            logger.warning("No documents found to process")
            return
        
        # Add documents to vector store
        doc_ids = vector_store.add_documents(documents)
        
        logger.info(f"Successfully ingested {len(documents)} document chunks")
        logger.info(f"Document IDs: {doc_ids[:5]}...")  # Show first 5 IDs
        
        # Get collection info (handle errors gracefully)
        try:
            info = vector_store.get_collection_info()
            logger.info(f"Collection info: {info}")
        except Exception as e:
            logger.warning(f"Could not retrieve collection info: {e}")
            logger.info("Ingestion completed successfully despite collection info error")
        
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise

if __name__ == "__main__":
    main() 