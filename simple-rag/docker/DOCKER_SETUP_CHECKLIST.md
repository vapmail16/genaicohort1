# Docker Setup Checklist for Beginners

This checklist will help you verify that Docker is properly installed and configured on your system, and that your RAG project is ready to run with Docker.

## 🔍 Pre-Flight Checklist

### 1. Docker Installation Verification

#### Check Docker Installation
```bash
# Check if Docker is installed
docker --version

# Check if Docker Compose is installed
docker-compose --version

# Check if Docker daemon is running
docker info
```

**Expected Output:**
- Docker version should be 20.10+ 
- Docker Compose version should be 2.0+
- `docker info` should show system information (not an error)

#### If Docker is NOT installed:
- **macOS**: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- **Windows**: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- **Linux**: Follow instructions at https://docs.docker.com/engine/install/

### 2. Docker Desktop Setup (macOS/Windows)

#### Verify Docker Desktop is Running
- Look for the Docker whale icon in your system tray/menu bar
- It should be green (running) not red (stopped)
- Click the icon to open Docker Desktop dashboard

#### Check Docker Desktop Settings
1. Open Docker Desktop
2. Go to Settings/Preferences
3. Verify these settings:
   - **Resources**: At least 4GB RAM allocated
   - **Disk**: At least 20GB free space
   - **File Sharing**: Your project directory should be accessible

### 3. Project Structure Verification

#### Check Your Project Files
```bash
# List all files in your project
ls -la

# Verify these files exist:
# ✅ Dockerfile
# ✅ docker-compose.yml
# ✅ requirements.txt
# ✅ app.py
# ✅ config.py
# ✅ vector_store.py
# ✅ ingestion_service.py
```

#### Verify File Contents
```bash
# Check if Dockerfile has content
head -5 Dockerfile

# Check if docker-compose.yml has content
head -10 docker-compose.yml

# Check if requirements.txt has dependencies
cat requirements.txt
```

### 4. Environment Setup

#### Create Environment File
```bash
# Create .env file
touch .env

# Add your OpenAI API key (replace with your actual key)
echo "OPENAI_API_KEY=sk-your-actual-openai-api-key-here" > .env

# Verify the file was created
cat .env
```

**⚠️ Important**: 
- Never commit your `.env` file to git
- Replace `sk-your-actual-openai-api-key-here` with your real OpenAI API key
- Get your API key from https://platform.openai.com/api-keys

#### Create Data Directory
```bash
# Create data directory for PDF files
mkdir -p data

# Verify it exists
ls -la data/
```

### 5. Test Docker Commands

#### Test Basic Docker Commands
```bash
# Test Docker can pull images
docker pull hello-world

# Test Docker can run containers
docker run hello-world

# Clean up test
docker rmi hello-world
```

#### Test Docker Compose
```bash
# Test docker-compose syntax
docker-compose config

# This should show your configuration without errors
```

### 6. System Requirements Check

#### Check Available Resources
```bash
# Check available disk space (need at least 5GB free)
df -h

# Check available memory (need at least 4GB)
free -h  # Linux
# or
vm_stat  # macOS
```

#### Check Network Connectivity
```bash
# Test internet connection
curl -I https://www.google.com

# Test Docker Hub connectivity
curl -I https://hub.docker.com
```

## 🚀 First-Time Setup Steps

### Step 1: Build the Images
```bash
# Build Docker images (this may take 5-10 minutes first time)
docker-compose build

# Watch for any error messages
# Success: "Successfully built [image-id]"
```

### Step 2: Start the Services
```bash
# Start all services
docker-compose up -d

# Check if services are running
docker-compose ps

# Expected output: Both 'rag-app' and 'qdrant' should show 'Up' status
```

### Step 3: Check Service Health
```bash
# Check Qdrant health
curl http://localhost:6333/health

# Check Streamlit app
curl -I http://localhost:8501

# View logs if there are issues
docker-compose logs
```

### Step 4: Add Test Documents
```bash
# Copy a test PDF to data directory
# (You can use any PDF file you have)

# Check if file is accessible in container
docker-compose exec rag-app ls -la /app/data/
```

### Step 5: Run Document Ingestion
```bash
# Ingest documents into vector database
docker-compose exec rag-app python docker-ingest.py

# Look for success message: "Successfully ingested X chunks"
```

## 🐛 Common Issues & Solutions

### Issue 1: "Docker command not found"
**Solution**: Install Docker Desktop or Docker Engine

### Issue 2: "Permission denied" errors
**Solution**: 
- macOS/Windows: Make sure Docker Desktop is running
- Linux: Add your user to docker group: `sudo usermod -aG docker $USER`

### Issue 3: "Port already in use"
**Solution**: 
```bash
# Check what's using the port
lsof -i :8501
lsof -i :6333

# Stop conflicting services or change ports in docker-compose.yml
```

### Issue 4: "Out of memory" errors
**Solution**: 
- Increase Docker Desktop memory allocation (Settings → Resources)
- Close other applications to free up memory

### Issue 5: "Build failed" errors
**Solution**:
```bash
# Clean build cache
docker-compose build --no-cache

# Check internet connection
# Verify requirements.txt is valid
```

### Issue 6: "Connection refused" to services
**Solution**:
```bash
# Check if services are running
docker-compose ps

# Check service logs
docker-compose logs rag-app
docker-compose logs qdrant

# Restart services
docker-compose restart
```

## ✅ Success Indicators

You'll know everything is working when:

1. **Docker commands work**: `docker --version` shows version
2. **Services start**: `docker-compose ps` shows both services as "Up"
3. **Qdrant responds**: `curl http://localhost:6333/health` returns JSON
4. **App loads**: http://localhost:8501 shows Streamlit interface
5. **Ingestion works**: `docker-compose exec rag-app python docker-ingest.py` succeeds
6. **Queries work**: You can ask questions in the Streamlit app

## 📞 Getting Help

If you encounter issues:

1. **Check logs**: `docker-compose logs`
2. **Restart services**: `docker-compose restart`
3. **Clean restart**: `docker-compose down && docker-compose up -d`
4. **Full reset**: `docker-compose down -v && docker system prune -a`

## 🎯 Next Steps After Setup

Once everything is working:

1. Add your PDF documents to the `data/` directory
2. Run document ingestion: `make ingest`
3. Access the app: http://localhost:8501
4. Start asking questions about your documents!

## 📚 Learning Resources

- [Docker Official Tutorial](https://docs.docker.com/get-started/)
- [Docker Compose Tutorial](https://docs.docker.com/compose/)
- [Docker Desktop Documentation](https://docs.docker.com/desktop/) 