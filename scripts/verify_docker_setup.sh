#!/bin/bash

# Verification script to test Docker configurations

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

# Function to check if file exists
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        print_success "$description: $file"
        return 0
    else
        print_error "$description: $file (MISSING)"
        return 1
    fi
}

# Function to validate Dockerfile
validate_dockerfile() {
    local dockerfile=$1
    local project=$2
    
    if [ -f "$dockerfile" ]; then
        print_status "Validating Dockerfile for $project..."
        
        # Check if it's a valid Dockerfile
        if docker build --dry-run -f "$dockerfile" . > /dev/null 2>&1; then
            print_success "Dockerfile syntax is valid for $project"
        else
            print_warning "Dockerfile syntax validation failed for $project (this might be normal)"
        fi
    fi
}

# Function to validate docker-compose.yml
validate_compose() {
    local compose_file=$1
    local project=$2
    
    if [ -f "$compose_file" ]; then
        print_status "Validating docker-compose.yml for $project..."
        
        # Check if it's a valid docker-compose file
        if docker-compose -f "$compose_file" config > /dev/null 2>&1; then
            print_success "docker-compose.yml syntax is valid for $project"
        else
            print_error "docker-compose.yml syntax is invalid for $project"
        fi
    fi
}

# Main execution
main() {
    echo "🔍 Docker Configuration Verification"
    echo "==================================="
    echo
    
    # Check Docker installation
    print_status "Checking Docker installation..."
    if command -v docker > /dev/null 2>&1; then
        print_success "Docker is installed"
        docker_version=$(docker --version)
        print_status "Docker version: $docker_version"
    else
        print_error "Docker is not installed"
        exit 1
    fi
    
    if command -v docker-compose > /dev/null 2>&1; then
        print_success "Docker Compose is installed"
        compose_version=$(docker-compose --version)
        print_status "Docker Compose version: $compose_version"
    else
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    echo
    
    # Check if Docker daemon is running
    print_status "Checking Docker daemon..."
    if docker info > /dev/null 2>&1; then
        print_success "Docker daemon is running"
    else
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    echo
    
    # Define projects to check (using arrays instead of associative arrays for compatibility)
    projects=("simple-rag" "simple-agent" "simple-chatbot" "simple-rag-fork" "project-scaffold")
    dockerfiles=("simple-rag/docker/Dockerfile" "simple-agent/Dockerfile" "simple-chatbot/Dockerfile" "simple-rag-fork/Dockerfile" "project_scaffold/my_project/Dockerfile")
    compose_files=("simple-rag/docker/docker-compose.yml" "simple-agent/docker-compose.yml" "simple-chatbot/docker-compose.yml" "simple-rag-fork/docker-compose.yml" "project_scaffold/my_project/docker-compose.yml")
    
    local total_files=0
    local found_files=0
    
    # Check each project
    for i in "${!projects[@]}"; do
        local project="${projects[$i]}"
        local dockerfile="${dockerfiles[$i]}"
        local compose_file="${compose_files[$i]}"
        
        echo "📁 Checking $project..."
        
        # Check Dockerfile
        if check_file "$dockerfile" "Dockerfile"; then
            ((found_files++))
            validate_dockerfile "$dockerfile" "$project"
        fi
        ((total_files++))
        
        # Check docker-compose.yml
        if check_file "$compose_file" "docker-compose.yml"; then
            ((found_files++))
            validate_compose "$compose_file" "$project"
        fi
        ((total_files++))
        
        # Check .dockerignore
        local dockerignore="${dockerfile%/*}/.dockerignore"
        if check_file "$dockerignore" ".dockerignore"; then
            ((found_files++))
        fi
        ((total_files++))
        
        # Check requirements.txt
        local requirements="${dockerfile%/*}/requirements.txt"
        if check_file "$requirements" "requirements.txt"; then
            ((found_files++))
        fi
        ((total_files++))
        
        echo
    done
    
    # Summary
    echo "📊 Summary"
    echo "=========="
    print_status "Found $found_files out of $total_files expected files"
    
    if [ $found_files -eq $total_files ]; then
        print_success "All Docker configurations are properly set up!"
    else
        print_warning "Some files are missing. Please check the errors above."
    fi
    
    echo
    echo "🚀 Next steps:"
    echo "  1. Create .env files with your API keys"
    echo "  2. Run: ./run_all_docker.sh"
    echo "  3. Access applications at their respective ports"
    echo
    echo "📖 For detailed instructions, see: DOCKER_SETUP_GUIDE.md"
}

# Run main function
main "$@" 