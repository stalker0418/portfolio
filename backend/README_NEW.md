# Portfolio Backend - Restructured

A modern, modular FastAPI backend for Manas Sanjay's portfolio with AI-powered chatbot capabilities.

## 🏗️ Architecture

The backend follows industrial coding practices with a clean, modular architecture:

```
backend/
├── src/
│   └── portfolio/
│       ├── api/           # API endpoints
│       ├── core/          # Core business logic
│       ├── models/        # Pydantic data models
│       ├── services/      # Service layer
│       └── utils/         # Utility functions
├── config/               # Configuration management
├── resources/            # Portfolio resources
├── tests/               # Test files
└── pyproject.toml       # Project configuration
```

## 🚀 Features

### Multi-Model AI Support
- **TogetherAI**: Primary model provider (Llama-2-7b-chat-hf)
- **OpenAI**: GPT-3.5-turbo support
- **Anthropic**: Claude-3-sonnet support
- Easy model switching via configuration

### Resource Management
- YAML-based resource configuration
- PDF resume support
- Social media profile integration
- Project links management
- Extensible resource types

### Modern API Design
- FastAPI with automatic OpenAPI documentation
- Pydantic models for data validation
- Async/await support throughout
- Comprehensive error handling
- Health check endpoints

## 📦 Installation

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application:**
   ```bash
   python run_new.py
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_MODEL` | Primary AI model provider | `together` |
| `TOGETHER_API_KEY` | TogetherAI API key | Required |
| `OPENAI_API_KEY` | OpenAI API key | Optional |
| `ANTHROPIC_API_KEY` | Anthropic API key | Optional |
| `MODEL_TEMPERATURE` | AI model temperature | `0.7` |
| `MODEL_MAX_TOKENS` | Maximum response tokens | `1000` |

### Resource Configuration

Edit `resources/resources.yaml` to manage portfolio resources:

```yaml
resources:
  resume:
    type: "pdf"
    path: "Manas_Sanjay_Pakalapati_Resume.pdf"
    description: "Professional resume and CV"
  
  profiles:
    linkedin:
      url: "https://linkedin.com/in/manas-sanjay-pakalapati"
      description: "LinkedIn professional profile"
      type: "social"
```

## 🛠️ API Endpoints

### Chat Endpoints
- `POST /api/chat/` - Chat with the AI assistant
- `GET /api/chat/summary` - Get portfolio summary

### Health Endpoints
- `GET /` - Basic health check
- `GET /health` - Detailed health check

## 🔄 Migration from Old Structure

The old `chatbot/` directory and `main.py` have been replaced with the new modular structure. To migrate:

1. **Update your .env file** with new variable names
2. **Use the new run script:** `python run_new.py`
3. **Update frontend API calls** if needed (endpoints remain the same)

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

## 📈 Scaling

The modular architecture supports easy scaling:

1. **Add new AI providers** in `services/ai_models.py`
2. **Add new resource types** in `models/resources.py`
3. **Add new API endpoints** in `api/` directory
4. **Extend configuration** in `config/settings.py`

## 🔒 Security

- API keys stored in environment variables
- CORS properly configured
- Input validation with Pydantic
- Error handling without sensitive data exposure

## 📝 Development

### Adding New AI Providers

1. Create a new provider class inheriting from `AIModelProvider`
2. Implement required methods: `initialize()`, `generate_response()`, `close()`
3. Add provider to `AIModelService.initialize()`

### Adding New Resource Types

1. Add new type to `ResourceType` enum in `models/resources.py`
2. Update `ResourceManager._parse_config()` to handle the new type
3. Add parsing logic for the new resource structure

## 🚀 Deployment

The application is ready for deployment on:
- **Vercel** (with serverless functions)
- **Railway** (containerized)
- **AWS/GCP/Azure** (containerized)
- **Docker** (with provided Dockerfile)

## 📊 Monitoring

- Health check endpoints for uptime monitoring
- Structured logging for debugging
- Performance metrics in API responses
- Error tracking and reporting
