# Simple RAG Application

A simple Retrieval-Augmented Generation (RAG) application using Qdrant vector database with Docker support.

## Features

- Document ingestion and vectorization
- Semantic search capabilities
- Streamlit web interface for querying
- Support for PDF documents
- Docker containerization for easy deployment
- OpenAI integration for LLM-powered responses

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd simple-rag
```

### 2. Set Environment Variables
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Add Documents
Place your PDF documents in the `data/` directory:
```bash
mkdir -p data
cp your_documents.pdf data/
```

### 4. Run with Docker Compose
```bash
# Using Makefile (recommended)
make start

# Or directly with docker-compose
docker-compose -f docker/docker-compose.yml up -d
```

### 5. Access the Application
- **Streamlit App**: http://localhost:8501
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## Manual Setup (Alternative)

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
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application
```bash
# Start the Streamlit app
streamlit run app.py
```

## Project Structure

- `app.py` - Streamlit web interface for RAG queries
- `ingestion_service.py` - Document ingestion and vectorization
- `vector_store.py` - Qdrant vector store operations
- `config.py` - Configuration management
- `data/` - Directory for documents to ingest
- `qdrant_storage/` - Qdrant database storage
- `docker/` - All Docker-related files
  - `Dockerfile` - Docker container configuration
  - `docker-compose.yml` - Multi-container orchestration
  - `DOCKER_GUIDE.md` - Comprehensive Docker documentation
  - `test-docker.sh` - Docker testing script
  - `verify-docker-setup.sh` - Setup verification script
- `Makefile` - Easy Docker commands

## Usage

1. Place your documents in the `data/` directory
2. Run the ingestion service to vectorize documents
3. Use the Streamlit interface to query your documents
4. The app will retrieve relevant chunks and generate LLM-powered answers

## Docker Documentation

For detailed Docker setup, troubleshooting, and production deployment instructions, see [docker/DOCKER_GUIDE.md](docker/DOCKER_GUIDE.md). 