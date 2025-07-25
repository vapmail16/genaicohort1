# 🚀 GenAI Cohort 1 - AI Projects Collection

A comprehensive collection of AI-powered applications and tools demonstrating various aspects of modern AI development, from conversational agents to document processing and project scaffolding.

## 📋 Table of Contents

- [Overview](#overview)
- [Projects](#projects)
  - [🤖 Simple Chatbot](#-simple-chatbot)
  - [📚 Simple RAG](#-simple-rag)
  - [🤖 Simple Agent](#-simple-agent)
  - [🏗️ Project Scaffold](#️-project-scaffold)
- [Quick Start](#quick-start)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains four distinct AI projects that showcase different aspects of modern AI development:

1. **Simple Chatbot** - A feature-rich conversational AI with multiple personalities
2. **Simple RAG** - A Retrieval-Augmented Generation system for document processing with Docker support
3. **Simple Agent** - A multi-agent stock analysis system with AI collaboration
4. **Project Scaffold** - A comprehensive project template with diagnostics and monitoring

Each project is self-contained with its own dependencies, configuration, and documentation.

## 🛠️ Projects

### 🤖 Simple Chatbot

**Location**: `simple-chatbot/`

A comprehensive, feature-rich chatbot application built with Streamlit and OpenAI GPT. This chatbot includes multiple personalities, memory management, feedback system, and analytics.

#### ✨ Key Features
- **Multiple Personalities**: Choose from 4 different assistant personalities (Friendly, Professional, Funny, Creative)
- **Memory Management**: Maintains conversation history and context
- **Real-time Analytics**: Track interactions, personality usage, and feedback
- **Export Capabilities**: Download chat history as CSV or JSON
- **Modern UI**: Beautiful, responsive interface with custom styling
- **Error Handling**: Robust error handling for API timeouts and rate limits

#### 🚀 Quick Start
```bash
cd simple-chatbot
pip install -r requirements.txt
# Set up your .env file with OPENAI_API_KEY
streamlit run app.py
```

#### 📁 Structure
```
simple-chatbot/
├── app.py                 # Main Streamlit application
├── chatbot_core.py        # Core chatbot functionality
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
├── README.md            # Detailed documentation
├── chat_history.csv     # Generated chat logs
└── chatbot.log          # Application logs
```

---

### 📚 Simple RAG

**Location**: `simple-rag/`

A Retrieval-Augmented Generation (RAG) application using Qdrant vector database with comprehensive Docker support for easy deployment and management.

#### ✨ Key Features
- **Document Ingestion**: Process and vectorize PDF documents
- **Semantic Search**: Advanced search capabilities using vector embeddings
- **Streamlit Web Interface**: User-friendly web interface for RAG queries
- **Vector Database**: Qdrant-based storage for efficient retrieval
- **Docker Support**: Complete containerization with organized structure
- **Evaluation Tools**: Built-in RAG performance evaluation
- **OpenAI Integration**: LLM-powered responses with context

#### 🚀 Quick Start with Docker (Recommended)
```bash
cd simple-rag

# 1. Set up environment variables
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 2. Add PDF documents to data/ directory
mkdir -p data
cp your_documents.pdf data/

# 3. Start with Docker
./docker-run.sh start

# 4. Access the application
# Streamlit App: http://localhost:8501
# Qdrant Dashboard: http://localhost:6333/dashboard
```

#### 🚀 Manual Setup (Alternative)
```bash
cd simple-rag
pip install -r requirements.txt

# Start Qdrant (Docker recommended)
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

# Run the application
streamlit run app.py
```

#### 📁 Structure
```
simple-rag/
├── app.py                 # Streamlit web interface
├── ingestion_service.py   # Document ingestion and vectorization
├── vector_store.py        # Qdrant vector store operations
├── evaluate_rag.py        # RAG performance evaluation
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── data/                 # Directory for documents to ingest
├── docker/               # All Docker-related files
│   ├── Dockerfile        # Container configuration
│   ├── docker-compose.yml # Multi-container orchestration
│   ├── DOCKER_GUIDE.md   # Comprehensive Docker documentation
│   └── ...               # Other Docker files
├── docker-run.sh         # Easy Docker runner script
├── Makefile              # Docker commands
└── README.md            # Detailed documentation
```

---

### 🤖 Simple Agent

**Location**: `simple-agent/`

A sophisticated multi-agent stock analysis system that demonstrates AI collaboration for financial analysis. This application uses multiple specialized AI agents working together to provide comprehensive stock market insights and recommendations.

#### ✨ Key Features
- **Multi-Agent Architecture**: 4 specialized AI agents collaborating on analysis
- **Real-time Stock Data**: Live financial data from Yahoo Finance
- **News Sentiment Analysis**: AI-powered sentiment analysis of market news
- **Risk Assessment**: Comprehensive risk evaluation and scoring
- **Interactive Web Interface**: Beautiful Streamlit-based dashboard
- **Human-in-the-Loop**: Approval system for AI recommendations
- **Comprehensive Testing**: 34+ tests ensuring reliability

#### 🚀 Quick Start
```bash
cd simple-agent
pip install -r requirements.txt

# Set up environment variables (optional for testing)
cp .env.example .env
# Add your OPENAI_API_KEY and NEWS_API_KEY

# Launch the application
./start_app.sh
# Or manually: streamlit run streamlit_app.py
```

#### 📁 Structure
```
simple-agent/
├── streamlit_app.py          # Main web application
├── demo_visual_interface.py  # Visual interface demo
├── run_app.py               # Application runner
├── start_app.sh             # Startup script
├── requirements.txt         # Python dependencies
├── src/                     # Source code
│   ├── agents/              # AI agent implementations
│   ├── tools/               # Stock analysis tools
│   ├── multi_agents/        # Multi-agent coordination
│   ├── ui/                  # User interface components
│   └── utils/               # Utility functions
├── tests/                   # Test suite
├── README.md               # Detailed documentation
├── LAUNCH_INSTRUCTIONS.md  # Launch guide
└── VISUAL_INTERFACE_README.md # UI documentation
```

#### 🎯 Agent Roles
1. **📊 Stock Fetcher**: Retrieves financial data and metrics
2. **📰 News Analyst**: Analyzes market sentiment from news
3. **⚖️ Risk Assessor**: Evaluates investment risks
4. **📋 Report Generator**: Creates comprehensive recommendations

---

### 🏗️ Project Scaffold

**Location**: `project-scaffold/`

A comprehensive project template that provides a solid foundation for AI/ML projects with built-in diagnostics, monitoring, and best practices.

#### ✨ Key Features
- **Project Structure**: Well-organized directory structure
- **Configuration Management**: Environment-based configuration
- **Logging & Monitoring**: Comprehensive logging and monitoring setup
- **Testing Framework**: Built-in testing infrastructure
- **Documentation**: Auto-generated documentation
- **CI/CD Ready**: GitHub Actions and deployment scripts
- **Docker Support**: Containerization for easy deployment

#### 🚀 Quick Start
```bash
cd project-scaffold
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Configure your environment variables

# Run the application
python main.py
```

#### 📁 Structure
```
project-scaffold/
├── main.py                 # Main application entry point
├── config/                 # Configuration files
├── src/                    # Source code
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── requirements.txt        # Python dependencies
└── README.md              # Detailed documentation
```

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vapmail16/genaicohort1.git
   cd genaicohort1
   ```

2. **Choose a project**:
   - For chatbot: `cd simple-chatbot`
   - For RAG system: `cd simple-rag`
   - For stock analysis: `cd simple-agent`
   - For project template: `cd project-scaffold`

3. **Follow the project-specific setup instructions** in each project's README.md

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **OpenAI GPT**: Large language models
- **Qdrant**: Vector database for RAG
- **Docker**: Containerization
- **FastAPI**: REST API framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning utilities

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
