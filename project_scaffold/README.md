# 🏗️ Project Scaffold

A comprehensive Python project template with built-in diagnostics, database connectivity checks, API monitoring, and Docker status verification. This scaffold provides a solid foundation for building robust Python applications with modern development practices.

## 🎯 Overview

The Project Scaffold is designed to accelerate development by providing:

- **Comprehensive Diagnostics**: Health checks for your development environment
- **Modern Tooling**: Poetry for dependency management, Make for automation
- **Monitoring Capabilities**: API status, database connectivity, Docker health
- **Best Practices**: Type checking, linting, formatting, and testing setup
- **Docker Support**: Containerization ready with Dockerfile
- **Documentation**: Structured documentation and configuration management

## 📁 Project Structure

```
project_scaffold/
└── my_project/
    ├── README.md              # Detailed project documentation
    ├── diagnostics.py         # Comprehensive health check script
    ├── pyproject.toml         # Poetry configuration and dependencies
    ├── makefile              # Development automation commands
    ├── Dockerfile            # Container configuration
    ├── .env.example          # Environment variables template
    ├── .gitignore            # Git ignore patterns
    ├── src/                  # Source code directory
    │   └── my_project/
    │       ├── __init__.py
    │       └── main.py       # Main application entry point
    ├── tests/                # Test cases and test utilities
    ├── configs/              # Configuration files
    ├── scripts/              # Utility and automation scripts
    ├── docs/                 # Documentation files
    └── data/                 # Data files and databases
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Poetry (for dependency management)
- Docker (optional, for containerization)

### Installation

1. **Navigate to the project directory**
   ```bash
   cd project_scaffold/my_project
   ```

2. **Install Poetry (if not already installed)**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values, especially OPENAI_API_KEY
   ```

5. **Run diagnostics**
   ```bash
   poetry run python diagnostics.py
   ```

## 🛠️ Features

### 🔍 Comprehensive Diagnostics
The `diagnostics.py` script performs extensive health checks:

- **System Resources**: CPU, memory, disk usage monitoring
- **Database Connectivity**: Test connections to various database systems
- **External API Status**: Check OpenAI, GitHub, and other API endpoints
- **Docker Integration**: Verify Docker daemon status and container health
- **Environment Validation**: Validate required environment variables
- **Python Environment**: Check Python version, dependencies, and virtual environment

### 📦 Modern Dependency Management
- **Poetry**: Modern Python dependency management with lock files
- **Virtual Environments**: Automatic virtual environment creation
- **Dependency Resolution**: Smart dependency resolution and conflict handling

### 🔧 Development Automation
The `makefile` provides convenient commands for development:

```bash
make install    # Install dependencies
make test       # Run tests
make lint       # Run linting with flake8
make format     # Format code with Black
make check      # Run type checking with MyPy
make run        # Run the main application
make clean      # Clean Poetry environment
make build      # Build the package
make publish    # Publish the package
```

### 🐳 Docker Support
- **Dockerfile**: Ready-to-use container configuration
- **Multi-stage Builds**: Optimized for production deployment
- **Health Checks**: Built-in container health monitoring

## 📋 Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
DEBUG=true
DATABASE_URL=your_database_connection_string
API_BASE_URL=https://api.example.com
LOG_LEVEL=INFO
```

### Poetry Configuration
The `pyproject.toml` file contains:

- **Project Metadata**: Name, version, description, authors
- **Dependencies**: Runtime and development dependencies
- **Build Configuration**: Package build settings
- **Tool Configuration**: Black, MyPy, and other tool settings

## 🔧 Development Workflow

### 1. Initial Setup
```bash
cd project_scaffold/my_project
poetry install
cp .env.example .env
# Edit .env with your values
poetry run python diagnostics.py
```

### 2. Development
```bash
# Start development
poetry run make run

# Run tests
poetry run make test

# Check code quality
poetry run make lint
poetry run make format
poetry run make check
```

### 3. Building and Deployment
```bash
# Build package
poetry run make build

