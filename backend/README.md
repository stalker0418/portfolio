# Portfolio Backend

FastAPI backend with AI-powered RAG chatbot for the portfolio website.

## 🚀 Quick Start with uv

### Install uv (if not already installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Setup and Run
```bash
# Install dependencies
uv sync

# Run the development server
uv run run.py

# Or use the direct uvicorn command
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 📦 Package Management with uv

### Adding Dependencies
```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev pytest

# Add with version constraint
uv add "fastapi>=0.100.0"
```

### Removing Dependencies
```bash
uv remove package-name
```

### Updating Dependencies
```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add package-name --upgrade
```

### Running Scripts
```bash
# Run Python with the project environment
uv run python script.py

# Run any command in the project environment
uv run pytest
uv run black .
uv run mypy .
```

## 🔧 Development Commands

```bash
# Install all dependencies (including dev)
uv sync

# Run the server in development mode
uv run run.py

# Run tests (when added)
uv run pytest

# Format code
uv run black .

# Type checking
uv run mypy .

# Start a Python REPL with project dependencies
uv run python
```

## 📁 Project Structure

```
backend/
├── pyproject.toml      # uv project configuration
├── uv.lock            # Lock file (auto-generated)
├── main.py            # FastAPI application
├── run.py             # Development server runner
├── chatbot/           # RAG chatbot module
│   ├── __init__.py
│   └── rag_system.py  # RAG implementation
├── .env               # Environment variables
└── README.md          # This file
```

## 🌟 Benefits of uv

- **Faster**: 10-100x faster than pip
- **Reliable**: Consistent dependency resolution
- **Modern**: Built-in virtual environment management
- **Simple**: Single tool for all Python package management
- **Compatible**: Works with existing pip/poetry projects

## 🔑 Environment Variables

Create a `.env` file:
```bash
# Optional: OpenAI API key for enhanced RAG capabilities
OPENAI_API_KEY=your_openai_api_key_here

# Server configuration
DEBUG=True
HOST=127.0.0.1
PORT=8000

# CORS settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📚 API Documentation

When running, visit:
- **Interactive docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
