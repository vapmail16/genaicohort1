#!/bin/bash

# Quick Start Script for Docker Applications

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to create .env file
create_env_file() {
    local project_dir=$1
    local env_file="$project_dir/.env"
    
    if [ ! -f "$env_file" ]; then
        print_status "Creating .env file for $project_dir..."
        echo "# Environment variables for $project_dir" > "$env_file"
        echo "OPENAI_API_KEY=your_openai_api_key_here" >> "$env_file"
        
        # Add NEWS_API_KEY for simple-agent
        if [[ "$project_dir" == *"simple-agent"* ]]; then
            echo "NEWS_API_KEY=your_news_api_key_here" >> "$env_file"
        fi
        
        print_warning "Created template .env file in $project_dir"
        print_warning "Please edit $env_file and add your actual API keys"
    else
        print_success ".env file already exists in $project_dir"
    fi
}

# Main execution
main() {
    echo "🚀 Quick Start Guide for Docker Applications"
    echo "============================================"
    echo
    
    # Step 1: Verify Docker setup
    print_status "Step 1: Verifying Docker setup..."
    if ./verify_docker_setup.sh; then
        print_success "Docker setup verified successfully!"
    else
        print_error "Docker setup verification failed. Please fix issues and try again."
        exit 1
    fi
    
    echo
    
    # Step 2: Create .env files
    print_status "Step 2: Setting up environment variables..."
    
    projects=("simple-rag" "simple-agent" "simple-chatbot" "simple-rag-fork" "project_scaffold/my_project")
    
    for project in "${projects[@]}"; do
        if [ -d "$project" ]; then
            create_env_file "$project"
        fi
    done
    
    echo
    
    # Step 3: Instructions
    print_status "Step 3: Next steps..."
    echo
    echo "📋 Before running applications:"
    echo "   1. Edit the .env files created above"
    echo "   2. Add your actual API keys:"
    echo "      - OPENAI_API_KEY (required for all apps)"
    echo "      - NEWS_API_KEY (required for simple-agent)"
    echo
    echo "🚀 To run all applications:"
    echo "   ./run_all_docker.sh"
    echo
    echo "🛑 To stop all applications:"
    echo "   ./stop_all_docker.sh"
    echo
    echo "📱 Application URLs (when running all):"
    echo "   • Simple RAG:        http://localhost:8501"
    echo "   • Simple Agent:      http://localhost:8502"
    echo "   • Simple Chatbot:    http://localhost:8503"
    echo "   • Simple RAG Fork:   http://localhost:8504"
    echo "   • Project Scaffold:  Check logs for output"
    echo
    echo "📖 For detailed instructions, see: DOCKER_SETUP_GUIDE.md"
    echo
    print_success "Quick start setup complete!"
    print_warning "Remember to add your API keys to the .env files before running applications."
}

# Run main function
main "$@" 