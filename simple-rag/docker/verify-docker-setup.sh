#!/bin/bash

# Docker Setup Verification Script for Beginners
# This script checks if everything is properly configured for the RAG application

set -e

echo "🔍 Docker Setup Verification for Simple RAG Application"
echo "======================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        if [ "$3" = "critical" ]; then
            echo -e "${RED}This is a critical error. Please fix it before proceeding.${NC}"
            exit 1
        fi
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Initialize counters
PASSED=0
FAILED=0
WARNINGS=0

echo "📋 Checking Docker Installation..."
echo "--------------------------------"

# Check Docker installation
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_status 0 "Docker is installed: $DOCKER_VERSION"
    ((PASSED++))
else
    print_status 1 "Docker is not installed" "critical"
    ((FAILED++))
fi

# Check Docker Compose installation
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    print_status 0 "Docker Compose is installed: $COMPOSE_VERSION"
    ((PASSED++))
else
    print_status 1 "Docker Compose is not installed" "critical"
    ((FAILED++))
fi

# Check if Docker daemon is running
if docker info &> /dev/null; then
    print_status 0 "Docker daemon is running"
    ((PASSED++))
else
    print_status 1 "Docker daemon is not running" "critical"
    print_info "Please start Docker Desktop or Docker Engine"
    ((FAILED++))
fi

echo ""
echo "📁 Checking Project Structure..."
echo "-------------------------------"

# Check if required files exist
REQUIRED_FILES=("requirements.txt" "app.py" "config.py" "vector_store.py" "ingestion_service.py")
DOCKER_FILES=("docker/Dockerfile" "docker/docker-compose.yml")

# Check main application files
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "Found $file"
        ((PASSED++))
    else
        print_status 1 "Missing $file" "critical"
        ((FAILED++))
    fi
done

# Check Docker files
for file in "${DOCKER_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "Found $file"
        ((PASSED++))
    else
        print_status 1 "Missing $file" "critical"
        ((FAILED++))
    fi
done

# Check if data directory exists
if [ -d "data" ]; then
    print_status 0 "Data directory exists"
    ((PASSED++))
else
    print_warning "Data directory does not exist - will be created automatically"
    ((WARNINGS++))
fi

echo ""
echo "🔧 Checking Environment Setup..."
echo "-------------------------------"

# Check if .env file exists
if [ -f ".env" ]; then
    print_status 0 ".env file exists"
    ((PASSED++))
    
    # Check if OPENAI_API_KEY is set
    if grep -q "OPENAI_API_KEY" .env; then
        API_KEY=$(grep "OPENAI_API_KEY" .env | cut -d'=' -f2)
        if [[ "$API_KEY" == "sk-"* ]]; then
            print_status 0 "OPENAI_API_KEY appears to be valid"
            ((PASSED++))
        else
            print_warning "OPENAI_API_KEY format looks incorrect (should start with 'sk-')"
            ((WARNINGS++))
        fi
    else
        print_warning "OPENAI_API_KEY not found in .env file"
        ((WARNINGS++))
    fi
else
    print_warning ".env file not found - you'll need to create one with your OpenAI API key"
    ((WARNINGS++))
fi

echo ""
echo "🌐 Checking Network Connectivity..."
echo "---------------------------------"

# Check internet connectivity
if curl -s --max-time 5 https://www.google.com &> /dev/null; then
    print_status 0 "Internet connectivity is working"
    ((PASSED++))
else
    print_status 1 "No internet connectivity"
    ((FAILED++))
fi

# Check Docker Hub connectivity
if curl -s --max-time 5 https://hub.docker.com &> /dev/null; then
    print_status 0 "Docker Hub is accessible"
    ((PASSED++))
else
    print_status 1 "Cannot access Docker Hub"
    ((FAILED++))
fi

echo ""
echo "💾 Checking System Resources..."
echo "------------------------------"

# Check available disk space (need at least 5GB)
AVAILABLE_SPACE=$(df . | awk 'NR==2 {print $4}')
AVAILABLE_SPACE_GB=$((AVAILABLE_SPACE / 1024 / 1024))

if [ $AVAILABLE_SPACE_GB -ge 5 ]; then
    print_status 0 "Sufficient disk space available: ${AVAILABLE_SPACE_GB}GB"
    ((PASSED++))
else
    print_warning "Low disk space: ${AVAILABLE_SPACE_GB}GB available (recommend at least 5GB)"
    ((WARNINGS++))
fi

# Check available memory (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    TOTAL_MEM=$(sysctl hw.memsize | awk '{print $2}')
    TOTAL_MEM_GB=$((TOTAL_MEM / 1024 / 1024 / 1024))
    
    if [ $TOTAL_MEM_GB -ge 8 ]; then
        print_status 0 "Sufficient memory: ${TOTAL_MEM_GB}GB total"
        ((PASSED++))
    else
        print_warning "Low memory: ${TOTAL_MEM_GB}GB total (recommend at least 8GB)"
        ((WARNINGS++))
    fi
fi

echo ""
echo "🧪 Testing Docker Functionality..."
echo "--------------------------------"

# Test Docker can pull images
if docker pull hello-world &> /dev/null; then
    print_status 0 "Docker can pull images from Docker Hub"
    ((PASSED++))
else
    print_status 1 "Docker cannot pull images"
    ((FAILED++))
fi

# Test Docker can run containers
if docker run --rm hello-world &> /dev/null; then
    print_status 0 "Docker can run containers"
    ((PASSED++))
else
    print_status 1 "Docker cannot run containers"
    ((FAILED++))
fi

# Clean up test image
docker rmi hello-world &> /dev/null || true

# Test docker-compose syntax
if docker-compose -f docker/docker-compose.yml config &> /dev/null; then
    print_status 0 "Docker Compose configuration is valid"
    ((PASSED++))
else
    print_status 1 "Docker Compose configuration has errors"
    ((FAILED++))
fi

echo ""
echo "📊 Verification Summary"
echo "======================"
echo -e "${GREEN}✅ Passed: $PASSED${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARNINGS${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical checks passed! Your Docker setup is ready.${NC}"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Run: docker-compose build"
    echo "2. Run: docker-compose up -d"
    echo "3. Run: ./test-docker.sh"
    echo "4. Add PDF files to data/ directory"
    echo "5. Run: make ingest"
    echo "6. Access the app at http://localhost:8501"
else
    echo -e "${RED}❌ Some critical checks failed. Please fix the issues above before proceeding.${NC}"
    echo ""
    echo "🔧 Common fixes:"
    echo "- Install Docker Desktop if not installed"
    echo "- Start Docker Desktop if not running"
    echo "- Create .env file with your OpenAI API key"
    echo "- Check internet connectivity"
    exit 1
fi

if [ $WARNINGS -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Warnings detected. These won't prevent the app from running, but you should address them:${NC}"
    echo "- Create .env file with your OpenAI API key"
    echo "- Add PDF files to data/ directory"
    echo "- Ensure sufficient disk space and memory"
fi

echo ""
echo "📚 For detailed help, see DOCKER_SETUP_CHECKLIST.md" 