# Portfolio Backend

Simple FastAPI backend for Manas's portfolio with AI chatbot functionality.

## Features

- Health check endpoint
- AI chatbot with multi-provider support (OpenAI, Anthropic, TogetherAI)
- Chat endpoint connected to frontend interface
- CORS enabled for frontend communication

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Set up environment variables (copy from env.example):
```bash
cp env.example .env
```

3. Run the server:
```bash
python run.py
```

The server will start on http://localhost:8000

## API Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health status check
- `POST /chat` - Chat with AI chatbot
- `GET /docs` - Interactive API documentation (Swagger UI)

## Current Status

- ✅ Health endpoint
- ✅ Chat endpoint structure
- ✅ Chatbot wrapper class
- 🔄 TogetherAI integration (placeholder - ready for implementation)
- ⏳ OpenAI integration (TODO)
- ⏳ Anthropic integration (TODO)