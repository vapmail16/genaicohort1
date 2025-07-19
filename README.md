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
2. **Simple RAG** - A Retrieval-Augmented Generation system for document processing
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

A Retrieval-Augmented Generation (RAG) application using Qdrant vector database for intelligent document processing and querying.

#### ✨ Key Features
- **Document Ingestion**: Process and vectorize PDF documents
- **Semantic Search**: Advanced search capabilities using vector embeddings
- **RESTful API**: FastAPI-based query interface
- **Vector Database**: Qdrant-based storage for efficient retrieval
- **Evaluation Tools**: Built-in RAG performance evaluation

#### 🚀 Quick Start
```bash
cd simple-rag
pip install -r requirements.txt

# Start Qdrant (Docker recommended)
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

# Run the application
python ingestion_service.py
python app.py
```

#### 📁 Structure
```
simple-rag/
├── app.py                 # FastAPI server for querying
├── ingestion_service.py   # Document ingestion and vectorization
├── vector_store.py        # Qdrant vector store operations
├── evaluate_rag.py        # RAG performance evaluation
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── data/                 # Directory for documents to ingest
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

**Location**: `project_scaffold/`

A comprehensive Python project template with built-in diagnostics, database connectivity checks, API monitoring, and Docker status verification.

#### ✨ Key Features
- **System Diagnostics**: Comprehensive health checks for your development environment
- **Database Connectivity**: Test connections to various database systems
- **API Monitoring**: Check status of external APIs (OpenAI, GitHub)
- **Docker Integration**: Verify Docker daemon status and container health
- **Environment Validation**: Validate required environment variables
- **Poetry Integration**: Modern Python dependency management

#### 🚀 Quick Start
```bash
cd project_scaffold/my_project
poetry install
cp .env.example .env
# Update .env with your OPENAI_API_KEY
poetry run python diagnostics.py
```

#### 📁 Structure
```
project_scaffold/
└── my_project/
    ├── diagnostics.py     # Comprehensive health check script
    ├── pyproject.toml     # Poetry configuration
    ├── makefile          # Development commands
    ├── Dockerfile        # Container configuration
    ├── src/              # Source code
    ├── tests/            # Test cases
    ├── configs/          # Configuration files
    ├── scripts/          # Utility scripts
    ├── docs/             # Documentation
    └── README.md         # Detailed documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Docker (for Simple RAG)
- OpenAI API key (for Simple Chatbot, Simple Agent, and Project Scaffold)
- News API key (optional, for Simple Agent)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vapmail16/genaicohort1.git
   cd genaicohort1
   ```

2. **Choose a project to run**
   Each project is self-contained. Navigate to the project directory and follow its specific setup instructions.

### Environment Setup

Create environment files for projects that need them:

**Simple Chatbot** (`simple-chatbot/.env`):
```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7
```

**Simple RAG** (`simple-rag/.env`):
```env
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=documents
```

**Project Scaffold** (`project_scaffold/my_project/.env`):
```env
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=true
DATABASE_URL=your_database_url
```

**Simple Agent** (`simple-agent/.env`):
```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **Streamlit** - Web application framework (Simple Chatbot, Simple Agent)
- **FastAPI** - REST API framework (Simple RAG)
- **OpenAI GPT** - Large Language Model integration
- **Qdrant** - Vector database (Simple RAG)
- **LangChain** - AI agent framework (Simple Agent)
- **CrewAI** - Multi-agent orchestration (Simple Agent)
- **Poetry** - Dependency management (Project Scaffold)

### Key Libraries
- **pandas** - Data manipulation and analysis
- **requests** - HTTP client library
- **python-dotenv** - Environment variable management
- **streamlit** - Web app framework
- **fastapi** - API framework
- **qdrant-client** - Vector database client
- **pypdf** - PDF processing
- **sentence-transformers** - Text embeddings
- **langchain** - AI agent framework
- **crewai** - Multi-agent orchestration
- **yfinance** - Stock market data
- **plotly** - Interactive visualizations

## 📊 Project Comparison

| Feature | Simple Chatbot | Simple RAG | Simple Agent | Project Scaffold |
|---------|----------------|------------|--------------|------------------|
| **Primary Purpose** | Conversational AI | Document Processing | Stock Analysis | Project Template |
| **UI Framework** | Streamlit | FastAPI | Streamlit | CLI |
| **AI Integration** | OpenAI GPT | Vector Search | Multi-Agent AI | Diagnostics |
| **Data Storage** | CSV/JSON | Qdrant Vector DB | Real-time APIs | File-based |
| **Deployment** | Streamlit Cloud | Docker | Streamlit Cloud | Local/Cloud |
| **Complexity** | Medium | High | High | Low |

## 🔧 Development

### Running Tests
Each project has its own testing setup:

```bash
# Simple Chatbot
cd simple-chatbot
python test_chatbot.py

# Simple RAG
cd simple-rag
python test_connection.py

# Simple Agent
cd simple-agent
python -m pytest tests/ -v

# Project Scaffold
cd project_scaffold/my_project
poetry run make test
```

### Code Quality
```bash
# Project Scaffold includes linting and formatting
cd project_scaffold/my_project
poetry run make lint
poetry run make format
poetry run make check
```

## 📈 Performance & Monitoring

### Simple Chatbot
- Real-time analytics dashboard
- Chat history export
- Feedback collection system
- Performance metrics tracking

### Simple RAG
- RAG evaluation metrics
- Vector search performance
- Document processing statistics
- API response time monitoring

### Simple Agent
- Multi-agent collaboration metrics
- Stock analysis performance tracking
- Real-time data processing statistics
- Agent response time monitoring

### Project Scaffold
- Comprehensive system diagnostics
- Database connectivity monitoring
- API status checks
- Resource usage tracking

## 🚀 Deployment

### Simple Chatbot
Deploy to Streamlit Cloud:
```bash
cd simple-chatbot
# Push to GitHub and connect to Streamlit Cloud
```

### Simple RAG
Deploy with Docker:
```bash
cd simple-rag
docker-compose up -d
```

### Simple Agent
Deploy to Streamlit Cloud:
```bash
cd simple-agent
# Push to GitHub and connect to Streamlit Cloud
# Or run locally: streamlit run streamlit_app.py
```

### Project Scaffold
Deploy as a monitoring service:
```bash
cd project_scaffold/my_project
poetry run python diagnostics.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all projects remain self-contained

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**OpenAI API Issues**
- Verify your API key is correct and has sufficient credits
- Check rate limits and wait if necessary
- Ensure proper environment variable setup

**Qdrant Connection Issues**
- Verify Docker is running
- Check port 6333 is available
- Ensure proper volume mounting for persistence

**Streamlit Issues**
- Check Python version compatibility
- Verify all dependencies are installed
- Check for port conflicts

### Getting Help
- Check individual project README files for detailed troubleshooting
- Review logs in project directories
- Ensure all prerequisites are met

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT API
- **Streamlit** for the amazing web framework
- **Qdrant** for the vector database
- **FastAPI** for the modern API framework
- **LangChain** for the AI agent framework
- **CrewAI** for multi-agent orchestration
- **Poetry** for dependency management

---

**Happy AI Development! 🚀✨**

*This collection demonstrates the power and versatility of modern AI tools and frameworks, from conversational interfaces to intelligent document processing, multi-agent financial analysis, and robust project scaffolding.* 