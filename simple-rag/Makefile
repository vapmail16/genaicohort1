# Makefile for Simple RAG Application

.PHONY: help build up down logs clean ingest shell restart

# Default target
help:
	@echo "Simple RAG Application - Docker Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - View logs from all services"
	@echo "  clean     - Stop services and remove volumes"
	@echo "  ingest    - Run document ingestion"
	@echo "  shell     - Open shell in RAG app container"
	@echo "  restart   - Restart all services"
	@echo "  status    - Show service status"

# Build Docker images
build:
	@echo "Building Docker images..."
	docker-compose -f docker/docker-compose.yml build

# Start all services
up:
	@echo "Starting services..."
	docker-compose -f docker/docker-compose.yml up -d

# Stop all services
down:
	@echo "Stopping services..."
	docker-compose -f docker/docker-compose.yml down

# View logs
logs:
	@echo "Viewing logs..."
	docker-compose -f docker/docker-compose.yml logs -f

# Clean up (stop and remove volumes)
clean:
	@echo "Cleaning up..."
	docker-compose -f docker/docker-compose.yml down -v
	docker system prune -f

# Run document ingestion
ingest:
	@echo "Running document ingestion..."
	docker-compose -f docker/docker-compose.yml exec rag-app python docker/docker-ingest.py

# Open shell in RAG app container
shell:
	@echo "Opening shell in RAG app container..."
	docker-compose -f docker/docker-compose.yml exec rag-app bash

# Restart all services
restart:
	@echo "Restarting services..."
	docker-compose -f docker/docker-compose.yml restart

# Show service status
status:
	@echo "Service status:"
	docker-compose -f docker/docker-compose.yml ps

# Quick start (build and up)
start: build up
	@echo "Services started! Access the app at http://localhost:8501"

# Development mode (with volume mounts for hot reload)
dev:
	@echo "Starting in development mode..."
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d

# Production mode
prod:
	@echo "Starting in production mode..."
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d 