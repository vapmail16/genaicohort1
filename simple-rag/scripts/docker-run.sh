#!/bin/bash

# Simple RAG Application - Docker Runner Script
# This script makes it easy to run Docker commands from the project root

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check if command is provided
if [ $# -eq 0 ]; then
    echo "🐳 Simple RAG Application - Docker Runner"
    echo "========================================"
    echo ""
    echo "Usage: ./docker-run.sh <command>"
    echo ""
    echo "Available commands:"
    echo "  start     - Build and start all services"
    echo "  up        - Start all services"
    echo "  down      - Stop all services"
    echo "  build     - Build Docker images"
    echo "  logs      - View logs from all services"
    echo "  status    - Show service status"
    echo "  restart   - Restart all services"
    echo "  clean     - Stop services and remove volumes"
    echo "  ingest    - Run document ingestion"
    echo "  shell     - Open shell in RAG app container"
    echo "  test      - Run Docker setup test"
    echo "  verify    - Run setup verification"
    echo "  dev       - Start in development mode"
    echo "  prod      - Start in production mode"
    echo ""
    echo "Examples:"
    echo "  ./docker-run.sh start"
    echo "  ./docker-run.sh logs"
    echo "  ./docker-run.sh status"
    exit 1
fi

COMMAND=$1

case $COMMAND in
    "start")
        print_info "Building and starting all services..."
        docker-compose -f docker/docker-compose.yml build
        docker-compose -f docker/docker-compose.yml up -d
        print_success "Services started! Access the app at http://localhost:8501"
        ;;
    "up")
        print_info "Starting all services..."
        docker-compose -f docker/docker-compose.yml up -d
        print_success "Services started!"
        ;;
    "down")
        print_info "Stopping all services..."
        docker-compose -f docker/docker-compose.yml down
        print_success "Services stopped!"
        ;;
    "build")
        print_info "Building Docker images..."
        docker-compose -f docker/docker-compose.yml build
        print_success "Build completed!"
        ;;
    "logs")
        print_info "Viewing logs..."
        docker-compose -f docker/docker-compose.yml logs -f
        ;;
    "status")
        print_info "Service status:"
        docker-compose -f docker/docker-compose.yml ps
        ;;
    "restart")
        print_info "Restarting services..."
        docker-compose -f docker/docker-compose.yml restart
        print_success "Services restarted!"
        ;;
    "clean")
        print_info "Cleaning up..."
        docker-compose -f docker/docker-compose.yml down -v
        docker system prune -f
        print_success "Cleanup completed!"
        ;;
    "ingest")
        print_info "Running document ingestion..."
        docker-compose -f docker/docker-compose.yml exec rag-app python docker/docker-ingest.py
        ;;
    "shell")
        print_info "Opening shell in RAG app container..."
        docker-compose -f docker/docker-compose.yml exec rag-app bash
        ;;
    "test")
        print_info "Running Docker setup test..."
        ./docker/test-docker.sh
        ;;
    "verify")
        print_info "Running setup verification..."
        ./docker/verify-docker-setup.sh
        ;;
    "dev")
        print_info "Starting in development mode..."
        docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d
        print_success "Development mode started!"
        ;;
    "prod")
        print_info "Starting in production mode..."
        docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d
        print_success "Production mode started!"
        ;;
    *)
        echo "❌ Unknown command: $COMMAND"
        echo "Run './docker-run.sh' without arguments to see available commands."
        exit 1
        ;;
esac 