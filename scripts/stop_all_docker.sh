#!/bin/bash

# Master script to stop all Docker applications

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

# Function to stop application
stop_app() {
    local app_name=$1
    local project_dir=$2
    local compose_file=$3
    
    print_status "Stopping $app_name..."
    
    if [ -d "$project_dir" ]; then
        cd "$project_dir"
        if docker-compose -f "$compose_file" down; then
            print_success "$app_name stopped successfully"
        else
            print_warning "Failed to stop $app_name (might not be running)"
        fi
    else
        print_warning "Directory $project_dir not found. Skipping $app_name"
    fi
}

# Main execution
main() {
    echo "🛑 Docker Application Stopper"
    echo "============================"
    
    # Define applications and their configurations (using arrays for compatibility)
    app_names=("simple-rag" "simple-agent" "simple-chatbot" "simple-rag-fork" "project-scaffold")
    project_dirs=("simple-rag" "simple-agent" "simple-chatbot" "simple-rag-fork" "project_scaffold/my_project")
    compose_files=("docker/docker-compose.yml" "docker-compose.yml" "docker-compose.yml" "docker-compose.yml" "docker-compose.yml")
    
    print_status "Stopping all applications..."
    echo
    
    # Stop each application
    for i in "${!app_names[@]}"; do
        local app_name="${app_names[$i]}"
        local project_dir="${project_dirs[$i]}"
        local compose_file="${compose_files[$i]}"
        stop_app "$app_name" "$project_dir" "$compose_file"
        echo
    done
    
    print_status "Cleaning up any remaining containers..."
    
    # Stop any remaining containers that might be running
    if docker ps --format "table {{.Names}}" | grep -q -E "(simple-|rag-|chatbot|project-scaffold)"; then
        docker ps --format "table {{.Names}}" | grep -E "(simple-|rag-|chatbot|project-scaffold)" | xargs -r docker stop
        print_success "Stopped remaining containers"
    else
        print_status "No remaining containers to stop"
    fi
    
    echo
    print_success "All applications stopped!"
    echo
    echo "🧹 To clean up volumes and networks:"
    echo "  docker system prune -a"
    echo
    echo "📊 To verify all containers are stopped:"
    echo "  docker ps"
}

# Run main function
main "$@" 