# Build Docker image
docker build -t my-project .

# Run in Docker
docker run -p 8000:8000 my-project
```

## 📊 Diagnostics Output

The diagnostics script provides detailed information about:

### System Health
- CPU usage and load average
- Memory usage and availability
- Disk space and I/O statistics
- Network connectivity

### Development Environment
- Python version and environment
- Installed packages and versions
- Virtual environment status
- Poetry configuration

### External Services
- Database connectivity status
- API endpoint availability
- Docker daemon status
- Environment variable validation

### Example Output
```
🔍 System Diagnostics Report
============================

✅ System Resources
   CPU Usage: 15.2%
   Memory Usage: 2.1GB / 8.0GB (26.3%)
   Disk Usage: 45.2GB / 500GB (9.0%)

✅ Python Environment
   Python Version: 3.9.7
   Virtual Environment: Active
   Poetry Version: 1.4.0

✅ External Services
   OpenAI API: ✅ Connected
   GitHub API: ✅ Connected
   Database: ✅ Connected

✅ Environment Variables
   OPENAI_API_KEY: ✅ Set
   DEBUG: ✅ Set (true)
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
poetry run make test

# Run specific test file
poetry run pytest tests/test_specific.py

# Run with coverage
poetry run pytest --cov=src/my_project tests/
```

### Test Structure
```
tests/
├── __init__.py
├── conftest.py          # Pytest configuration
├── test_main.py         # Main application tests
├── test_diagnostics.py  # Diagnostics tests
└── fixtures/            # Test data and fixtures
```

## 📚 Documentation

### Code Documentation
- **Docstrings**: Comprehensive function and class documentation
- **Type Hints**: Full type annotation support
- **Comments**: Inline code documentation

### Project Documentation
- **README.md**: Project overview and setup instructions
- **docs/**: Detailed documentation and guides
- **API Documentation**: Auto-generated API docs

## 🔒 Security

### Best Practices
- **Environment Variables**: Sensitive data stored in environment variables
- **Dependency Scanning**: Regular security updates for dependencies
- **Input Validation**: Comprehensive input validation and sanitization
- **Error Handling**: Secure error handling without information leakage

### Security Features
- **API Key Management**: Secure API key handling
- **Database Security**: Connection string encryption
- **Container Security**: Non-root user in Docker containers

## 🚀 Deployment

### Local Development
```bash
poetry run make run
```

### Docker Deployment
```bash
# Build image
docker build -t my-project .

# Run container
docker run -d -p 8000:8000 --env-file .env my-project
```

### Cloud Deployment
The project is ready for deployment to:
- **AWS**: ECS, Lambda, or EC2
- **Google Cloud**: Cloud Run or Compute Engine
- **Azure**: Container Instances or App Service
- **Heroku**: Direct deployment with Procfile

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 and use Black for formatting
2. **Type Hints**: Use type annotations for all functions
3. **Testing**: Write tests for new features
4. **Documentation**: Update documentation for changes
5. **Commits**: Use conventional commit messages

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**Poetry Installation Issues**
```bash
# Clear Poetry cache
poetry cache clear --all pypi

# Reinstall dependencies
poetry install --sync
```

**Docker Issues**
```bash
# Check Docker daemon
docker info

# Clean up containers
docker system prune -a
```

**Environment Issues**
```bash
# Verify environment variables
poetry run python -c "import os; print(os.getenv('OPENAI_API_KEY'))"

# Check Poetry environment
poetry env info
```

### Getting Help
- Check the diagnostics output for system issues
- Review the logs for detailed error information
- Ensure all prerequisites are properly installed
- Verify environment variables are correctly set

## 🙏 Acknowledgments

- **Poetry** for modern Python dependency management
- **Pytest** for comprehensive testing framework
- **Black** for code formatting
- **MyPy** for static type checking
- **Docker** for containerization support

---

**Happy Development! 🚀✨**

*This scaffold provides a solid foundation for building robust, maintainable Python applications with modern development practices and comprehensive monitoring capabilities.* 