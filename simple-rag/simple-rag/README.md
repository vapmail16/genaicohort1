# Simple RAG Application

A simple Retrieval-Augmented Generation (RAG) application using Qdrant vector database.

## Features

- Document ingestion and vectorization
- Semantic search capabilities
- RESTful API for querying
- Support for PDF documents

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Qdrant Vector Database
```bash
# Using Docker (recommended)
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

# Or using pip
pip install qdrant
qdrant
```

### 3. Set Environment Variables
Create a `.env` file:
```bash
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=documents
```

### 4. Run the Application
```bash
# Start the ingestion service
python ingestion_service.py

# Start the API server
python api_server.py
```

## Project Structure

- `ingestion_service.py` - Document ingestion and vectorization
- `api_server.py` - FastAPI server for querying
- `vector_store.py` - Qdrant vector store operations
- `data/` - Directory for documents to ingest
- `qdrant_storage/` - Qdrant database storage

## Usage

1. Place your documents in the `data/` directory
2. Run the ingestion service to vectorize documents
3. Use the API to query your documents 