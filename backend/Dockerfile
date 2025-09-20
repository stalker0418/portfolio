# Step 1: Choose base image - Python 3.11 slim (smaller size, good for production)
FROM python:3.11-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Step 4: Install system dependencies (gcc needed for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy dependency files first (for Docker layer caching)
COPY pyproject.toml uv.lock* ./

# Step 6: Install Python dependencies
# We use uv for faster package installation
RUN pip install --upgrade pip && \
    pip install uv && \
    uv pip install --system -r pyproject.toml

# Step 7: Copy application code
COPY . .

# Step 8: Create non-root user for security (best practice)
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Step 9: Expose port 8000 (your FastAPI app port)
EXPOSE 8000

# Step 10: Add health check for Fly.io monitoring
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Step 11: Run command - start your FastAPI app
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
