# Docker Setup Guide for Simple RAG Application

This guide explains how to run the Simple RAG application using Docker and Docker Compose.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system
- OpenAI API key (for LLM functionality)

## Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd simple-rag
```

### 2. Set Environment Variables
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Add Documents
Place your PDF documents in the `data/` directory:
```bash
mkdir -p data
cp your_documents.pdf data/
```

### 4. Run with Docker Compose
```bash
docker-compose up -d
```

### 5. Access the Application
- **Streamlit App**: http://localhost:8501
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## Docker Services

### 1. Qdrant Vector Database
- **Image**: `qdrant/qdrant:latest`
- **Ports**: 6333 (HTTP), 6334 (gRPC)
- **Storage**: Persistent volume for vector data
- **Health Check**: Automatic health monitoring

### 2. RAG Application
- **Base Image**: Python 3.11-slim
- **Port**: 8501 (Streamlit)
- **Features**: Document ingestion, vector search, LLM integration
- **Dependencies**: Automatically waits for Qdrant to be healthy

## Docker Commands

### Build and Start Services
```bash
# Build and start all services
docker-compose up -d

# Build and start with logs
docker-compose up --build

# Start specific service
docker-compose up -d rag-app
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f rag-app
docker-compose logs -f qdrant
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Rebuild Services
```bash
# Rebuild specific service
docker-compose build rag-app

# Rebuild and restart
docker-compose up --build -d
```

## Development Workflow

### 1. Local Development
For development, you can mount the source code as a volume:

```yaml
# In docker-compose.yml, add to rag-app service:
volumes:
  - ./data:/app/data
  - ./qdrant_storage:/app/qdrant_storage
  - .:/app  # Mount source code for development
```

### 2. Hot Reload
The Streamlit app supports hot reload. Changes to your Python files will automatically restart the application.

### 3. Debugging
```bash
# Access container shell
docker-compose exec rag-app bash

# View container logs
docker-compose logs rag-app

# Check service health
docker-compose ps
```

## Data Persistence

### Qdrant Storage
- Vector data is stored in a Docker volume: `qdrant_storage`
- Data persists between container restarts
- To reset data: `docker-compose down -v`

### Document Storage
- Documents in `./data` are mounted to `/app/data` in the container
- Add new documents to the `data/` directory and restart the ingestion

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key for LLM functionality |
| `QDRANT_HOST` | `qdrant` | Qdrant service hostname |
| `QDRANT_PORT` | `6333` | Qdrant service port |
| `COLLECTION_NAME` | `documents` | Vector collection name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `CHUNK_SIZE` | `1000` | Document chunk size |
| `CHUNK_OVERLAP` | `200` | Document chunk overlap |

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8501
   lsof -i :6333
   
   # Stop conflicting services
   docker-compose down
   ```

2. **Qdrant Connection Issues**
   ```bash
   # Check Qdrant health
   curl http://localhost:6333/health
   
   # View Qdrant logs
   docker-compose logs qdrant
   ```

3. **Memory Issues**
   ```bash
   # Check container resource usage
   docker stats
   
   # Increase memory limits in docker-compose.yml
   ```

4. **Build Failures**
   ```bash
   # Clean build cache
   docker-compose build --no-cache
   
   # Remove all containers and images
   docker system prune -a
   ```

### Performance Optimization

1. **Use .dockerignore**: Excludes unnecessary files from build context
2. **Multi-stage builds**: Consider for production deployments
3. **Resource limits**: Set appropriate CPU/memory limits
4. **Volume optimization**: Use named volumes for better performance

## Production Deployment

### Security Considerations
- Use secrets management for API keys
- Implement proper network security
- Use non-root user in containers
- Regular security updates

### Scaling
- Use Docker Swarm or Kubernetes for orchestration
- Implement load balancing
- Use external databases for production

### Monitoring
- Implement health checks
- Use logging aggregation
- Monitor resource usage
- Set up alerts

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review container logs
3. Verify environment variables
4. Check Docker and Docker Compose versions 