#!/bin/bash

# Master script to run all Docker applications
# This script runs each application on different ports to avoid conflicts

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# Function to create .env file if it doesn't exist
create_env_file() {
    local project_dir=$1
    local env_file="$project_dir/.env"
    
    if [ ! -f "$env_file" ]; then
        print_warning "No .env file found in $project_dir"
        echo "# Environment variables for $project_dir" > "$env_file"
        echo "OPENAI_API_KEY=your_openai_api_key_here" >> "$env_file"
        
        # Add NEWS_API_KEY for simple-agent
        if [[ "$project_dir" == *"simple-agent"* ]]; then
            echo "NEWS_API_KEY=your_news_api_key_here" >> "$env_file"
        fi
        
        print_warning "Created template .env file in $project_dir"
        print_warning "Please edit $env_file and add your actual API keys"
    fi
}

# Function to run application with custom port
run_app() {
    local app_name=$1
    local project_dir=$2
    local port=$3
    local compose_file=$4
    
    print_status "Starting $app_name on port $port..."
    
    # Create .env file if needed
    create_env_file "$project_dir"
    
    # Check if port is available
    if ! check_port $port; then
        print_error "Port $port is already in use. Skipping $app_name"
        return 1
    fi
    
    # Create temporary docker-compose override
    local override_file="$project_dir/docker-compose.override.yml"
    cat > "$override_file" << EOF
version: '3.8'
services:
  $(docker-compose -f "$compose_file" config --services | head -1):
    ports:
      - "$port:8501"
EOF
    
    # Start the application
    cd "$project_dir"
    if docker-compose -f "$compose_file" -f "$override_file" up -d; then
        print_success "$app_name started successfully on http://localhost:$port"
    else
        print_error "Failed to start $app_name"
        rm -f "$override_file"
        return 1
    fi
    
    # Clean up override file
    rm -f "$override_file"
}

# Main execution
main() {
    echo "🐳 Docker Application Launcher"
    echo "=============================="
    
    # Check Docker
    check_docker
    
    # Define applications and their configurations (using arrays for compatibility)
    app_names=("simple-rag" "simple-agent" "simple-chatbot" "simple-rag-fork" "project-scaffold")
    project_dirs=("simple-rag" "simple-agent" "simple-chatbot" "simple-rag-fork" "project_scaffold/my_project")
    compose_files=("docker/docker-compose.yml" "docker-compose.yml" "docker-compose.yml" "docker-compose.yml" "docker-compose.yml")
    ports=("8501" "8502" "8503" "8504" "8505")
    
    print_status "Starting all applications..."
    echo
    
    # Start each application
    for i in "${!app_names[@]}"; do
        local app_name="${app_names[$i]}"
        local project_dir="${project_dirs[$i]}"
        local compose_file="${compose_files[$i]}"
        local port="${ports[$i]}"
        
        if [ -d "$project_dir" ]; then
            run_app "$app_name" "$project_dir" "$port" "$compose_file"
        else
            print_warning "Directory $project_dir not found. Skipping $app_name"
        fi
        echo
    done
    
    echo "🎉 All applications started!"
    echo
    echo "📱 Application URLs:"
    echo "  • Simple RAG:        http://localhost:8501"
    echo "  • Simple Agent:      http://localhost:8502"
    echo "  • Simple Chatbot:    http://localhost:8503"
    echo "  • Simple RAG Fork:   http://localhost:8504"
    echo "  • Project Scaffold:  Check logs for output"
    echo
    echo "📊 Monitor containers:"
    echo "  docker ps"
    echo
    echo "📋 View logs:"
    echo "  docker-compose logs -f"
    echo
    echo "🛑 Stop all applications:"
    echo "  ./stop_all_docker.sh"
}

# Run main function
main "$@" 