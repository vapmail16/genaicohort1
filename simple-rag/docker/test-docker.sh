#!/bin/bash

# Test script for Docker setup
# This script tests the Docker environment and verifies all services are working

set -e

echo "🐳 Testing Docker setup for Simple RAG Application"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Docker is running
echo "1. Checking Docker..."
if docker info > /dev/null 2>&1; then
    print_status 0 "Docker is running"
else
    print_status 1 "Docker is not running"
fi

# Check if Docker Compose is available
echo "2. Checking Docker Compose..."
if docker-compose --version > /dev/null 2>&1; then
    print_status 0 "Docker Compose is available"
else
    print_status 1 "Docker Compose is not available"
fi

# Check if .env file exists
echo "3. Checking environment file..."
if [ -f ".env" ]; then
    print_status 0 ".env file exists"
    if grep -q "OPENAI_API_KEY" .env; then
        print_status 0 "OPENAI_API_KEY is set"
    else
        print_warning "OPENAI_API_KEY not found in .env file"
    fi
else
    print_warning ".env file not found - create one with your OpenAI API key"
fi

# Check if data directory exists
echo "4. Checking data directory..."
if [ -d "data" ]; then
    pdf_count=$(find data -name "*.pdf" | wc -l)
    if [ $pdf_count -gt 0 ]; then
        print_status 0 "Data directory exists with $pdf_count PDF file(s)"
    else
        print_warning "Data directory exists but no PDF files found"
    fi
else
    print_warning "Data directory not found - create one and add PDF files"
fi

# Build Docker images
echo "5. Building Docker images..."
if docker-compose -f docker/docker-compose.yml build > /dev/null 2>&1; then
    print_status 0 "Docker images built successfully"
else
    print_status 1 "Failed to build Docker images"
fi

# Start services
echo "6. Starting services..."
if docker-compose -f docker/docker-compose.yml up -d > /dev/null 2>&1; then
    print_status 0 "Services started successfully"
else
    print_status 1 "Failed to start services"
fi

# Wait for services to be ready
echo "7. Waiting for services to be ready..."
sleep 10

# Check if Qdrant is responding
echo "8. Testing Qdrant connection..."
if curl -s http://localhost:6333/health > /dev/null 2>&1; then
    print_status 0 "Qdrant is responding"
else
    print_status 1 "Qdrant is not responding"
fi

# Check if Streamlit app is responding
echo "9. Testing Streamlit app..."
if curl -s http://localhost:8501 > /dev/null 2>&1; then
    print_status 0 "Streamlit app is responding"
else
    print_status 1 "Streamlit app is not responding"
fi

# Check container status
echo "10. Checking container status..."
if docker-compose ps | grep -q "Up"; then
    print_status 0 "All containers are running"
else
    print_status 1 "Some containers are not running"
fi

echo ""
echo "🎉 Docker setup test completed!"
echo ""
echo "📋 Summary:"
echo "  - Streamlit App: http://localhost:8501"
echo "  - Qdrant Dashboard: http://localhost:6333/dashboard"
echo ""
echo "📝 Next steps:"
echo "  1. Add PDF files to the data/ directory"
echo "  2. Run: make ingest (or docker-compose exec rag-app python docker-ingest.py)"
echo "  3. Access the app at http://localhost:8501"
echo ""
echo "🔧 Useful commands:"
echo "  - View logs: make logs"
echo "  - Stop services: make down"
echo "  - Restart services: make restart"
echo "  - Clean up: make clean" 