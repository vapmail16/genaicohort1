# 🚀 Simple RAG Application - Clean & Organized

A professional Retrieval-Augmented Generation (RAG) application with comprehensive Docker support and clean, organized project structure.

## 📁 Clean Project Structure

```
simple-rag/
├── run.sh                        # 🚀 Main runner script
├── requirements.txt              # 📦 Python dependencies
├── .env                          # 🔐 Environment variables
├── .gitignore                    # 🚫 Git ignore rules
├── data/                         # 📄 PDF documents directory
│
├── src/                          # 🔧 Main application source
│   ├── app.py                    # 🌐 Streamlit web interface
│   ├── config.py                 # ⚙️ Configuration management
│   ├── ingestion_service.py      # 📥 Document processing
│   └── vector_store.py           # 🗄️ Vector database operations
│
├── docker/                       # 🐳 Docker configuration
│   ├── Dockerfile                # 📦 Container configuration
│   ├── docker-compose.yml        # 🎯 Multi-container setup
│   ├── docker-compose.dev.yml    # 🔧 Development mode
│   ├── docker-compose.prod.yml   # 🚀 Production mode
│   ├── docker-ingest.py          # 📥 Document ingestion script
│   ├── test-docker.sh            # 🧪 Docker testing
│   ├── verify-docker-setup.sh    # ✅ Setup verification
│   └── [Docker documentation]    # 📚 Docker guides
│
├── docs/                         # 📚 Documentation
│   ├── README.md                 # 📖 Main documentation (this file)
│   ├── DOCKER_ORGANIZATION.md    # 🗂️ Organization guide
│   ├── GITHUB_UPLOAD_GUIDE.md    # 📤 Upload instructions
│   └── FINAL_SUMMARY.md          # 📋 Project summary
│
├── scripts/                      # 🛠️ Utility scripts
│   ├── docker-run.sh             # 🐳 Docker management
│   └── Makefile                  # 🔨 Make commands
│
├── examples/                     # 📖 Example implementations
│   ├── app_*.py                  # 🌐 Application examples
│   ├── hybrid_*.py               # 🔍 Hybrid search examples
│   ├── vector_store_*.py         # 🗄️ Vector store examples
│   ├── text_cleaner.py           # 🧹 Text processing
│   └── [other examples]          # 🔧 Various utilities
│
└── tests/                        # 🧪 Test files
    ├── test_*.py                 # 🔍 Test files
    ├── debug_*.py                # 🐛 Debug files
    └── simple_test.py            # 🧪 Simple tests
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### 1. Setup Environment
```bash
# Create environment file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Add PDF documents
mkdir -p data
cp your_documents.pdf data/
```

### 2. Start Application
```bash
# Start everything with one command
./run.sh docker start

# Check status
./run.sh docker status

# View logs
./run.sh docker logs
```

### 3. Access Application
- **Streamlit App**: http://localhost:8501
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## 🎯 Easy Commands

### Docker Management
```bash
./run.sh docker start      # Start all services
./run.sh docker status     # Check service status
./run.sh docker logs       # View logs
./run.sh docker down       # Stop all services
./run.sh docker restart    # Restart services
./run.sh docker clean      # Clean up everything
./run.sh docker ingest     # Run document ingestion
./run.sh docker shell      # Open container shell
./run.sh docker verify     # Verify setup
```

### Development
```bash
./run.sh dev start         # Start in development mode
./run.sh dev shell         # Open development shell
```

### Documentation & Examples
```bash
./run.sh docs              # View documentation
./run.sh examples          # List examples
./run.sh tests             # Run tests
./run.sh structure         # Show project structure
```

## 🔧 Features

### 🐳 Docker Features
- **Multi-container orchestration** with docker-compose
- **Qdrant vector database** container
- **Streamlit web interface** container
- **Volume persistence** for data and storage
- **Environment variable management**
- **Health checks** for all services
- **Development and production** configurations
- **Automated document ingestion**
- **Network isolation** between services

### 🔍 RAG Features
- **Document ingestion** from PDF files
- **Vector embedding** with sentence-transformers
- **Semantic search** capabilities
- **OpenAI integration** for LLM responses
- **Streamlit web interface** for user interaction
- **Qdrant vector database** for efficient storage
- **Configuration management** with environment variables

### 📚 Documentation Features
- **Comprehensive guides** for all skill levels
- **Step-by-step tutorials** for beginners
- **Troubleshooting guides** for common issues
- **Setup verification** scripts
- **Organization documentation** explaining the structure
- **GitHub upload guide** for repository management

## 🎯 Benefits of Clean Organization

### ✅ Professional Structure
- **Clear separation** of concerns
- **Logical grouping** of related files
- **Easy navigation** and maintenance
- **Scalable architecture** for future growth

### ✅ Developer Experience
- **Intuitive file locations**
- **Consistent naming conventions**
- **Easy to find** specific functionality
- **Reduced cognitive load**

### ✅ User Experience
- **Simple commands** for all operations
- **Clear documentation** for every aspect
- **Multiple access methods** (script, Makefile, direct)
- **Beginner-friendly** guides and examples

## 📖 Documentation

### Main Documentation
- `docs/README.md` - Main project documentation (this file)
- `docs/DOCKER_ORGANIZATION.md` - Docker organization guide
- `docs/GITHUB_UPLOAD_GUIDE.md` - GitHub upload instructions
- `docs/FINAL_SUMMARY.md` - Project summary

### Docker Documentation
- `docker/DOCKER_GUIDE.md` - Comprehensive Docker guide
- `docker/DOCKER_FOR_BEGINNERS.md` - Beginner-friendly guide
- `docker/DOCKER_SETUP_CHECKLIST.md` - Setup verification
- `docker/WHAT_YOU_NEED_TO_PROVIDE.md` - Requirements guide

## 🧪 Examples & Tests

### Examples (`examples/`)
- **Application examples**: `app_simple.py`, `app_hybrid.py`
- **Search implementations**: `hybrid_search.py`, `vector_store_simple.py`
- **Text processing**: `text_cleaner.py`, `simple_text_cleaner.py`
- **Evaluation tools**: `evaluate_rag.py`, `inspect_chunk.py`

### Tests (`tests/`)
- **Connection tests**: `test_connection.py`
- **LLM integration**: `test_llm.py`
- **Debug tools**: `debug_search.py`
- **Simple tests**: `simple_test.py`

## 🚀 Deployment

### Local Development
```bash
./run.sh docker start
# Access at http://localhost:8501
```

### Production Deployment
```bash
./run.sh dev start
# Uses production configuration with resource limits
```

### GitHub Upload
Follow the `docs/GITHUB_UPLOAD_GUIDE.md` for complete instructions.

## 🎉 Success Indicators

You'll know everything is working when:
1. ✅ `./run.sh docker verify` passes all checks
2. ✅ `./run.sh docker start` starts all services
3. ✅ Streamlit app loads at http://localhost:8501
4. ✅ Qdrant dashboard accessible at http://localhost:6333/dashboard
5. ✅ Document ingestion works with `./run.sh docker ingest`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- Streamlit for the web framework
- Qdrant for the vector database
- The AI community for inspiration and support

---

## 🏆 Why This Organization?

This clean, organized structure provides:

- **🎯 Clear Purpose**: Each directory has a specific role
- **🔍 Easy Navigation**: Find what you need quickly
- **📈 Scalability**: Easy to add new features and components
- **👥 Team Collaboration**: Clear structure for multiple developers
- **📚 Learning**: Examples and documentation in logical places
- **🚀 Deployment**: Production-ready organization

**Your RAG application is now professionally organized and ready for the world!** 🌟
