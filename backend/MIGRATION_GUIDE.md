# Migration Guide: Old to New Backend Structure

## 🎯 What We've Accomplished

✅ **Complete Backend Restructuring** following industrial coding practices
✅ **Multi-Model AI Support** (TogetherAI, OpenAI, Anthropic)
✅ **Resource Management System** with YAML configuration
✅ **Modular Architecture** for easy scaling
✅ **Proper Package Structure** with `__init__.py` files
✅ **Configuration Management** with environment variables
✅ **Comprehensive Testing** setup

## 📁 New Project Structure

```
backend/
├── src/portfolio/           # Main application package
│   ├── api/                # API endpoints (chat, health)
│   ├── models/             # Pydantic data models
│   ├── services/           # Business logic services
│   └── utils/              # Utility functions
├── config/                 # Configuration management
├── resources/              # Portfolio resources & config
├── tests/                  # Test files
├── src/main.py            # New main application
├── run_new.py             # New run script
└── pyproject.toml         # Updated dependencies
```

## 🔄 Migration Steps

### 1. Environment Setup
```bash
cd backend
cp env.example .env
# Edit .env with your TogetherAI API key
```

### 2. Install Dependencies
```bash
pip install -e .
```

### 3. Test the New Structure
```bash
# Run tests
pytest tests/

# Start the new server
python run_new.py
```

### 4. Verify API Endpoints
```bash
# Health check
curl http://localhost:8000/

# Chat endpoint
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Manas"}'
```

## 🆕 New Features

### Multi-Model AI Support
- **TogetherAI**: Primary model (Llama-2-7b-chat-hf)
- **OpenAI**: GPT-3.5-turbo support
- **Anthropic**: Claude-3-sonnet support
- Easy switching via `DEFAULT_MODEL` environment variable

### Resource Management
- YAML-based configuration in `resources/resources.yaml`
- PDF resume support
- Social media profiles (LinkedIn, GitHub, Medium)
- Project links management
- Extensible for future resource types

### Enhanced API
- Same endpoints as before (backward compatible)
- Additional response fields (model_used, processing_time)
- Better error handling
- Comprehensive health checks

## 🔧 Configuration

### Environment Variables (.env)
```bash
# AI Model Configuration
DEFAULT_MODEL="together"
TOGETHER_API_KEY="your_api_key_here"
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=1000

# Server Configuration
HOST="0.0.0.0"
PORT=8000
DEBUG=true
```

### Resource Configuration (resources/resources.yaml)
```yaml
resources:
  resume:
    type: "pdf"
    path: "Manas_Sanjay_Pakalapati_Resume.pdf"
    description: "Professional resume"
  
  profiles:
    linkedin:
      url: "https://linkedin.com/in/manas-sanjay-pakalapati"
      type: "social"
      description: "LinkedIn profile"
```

## 🚀 Next Steps

1. **Add your TogetherAI API key** to `.env`
2. **Test the new structure** with `python run_new.py`
3. **Update frontend** if needed (API endpoints remain the same)
4. **Add more resources** to `resources/resources.yaml`
5. **Deploy** using the new structure

## 🔍 Troubleshooting

### Import Issues
If you get import errors, make sure you're running from the backend directory:
```bash
cd backend
python run_new.py
```

### Missing Dependencies
Install all dependencies:
```bash
pip install -e .
```

### API Key Issues
Make sure your `.env` file has the correct API key:
```bash
TOGETHER_API_KEY="your_actual_api_key_here"
```

## 📊 Benefits of New Structure

1. **Scalability**: Easy to add new AI models and features
2. **Maintainability**: Clear separation of concerns
3. **Testability**: Comprehensive test coverage
4. **Configuration**: Centralized configuration management
5. **Documentation**: Self-documenting code with type hints
6. **Industry Standards**: Follows Python packaging best practices

The new structure is production-ready and follows all modern Python development practices!
