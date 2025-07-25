#!/usr/bin/env python3
"""
Document ingestion script for Docker environment.
This script helps ingest documents into the vector database when running in Docker.
"""

import os
import sys
from pathlib import Path
import sys
import os
sys.path.append('/app/src')

from ingestion_service import load_pdfs_from_directory, chunk_documents
from vector_store import VectorStore
from config import CHUNK_SIZE, CHUNK_OVERLAP

def main():
    """Main function to ingest documents in Docker environment."""
    
    # Get data directory from environment or use default
    data_dir = os.getenv('DATA_DIR', '/app/data')
    data_path = Path(data_dir)
    
    print(f"🔍 Looking for documents in: {data_path}")
    
    # Check if data directory exists
    if not data_path.exists():
        print(f"❌ Data directory {data_path} does not exist!")
        print("Please mount your documents directory to /app/data")
        sys.exit(1)
    
    # Find PDF files
    pdf_files = list(data_path.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in data directory!")
        print(f"Please add PDF files to: {data_path}")
        sys.exit(1)
    
    print(f"📄 Found {len(pdf_files)} PDF file(s):")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # Ingest documents
    print("\n🚀 Starting document ingestion...")
    try:
        # Load PDFs
        print("Loading PDFs...")
        docs = load_pdfs_from_directory(str(data_path))
        
        if not docs:
            print("❌ No PDF files could be processed!")
            sys.exit(1)
        
        print(f"Loaded {len(docs)} PDF(s). Chunking text...")
        
        # Chunk documents
        chunked_docs = chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
        print(f"Created {len(chunked_docs)} text chunks.")
        
        # Ingest into vector store
        print("Ingesting into Qdrant...")
        vs = VectorStore()
        ids = vs.add_documents(chunked_docs)
        
        print(f"✅ Successfully ingested {len(ids)} chunks into Qdrant collection '{vs.collection_name}'!")
        print("\n🎉 You can now use the Streamlit app to query your documents!")
        print("   Access the app at: http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 