#!/bin/bash

# Simple RAG Application - Main Runner Script
# This script provides easy access to the organized project structure

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if command is provided
if [ $# -eq 0 ]; then
    echo "🚀 Simple RAG Application - Main Runner"
    echo "======================================"
    echo ""
    echo "📁 Project Structure:"
    echo "  src/          - Main application source code"
    echo "  docker/       - Docker configuration and scripts"
    echo "  docs/         - Documentation and guides"
    echo "  scripts/      - Utility scripts"
    echo "  examples/     - Example implementations"
    echo "  tests/        - Test files"
    echo "  data/         - PDF documents directory"
    echo ""
    echo "🚀 Quick Start:"
    echo "  ./run.sh docker start    - Start with Docker"
    echo "  ./run.sh docker status   - Check Docker status"
    echo "  ./run.sh docker logs     - View Docker logs"
    echo ""
    echo "📚 Documentation:"
    echo "  ./run.sh docs            - Open documentation"
    echo "  ./run.sh examples        - List examples"
    echo "  ./run.sh tests           - Run tests"
    echo ""
    echo "🔧 Development:"
    echo "  ./run.sh dev start       - Start in development mode"
    echo "  ./run.sh dev shell       - Open development shell"
    echo ""
    exit 1
fi

COMMAND=$1
SUBCOMMAND=$2

case $COMMAND in
    "docker")
        case $SUBCOMMAND in
            "start")
                print_info "Starting Docker services..."
                ./scripts/docker-run.sh start
                ;;
            "up")
                print_info "Starting Docker services..."
                ./scripts/docker-run.sh up
                ;;
            "down")
                print_info "Stopping Docker services..."
                ./scripts/docker-run.sh down
                ;;
            "status")
                print_info "Checking Docker status..."
                ./scripts/docker-run.sh status
                ;;
            "logs")
                print_info "Viewing Docker logs..."
                ./scripts/docker-run.sh logs
                ;;
            "restart")
                print_info "Restarting Docker services..."
                ./scripts/docker-run.sh restart
                ;;
            "clean")
                print_info "Cleaning up Docker..."
                ./scripts/docker-run.sh clean
                ;;
            "ingest")
                print_info "Running document ingestion..."
                ./scripts/docker-run.sh ingest
                ;;
            "shell")
                print_info "Opening Docker shell..."
                ./scripts/docker-run.sh shell
                ;;
            "verify")
                print_info "Verifying Docker setup..."
                ./scripts/docker-run.sh verify
                ;;
            *)
                echo "❌ Unknown Docker command: $SUBCOMMAND"
                echo "Available Docker commands: start, up, down, status, logs, restart, clean, ingest, shell, verify"
                exit 1
                ;;
        esac
        ;;
    "dev")
        case $SUBCOMMAND in
            "start")
                print_info "Starting in development mode..."
                ./scripts/docker-run.sh dev
                ;;
            "shell")
                print_info "Opening development shell..."
                ./scripts/docker-run.sh shell
                ;;
            *)
                echo "❌ Unknown development command: $SUBCOMMAND"
                echo "Available development commands: start, shell"
                exit 1
                ;;
        esac
        ;;
    "docs")
        print_info "📚 Documentation available in docs/ directory:"
        echo ""
        echo "📖 Main Documentation:"
        echo "  docs/README.md                    - Main project documentation"
        echo "  docs/DOCKER_ORGANIZATION.md       - Docker organization guide"
        echo "  docs/GITHUB_UPLOAD_GUIDE.md       - GitHub upload instructions"
        echo "  docs/FINAL_SUMMARY.md             - Project summary"
        echo ""
        echo "🐳 Docker Documentation:"
        echo "  docker/DOCKER_GUIDE.md            - Comprehensive Docker guide"
        echo "  docker/DOCKER_FOR_BEGINNERS.md    - Beginner-friendly guide"
        echo "  docker/DOCKER_SETUP_CHECKLIST.md  - Setup verification"
        echo "  docker/WHAT_YOU_NEED_TO_PROVIDE.md - Requirements guide"
        echo ""
        echo "💡 Quick Start:"
        echo "  ./run.sh docker start"
        echo "  # Then open http://localhost:8501"
        ;;
    "examples")
        print_info "📁 Examples available in examples/ directory:"
        echo ""
        echo "🔧 Application Examples:"
        echo "  examples/app_simple.py            - Simple Streamlit app"
        echo "  examples/app_hybrid.py            - Hybrid search app"
        echo "  examples/ingestion_service_simple.py - Simple ingestion"
        echo ""
        echo "🔍 Search Examples:"
        echo "  examples/hybrid_search.py         - Hybrid search implementation"
        echo "  examples/vector_store_simple.py   - Simple vector store"
        echo "  examples/vector_store_comparison.py - Vector store comparison"
        echo ""
        echo "🧹 Text Processing:"
        echo "  examples/text_cleaner.py          - Text cleaning utilities"
        echo "  examples/simple_text_cleaner.py   - Simple text cleaner"
        echo "  examples/demo_cleaning.py         - Cleaning demonstration"
        echo ""
        echo "📊 Evaluation & Debugging:"
        echo "  examples/evaluate_rag.py          - RAG evaluation"
        echo "  examples/inspect_chunk.py         - Chunk inspection"
        echo "  examples/print_all_chunks.py      - Print all chunks"
        ;;
    "tests")
        print_info "🧪 Tests available in tests/ directory:"
        echo ""
        echo "🔍 Test Files:"
        echo "  tests/test_connection.py          - Connection tests"
        echo "  tests/test_llm.py                 - LLM integration tests"
        echo "  tests/test_fix.py                 - Fix tests"
        echo "  tests/simple_test.py              - Simple tests"
        echo "  tests/debug_search.py             - Search debugging"
        echo ""
        echo "🚀 Run Tests:"
        echo "  cd tests && python test_connection.py"
        echo "  cd tests && python test_llm.py"
        ;;
    "structure")
        print_info "📁 Current Project Structure:"
        echo ""
        echo "📦 Root Directory:"
        echo "  ├── run.sh                        # Main runner script (this file)"
        echo "  ├── requirements.txt              # Python dependencies"
        echo "  ├── .env                          # Environment variables"
        echo "  ├── .gitignore                    # Git ignore rules"
        echo "  └── data/                         # PDF documents directory"
        echo ""
        echo "🔧 Source Code:"
        echo "  src/                              # Main application source"
        echo "  ├── app.py                        # Streamlit application"
        echo "  ├── config.py                     # Configuration"
        echo "  ├── ingestion_service.py          # Document processing"
        echo "  └── vector_store.py               # Vector database operations"
        echo ""
        echo "🐳 Docker:"
        echo "  docker/                           # All Docker-related files"
        echo "  ├── Dockerfile                    # Container configuration"
        echo "  ├── docker-compose.yml            # Multi-container setup"
        echo "  ├── docker-ingest.py              # Document ingestion"
        echo "  └── [documentation files]         # Docker guides"
        echo ""
        echo "📚 Documentation:"
        echo "  docs/                             # All documentation"
        echo "  ├── README.md                     # Main documentation"
        echo "  ├── DOCKER_ORGANIZATION.md        # Organization guide"
        echo "  ├── GITHUB_UPLOAD_GUIDE.md        # Upload instructions"
        echo "  └── FINAL_SUMMARY.md              # Project summary"
        echo ""
        echo "🛠️ Scripts:"
        echo "  scripts/                          # Utility scripts"
        echo "  ├── docker-run.sh                 # Docker management"
        echo "  └── Makefile                      # Make commands"
        echo ""
        echo "📖 Examples:"
        echo "  examples/                         # Example implementations"
        echo "  ├── app_*.py                      # Application examples"
        echo "  ├── hybrid_*.py                   # Hybrid search examples"
        echo "  ├── vector_store_*.py             # Vector store examples"
        echo "  └── [other examples]              # Various utilities"
        echo ""
        echo "🧪 Tests:"
        echo "  tests/                            # Test files"
        echo "  ├── test_*.py                     # Test files"
        echo "  ├── debug_*.py                    # Debug files"
        echo "  └── simple_test.py                # Simple tests"
        ;;
    *)
        echo "❌ Unknown command: $COMMAND"
        echo "Run './run.sh' without arguments to see available commands."
        exit 1
        ;;
esac 