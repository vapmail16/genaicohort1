# Docker Setup Guide for All Applications

This guide provides instructions for running all applications in this workspace using Docker.

## 📋 Overview

All applications in this workspace are now Docker-ready with the following configurations:

### Applications with Docker Support

1. **simple-rag** ✅ (Already had comprehensive setup)
   - Multi-container setup with Qdrant vector database
   - Development and production configurations
   - Located in `simple-rag/docker/`

2. **simple-agent** ✅ (Newly added)
   - Stock analysis agent with Streamlit interface
   - Single container setup
   - Located in `simple-agent/`

3. **simple-chatbot** ✅ (Newly added)
   - AI chatbot with Streamlit interface
   - Single container setup
   - Located in `simple-chatbot/`

4. **simple-rag-fork** ✅ (Newly added)
   - RAG application with Streamlit interface
   - Single container setup
   - Located in `simple-rag-fork/`

5. **project_scaffold** ✅ (Enhanced)
   - Poetry-based project template
   - Single container setup
   - Located in `project_scaffold/my_project/`

## 🚀 Quick Start

### Prerequisites

1. **Docker** installed on your system
2. **Docker Compose** installed
3. **Environment variables** configured (see below)

### Environment Variables

Create a `.env` file in each project directory with the required API keys:

```bash
# Required for most applications
OPENAI_API_KEY=your_openai_api_key_here

# Required for simple-agent
NEWS_API_KEY=your_news_api_key_here
```

## 📱 Running Individual Applications

### 1. Simple RAG (Multi-container)

```bash
cd simple-rag
docker-compose -f docker/docker-compose.yml up -d
```

**Access:** http://localhost:8501

### 2. Simple Agent (Stock Analysis)

```bash
cd simple-agent
docker-compose up -d
```

**Access:** http://localhost:8501

### 3. Simple Chatbot

```bash
cd simple-chatbot
docker-compose up -d
```

**Access:** http://localhost:8501

### 4. Simple RAG Fork

```bash
cd simple-rag-fork
docker-compose up -d
```

**Access:** http://localhost:8501

### 5. Project Scaffold

```bash
cd project_scaffold/my_project
docker-compose up -d
```

**Access:** Check logs for output

## 🔧 Development Mode

For development, you can use the development configurations:

### Simple RAG (Development)
```bash
cd simple-rag
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d
```

## 📊 Monitoring

### Check Container Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f
```

### Health Checks
All containers include health checks that monitor application status.

## 🛠️ Management Commands

### Build Images
```bash
docker-compose build
```

### Stop Applications
```bash
docker-compose down
```

### Restart Applications
```bash
docker-compose restart
```

### Remove Volumes (Clean Slate)
```bash
docker-compose down -v
```

## 🔍 Troubleshooting

### Port Conflicts
If you get port conflicts, modify the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "8502:8501"  # Change 8501 to 8502 or another port
```

### Environment Variables
Ensure your `.env` file is in the correct directory and contains valid API keys.

### Build Issues
If you encounter build issues:

1. Clean Docker cache:
   ```bash
   docker system prune -a
   ```

2. Rebuild without cache:
   ```bash
   docker-compose build --no-cache
   ```

### Permission Issues
On Linux/macOS, you might need to adjust file permissions:
```bash
chmod +x start_app.sh
```

## 📁 File Structure

Each application now includes:

```
application/
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container orchestration
├── .dockerignore          # Files to exclude from build
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (create this)
```

## 🎯 Best Practices

1. **Always use `.env` files** for sensitive data
2. **Check container health** before accessing applications
3. **Use development configurations** for debugging
4. **Monitor resource usage** with `docker stats`
5. **Clean up unused containers** regularly

## 🔄 Updates

To update applications:

1. Pull latest code
2. Rebuild containers:
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

## 📞 Support

If you encounter issues:

1. Check the application-specific README files
2. Review Docker logs: `docker-compose logs -f`
3. Verify environment variables are set correctly
4. Ensure Docker and Docker Compose are up to date 