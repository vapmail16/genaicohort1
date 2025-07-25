# Simple RAG Application - Code Guide

This guide explains the structure and functionality of the Simple RAG (Retrieval-Augmented Generation) application. Read the files in the order listed below to understand how the system works.

## 📁 Project Overview

This is a complete RAG system that:
1. **Ingests PDF documents** and converts them to searchable chunks
2. **Stores embeddings** in a Qdrant vector database
3. **Provides semantic search** capabilities
4. **Generates answers** using an LLM (GPT-3.5-turbo)
5. **Offers a web interface** for querying documents

## 📖 Reading Order & File Descriptions

### 1. **README.md** - Start Here
**Purpose**: Project overview and setup instructions
**Key Components**:
- Project description and features
- Setup instructions for dependencies
- How to start Qdrant database
- Environment variable configuration
- Basic usage instructions

**What to understand**: The overall system architecture and how to get it running.

---

### 2. **config.py** - Configuration Management
**Purpose**: Central configuration for all system components
**Key Components**:
- **Qdrant Configuration**: Database connection settings (host, port, API key)
- **Embedding Configuration**: Which embedding model to use (`all-MiniLM-L6-v2`)
- **API Configuration**: Server settings (host, port)
- **Document Processing**: Chunk size and overlap settings
- **Cloud vs Local Detection**: Automatically detects if using Qdrant Cloud

**What to understand**: How the system is configured and what parameters control its behavior.

---

### 3. **vector_store.py** - Core Vector Database Operations
**Purpose**: Handles all interactions with the Qdrant vector database
**Key Components**:

#### **VectorStore Class**:
- **`__init__()`**: Initializes Qdrant client and embedding model
- **`_ensure_collection_exists()`**: Creates the vector collection if it doesn't exist
- **`add_documents()`**: Converts text to embeddings and stores them
- **`search()`**: Performs semantic search using query embeddings
- **`delete_collection()`**: Removes the entire collection
- **`get_collection_info()`**: Returns collection statistics

#### **Key Concepts**:
- Uses `sentence-transformers` for creating embeddings
- Stores documents as "points" in Qdrant with metadata
- Performs cosine similarity search
- Handles both cloud and local Qdrant deployments

**What to understand**: How documents are stored as vectors and how semantic search works.

---

### 4. **ingestion_service.py** - Document Processing Pipeline
**Purpose**: Converts PDF documents into searchable chunks in the vector database
**Key Components**:

#### **Main Functions**:
- **`load_pdfs_from_directory()`**: Extracts text from all PDFs in the data directory
- **`chunk_documents()`**: Splits large documents into smaller, overlapping chunks
- **`main()`**: Orchestrates the entire ingestion process

#### **Processing Flow**:
1. Load PDFs from `data/` directory
2. Extract text from each PDF
3. Split text into chunks using `RecursiveCharacterTextSplitter`
4. Convert chunks to embeddings and store in Qdrant

**What to understand**: How raw documents become searchable vector embeddings.

---

### 5. **app.py** - Web Interface (Streamlit)
**Purpose**: Provides a user-friendly web interface for querying documents
**Key Components**:

#### **Main Features**:
- **Question Input**: Text field for user queries
- **Parameter Controls**: Sliders for score threshold and number of chunks
- **Search Results**: Displays retrieved chunks with similarity scores
- **LLM Integration**: Uses OpenAI GPT-3.5-turbo to generate answers
- **Context Display**: Shows the chunks used to generate the answer

#### **Workflow**:
1. User enters a question
2. System searches for relevant chunks
3. Displays retrieved chunks with scores
4. Sends chunks + question to LLM
5. Displays generated answer

**What to understand**: How users interact with the RAG system and how answers are generated.

---

### 6. **evaluate_rag.py** - System Evaluation
**Purpose**: Evaluates the performance of the RAG system
**Key Components**:

#### **RAGEvaluator Class**:
- **`retrieve_chunks()`**: Gets relevant chunks for a query
- **`generate_answer()`**: Creates answers using retrieved chunks
- **`calculate_similarity_score()`**: Measures text similarity using Jaccard index
- **`evaluate_rag_performance()`**: Runs comprehensive evaluation tests
- **`calculate_overall_metrics()`**: Computes aggregate performance metrics

#### **Evaluation Metrics**:
- **Retrieval Metrics**: Keyword recall, precision, chunk relevance
- **Answer Quality**: Answer similarity, length
- **Performance Analysis**: Detailed breakdown of each test case

#### **Test Questions**: Pre-defined questions about GDPR/Board documents

**What to understand**: How to measure and improve RAG system performance.

---

### 7. **Utility Files** - Debugging and Inspection

#### **test_connection.py**
**Purpose**: Verifies Qdrant database connection
**Use**: Run this first to ensure your database is accessible

#### **inspect_chunk.py**
**Purpose**: Debug tool to find and examine specific chunks
**Use**: Enter text to find the most similar chunk and see its vector

#### **print_all_chunks.py**
**Purpose**: Inspect chunks and their vector representations
**Use**: View sample chunks and their embedding vectors

---

### 8. **requirements.txt** - Dependencies
**Purpose**: Lists all Python packages needed
**Key Dependencies**:
- `qdrant-client`: Vector database client
- `sentence-transformers`: Embedding generation
- `langchain`: Text chunking utilities
- `pypdf`: PDF text extraction
- `streamlit`: Web interface
- `openai`: LLM integration

---

### 9. **data/** - Document Storage
**Purpose**: Contains PDF documents to be processed
**Current Documents**:
- `CELEX_32016R0679_EN_TXT.pdf`: GDPR regulation document
- `Reviewer List for Voices 09Jan2025 copy 2.pdf`: Review document

---

## 🔄 System Workflow

### **Setup Phase**:
1. Install dependencies (`pip install -r requirements.txt`)
2. Start Qdrant database (Docker or local)
3. Configure environment variables
4. Test connection (`python test_connection.py`)

### **Ingestion Phase**:
1. Place PDFs in `data/` directory
2. Run ingestion service (`python ingestion_service.py`)
3. Documents are chunked and stored as vectors

### **Query Phase**:
1. Start web interface (`streamlit run app.py`)
2. Enter questions in the web interface
3. System retrieves relevant chunks
4. LLM generates answers based on retrieved context

### **Evaluation Phase**:
1. Run evaluation (`python evaluate_rag.py`)
2. Review performance metrics
3. Adjust parameters based on results

## 🎯 Key Concepts to Understand

1. **Vector Embeddings**: How text becomes numerical representations
2. **Semantic Search**: Finding similar meaning, not just exact matches
3. **Chunking Strategy**: Breaking documents into searchable pieces
4. **RAG Pipeline**: Retrieve → Augment → Generate workflow
5. **Similarity Scoring**: How relevance is measured
6. **Context Window**: How much information is sent to the LLM

## 🛠️ Customization Points

- **Embedding Model**: Change in `config.py` (EMBEDDING_MODEL)
- **Chunk Size**: Adjust in `config.py` (CHUNK_SIZE, CHUNK_OVERLAP)
- **LLM Model**: Modify in `app.py` and `evaluate_rag.py`
- **Search Parameters**: Adjust score threshold and top-k in the interface
- **Evaluation Questions**: Add custom test cases in `evaluate_rag.py`

This system demonstrates a complete RAG implementation from document ingestion to answer generation, with evaluation capabilities for continuous improvement. 