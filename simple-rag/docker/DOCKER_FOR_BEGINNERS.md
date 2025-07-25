# Docker for Beginners - Simple RAG Setup Guide

This guide is designed for people who are new to Docker and want to run the Simple RAG application.

## 🤔 What is Docker?

Think of Docker like a shipping container for software. Just like how shipping containers can be moved between ships, trucks, and trains without changing their contents, Docker containers can run on any computer that has Docker installed.

### Key Concepts:
- **Container**: A lightweight, standalone package that includes everything needed to run an application
- **Image**: A template used to create containers (like a blueprint)
- **Docker Compose**: A tool for defining and running multi-container applications

## 🎯 Why Use Docker for This Project?

1. **No Installation Hassles**: You don't need to install Python, Qdrant, or any dependencies manually
2. **Consistent Environment**: Works the same way on any computer
3. **Easy Cleanup**: Can be completely removed without affecting your system
4. **Isolation**: Won't interfere with other software on your computer

## 📋 What You Need to Provide

### 1. Your OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create a new API key
- Copy the key (it starts with `sk-`)

### 2. PDF Documents
- Any PDF files you want to ask questions about
- Place them in the `data/` folder

### 3. System Requirements
- **macOS**: macOS 10.15 or later
- **Windows**: Windows 10 Pro, Enterprise, or Education (64-bit)
- **Linux**: Ubuntu 18.04+, CentOS 7+, or similar
- **Memory**: At least 4GB RAM (8GB recommended)
- **Storage**: At least 5GB free space

## 🚀 Step-by-Step Setup

### Step 1: Install Docker Desktop

#### For macOS:
1. Go to https://www.docker.com/products/docker-desktop
2. Click "Download for Mac"
3. Open the downloaded `.dmg` file
4. Drag Docker to Applications folder
5. Open Docker from Applications
6. Wait for Docker to start (whale icon in menu bar turns green)

#### For Windows:
1. Go to https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer
4. Follow the installation wizard
5. Restart your computer if prompted
6. Start Docker Desktop from Start menu

#### For Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
# Log out and log back in
```

### Step 2: Verify Docker Installation

Open Terminal (macOS/Linux) or Command Prompt (Windows) and run:

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker
docker run hello-world
```

You should see:
- Docker version information
- Docker Compose version information
- A "Hello from Docker!" message

### Step 3: Download the Project

1. Clone or download the project files
2. Open Terminal/Command Prompt
3. Navigate to the project folder:
   ```bash
   cd path/to/simple-rag
   ```

### Step 4: Run the Verification Script

```bash
# Make the script executable (macOS/Linux only)
chmod +x verify-docker-setup.sh

# Run the verification
./verify-docker-setup.sh
```

This script will check everything and tell you what's missing.

### Step 5: Create Environment File

Create a file named `.env` in the project folder:

```bash
# Create the file
touch .env

# Add your OpenAI API key (replace with your actual key)
echo "OPENAI_API_KEY=sk-your-actual-api-key-here" > .env
```

**Important**: Replace `sk-your-actual-api-key-here` with your real OpenAI API key.

### Step 6: Add Your Documents

1. Create a `data` folder in the project directory
2. Copy your PDF files into the `data` folder

```bash
# Create data directory
mkdir -p data

# Copy your PDF files (example)
cp /path/to/your/document.pdf data/
```

### Step 7: Build and Start the Application

```bash
# Build the Docker images (first time only, takes 5-10 minutes)
docker-compose build

# Start the services
docker-compose up -d

# Check if services are running
docker-compose ps
```

You should see both `rag-app` and `qdrant` services showing "Up" status.

### Step 8: Process Your Documents

```bash
# Ingest your PDF documents into the system
docker-compose exec rag-app python docker-ingest.py
```

You should see messages about documents being processed and chunks being created.

### Step 9: Access the Application

Open your web browser and go to:
- **Main App**: http://localhost:8501
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## 🎉 You're Done!

Now you can:
1. Ask questions about your documents in the web interface
2. Adjust search parameters
3. Get AI-powered answers based on your documents

## 🔧 Common Commands

```bash
# View logs
docker-compose logs

# Stop the application
docker-compose down

# Restart the application
docker-compose restart

# Add new documents and re-ingest
docker-compose exec rag-app python docker-ingest.py

# Access the container shell (for debugging)
docker-compose exec rag-app bash
```

## 🐛 Troubleshooting

### "Docker command not found"
- Make sure Docker Desktop is installed and running
- Restart your terminal/command prompt

### "Permission denied"
- On macOS/Windows: Make sure Docker Desktop is running
- On Linux: Add your user to the docker group and log out/in

### "Port already in use"
- Stop other applications using ports 8501 or 6333
- Or change ports in `docker-compose.yml`

### "Out of memory"
- Close other applications
- Increase Docker Desktop memory allocation (Settings → Resources)

### "Build failed"
- Check your internet connection
- Try: `docker-compose build --no-cache`

### "Cannot connect to services"
- Check if services are running: `docker-compose ps`
- View logs: `docker-compose logs`
- Restart: `docker-compose restart`

## 📚 Understanding What's Running

### Services:
1. **Qdrant** (Port 6333): Vector database that stores document embeddings
2. **RAG App** (Port 8501): Streamlit web interface for asking questions

### What Happens When You Ask a Question:
1. Your question gets converted to a vector (embedding)
2. The system searches for similar text chunks in your documents
3. Relevant chunks are sent to OpenAI's GPT model
4. GPT generates an answer based on those chunks
5. The answer is displayed in the web interface

## 🧹 Cleanup

To completely remove everything:

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (this deletes all data)
docker-compose down -v

# Remove images
docker rmi simple-rag_rag-app qdrant/qdrant

# Clean up Docker system
docker system prune -a
```

## 🆘 Getting Help

1. **Check the logs**: `docker-compose logs`
2. **Run verification**: `./verify-docker-setup.sh`
3. **Check documentation**: `DOCKER_GUIDE.md`
4. **Common issues**: See troubleshooting section above

## 🎓 Learning More

- [Docker Official Tutorial](https://docs.docker.com/get-started/)
- [Docker Compose Tutorial](https://docs.docker.com/compose/)
- [Docker Desktop Documentation](https://docs.docker.com/desktop/)

---

**Remember**: Docker is just a tool to make your life easier. The goal is to get your RAG application running without worrying about complex installations and dependencies! 