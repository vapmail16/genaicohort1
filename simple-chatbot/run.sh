#!/bin/bash

# AWS EC2 Deployment Script for AI Chatbot Assistant
# This script handles Docker installation, image building, and container deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="ai-chatbot"
CONTAINER_NAME="chatbot-container"
IMAGE_NAME="chatbot-app"
PORT=80
DOCKERFILE="Dockerfile"

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Docker
install_docker() {
    print_status "Installing Docker..."
    
    # Update package index
    sudo apt-get update
    
    # Install required packages
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Set up stable repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Update package index again
    sudo apt-get update
    
    # Install Docker Engine
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Add current user to docker group to avoid sudo
    sudo usermod -aG docker $USER
    
    print_success "Docker installed successfully!"
    print_warning "Please log out and log back in for group changes to take effect, or run 'newgrp docker'"
}

# Function to check Docker installation
check_docker() {
    if ! command_exists docker; then
        print_error "Docker is not installed!"
        read -p "Do you want to install Docker? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_docker
        else
            print_error "Docker is required to run this application. Exiting."
            exit 1
        fi
    else
        print_success "Docker is already installed"
    fi
}

# Function to check if user is in docker group
check_docker_permissions() {
    if ! groups $USER | grep -q '\bdocker\b'; then
        print_warning "User is not in docker group. Adding user to docker group..."
        sudo usermod -aG docker $USER
        print_warning "Please run 'newgrp docker' or log out and log back in, then run this script again."
        exit 1
    fi
}

# Function to stop and remove existing container
cleanup_existing_container() {
    if docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_status "Stopping existing container..."
        docker stop $CONTAINER_NAME || true
        docker rm $CONTAINER_NAME || true
        print_success "Existing container removed"
    fi
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image..."
    
    if [ ! -f "$DOCKERFILE" ]; then
        print_error "Dockerfile not found!"
        exit 1
    fi
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    if [ ! -f "app.py" ]; then
        print_error "app.py not found!"
        exit 1
    fi
    
    # Build the image
    docker build -t $IMAGE_NAME .
    
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully!"
    else
        print_error "Failed to build Docker image!"
        exit 1
    fi
}

# Function to run the container
run_container() {
    print_status "Starting container..."
    
    # Check if port 80 is already in use
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $PORT is already in use. Stopping existing process..."
        sudo fuser -k $PORT/tcp || true
        sleep 2
    fi
    
    # Run the container
    docker run -d \
        --name $CONTAINER_NAME \
        --restart unless-stopped \
        -p $PORT:80 \
        -e OPENAI_API_KEY="${OPENAI_API_KEY:-your_openai_api_key_here}" \
        -e DEFAULT_MODEL="${DEFAULT_MODEL:-gpt-3.5-turbo}" \
        -e MAX_TOKENS="${MAX_TOKENS:-1000}" \
        -e TEMPERATURE="${TEMPERATURE:-0.7}" \
        -e LOG_LEVEL="${LOG_LEVEL:-INFO}" \
        $IMAGE_NAME
    
    if [ $? -eq 0 ]; then
        print_success "Container started successfully!"
        print_status "Application is running on: http://localhost:$PORT"
        print_status "Container name: $CONTAINER_NAME"
    else
        print_error "Failed to start container!"
        exit 1
    fi
}

# Function to show container status
show_status() {
    print_status "Container Status:"
    docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    print_status "Container Logs (last 10 lines):"
    docker logs --tail 10 $CONTAINER_NAME
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --install-docker    Install Docker (requires sudo)"
    echo "  --build-only        Only build the Docker image"
    echo "  --run-only          Only run the container (assumes image exists)"
    echo "  --stop              Stop the running container"
    echo "  --restart           Restart the container"
    echo "  --logs              Show container logs"
    echo "  --status            Show container status"
    echo "  --cleanup           Remove container and image"
    echo "  --help              Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  OPENAI_API_KEY      Your OpenAI API key (required)"
    echo "  DEFAULT_MODEL       GPT model to use (default: gpt-3.5-turbo)"
    echo "  MAX_TOKENS          Maximum tokens per response (default: 1000)"
    echo "  TEMPERATURE         Response creativity (default: 0.7)"
    echo "  LOG_LEVEL           Logging level (default: INFO)"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Full deployment"
    echo "  $0 --build-only                      # Only build image"
    echo "  $0 --run-only                        # Only run container"
    echo "  OPENAI_API_KEY=your_key $0           # Deploy with API key"
}

# Main script logic
main() {
    print_status "Starting AWS EC2 deployment for AI Chatbot Assistant..."
    
    # Parse command line arguments
    case "${1:-}" in
        --install-docker)
            install_docker
            exit 0
            ;;
        --build-only)
            check_docker
            check_docker_permissions
            build_image
            exit 0
            ;;
        --run-only)
            check_docker
            check_docker_permissions
            cleanup_existing_container
            run_container
            show_status
            exit 0
            ;;
        --stop)
            print_status "Stopping container..."
            docker stop $CONTAINER_NAME || true
            print_success "Container stopped"
            exit 0
            ;;
        --restart)
            print_status "Restarting container..."
            docker restart $CONTAINER_NAME || true
            show_status
            exit 0
            ;;
        --logs)
            docker logs -f $CONTAINER_NAME
            exit 0
            ;;
        --status)
            show_status
            exit 0
            ;;
        --cleanup)
            print_status "Cleaning up..."
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            docker rmi $IMAGE_NAME || true
            print_success "Cleanup completed"
            exit 0
            ;;
        --help)
            show_help
            exit 0
            ;;
        "")
            # Full deployment
            check_docker
            check_docker_permissions
            cleanup_existing_container
            build_image
            run_container
            show_status
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root is not recommended. Consider using a regular user."
fi

# Run main function
main "$@"