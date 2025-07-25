# 🛠️ Docker Management Scripts

This directory contains scripts for managing all Docker applications in the repository.

## 📋 Available Scripts

### 🚀 `run_all_docker.sh`
Launches all applications on different ports to avoid conflicts.

**Usage:**
```bash
./scripts/run_all_docker.sh
```

**Features:**
- Automatically assigns different ports for each application
- Creates .env files if they don't exist
- Checks port availability before starting
- Provides status updates and URLs

### 🛑 `stop_all_docker.sh`
Stops all Docker applications cleanly.

**Usage:**
```bash
./scripts/stop_all_docker.sh
```

**Features:**
- Stops all running containers
- Cleans up any remaining containers
- Provides cleanup instructions

### 🔍 `verify_docker_setup.sh`
Validates Docker configurations and setup.

**Usage:**
```bash
./scripts/verify_docker_setup.sh
```

**Features:**
- Checks Docker installation
- Validates Dockerfile syntax
- Verifies docker-compose configurations
- Reports missing files

### 🚀 `quick_start.sh`
Guided setup process for Docker applications.

**Usage:**
```bash
./scripts/quick_start.sh
```

**Features:**
- Step-by-step setup guide
- Creates .env file templates
- Verifies Docker setup
- Provides next steps

## 📱 Application URLs (when running all)

- **Simple RAG**: http://localhost:8501
- **Simple Agent**: http://localhost:8502
- **Simple Chatbot**: http://localhost:8503
- **Simple RAG Fork**: http://localhost:8504
- **Project Scaffold**: Check logs for output

## 🔧 Prerequisites

- Docker installed and running
- Docker Compose installed
- Environment variables configured (see individual project READMEs)

## 📖 Documentation

For detailed setup instructions, see:
- `../docs/DOCKER_SETUP_GUIDE.md` - Comprehensive setup guide
- `../docs/DOCKER_READY_SUMMARY.md` - Complete status summary 