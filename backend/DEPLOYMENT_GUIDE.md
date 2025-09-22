# Deployment Guide for Portfolio Backend with RAG System

## Overview

This guide explains how to deploy the portfolio backend with the integrated RAG system to Fly.io. The deployment process now automatically updates the vector database with the latest resources during each deployment.

## Prerequisites

1. **Fly.io CLI installed**: [Install flyctl](https://fly.io/docs/hands-on/install-flyctl/)
2. **Fly.io account**: [Sign up for free](https://fly.io/app/sign-up)
3. **Together AI API key**: [Get API key](https://api.together.xyz/)

## Initial Setup

### 1. Create Fly.io App (First Time Only)

```bash
# Navigate to backend directory
cd backend

# Create the app (this will use settings from fly.toml)
flyctl apps create manas-portfolio-backend
```

### 2. Create Persistent Volume for Vector Database (First Time Only)

```bash
# Create a 1GB volume for the vector database
flyctl volumes create portfolio_vector_db --region ord --size 1

# Verify volume was created
flyctl volumes list
```

### 3. Set Environment Variables (First Time Only)

```bash
# Set your Together AI API key (required)
flyctl secrets set TOGETHER_API_KEY="your_together_api_key_here"

# Optional: Set other API keys if you plan to use them
flyctl secrets set OPENAI_API_KEY="your_openai_api_key_here"
flyctl secrets set ANTHROPIC_API_KEY="your_anthropic_api_key_here"
```

## Deployment Process

### Standard Deployment (Recommended)

This will automatically update the RAG database during deployment:

```bash
# Deploy with RAG database update
flyctl deploy

# Monitor deployment logs
flyctl logs
```

### Quick Deployment (Skip RAG Update)

If you want to deploy quickly without updating the RAG database:

```bash
# Set environment variable to skip RAG update
flyctl secrets set SKIP_RAG_UPDATE="true"

# Deploy
flyctl deploy

# Don't forget to re-enable RAG updates for future deployments
flyctl secrets unset SKIP_RAG_UPDATE
```

### Manual RAG Database Update

If you need to update the RAG database without redeploying:

```bash
# Use the API endpoint
curl -X POST https://manas-portfolio-backend.fly.dev/rag/update

# Or connect to the running instance and run the script
flyctl ssh console
python update_rag_database.py --verbose --stats
```

## Deployment Flow

When you run `flyctl deploy`, here's what happens:

1. **Docker Build**: 
   - Installs system dependencies (Tesseract OCR, Poppler)
   - Installs Python dependencies including RAG system packages
   - Copies your application code and resources

2. **Container Startup**:
   - Runs `startup.py` script
   - **RAG Database Update**: Automatically processes all resources:
     - Extracts text from your resume PDF using OCR
     - Scrapes information from GitHub, LinkedIn, Medium links
     - Generates embeddings and stores in ChromaDB
     - Creates searchable vector database
   - **Server Start**: Launches FastAPI application

3. **Health Checks**: Fly.io monitors the `/health` endpoint

## Monitoring and Troubleshooting

### View Deployment Logs

```bash
# View recent logs
flyctl logs

# Follow logs in real-time
flyctl logs -f

# View logs from a specific time
flyctl logs --since="1h"
```

### Check RAG Database Status

```bash
# Get database statistics
curl https://manas-portfolio-backend.fly.dev/rag/stats

# Or using the API
curl https://manas-portfolio-backend.fly.dev/health
```

### Debug RAG System

```bash
# Connect to running instance
flyctl ssh console

# Run RAG system test
python test_rag.py

# Check vector database
ls -la /app/vector_db/

# View resource files
ls -la /app/resources/
```

### Common Issues and Solutions

#### 1. RAG Database Update Fails

**Symptoms**: Logs show "RAG database update failed"

**Solutions**:
```bash
# Check if resources directory exists
flyctl ssh console
ls -la /app/resources/

# Manually update database
python update_rag_database.py --verbose

# Check OCR dependencies
tesseract --version
```

#### 2. Volume Mount Issues

**Symptoms**: "Permission denied" or database not persisting

**Solutions**:
```bash
# Check volume status
flyctl volumes list

# Verify mount point
flyctl ssh console
ls -la /app/vector_db/
df -h /app/vector_db/
```

#### 3. OCR Processing Fails

**Symptoms**: "OCR extraction failed" in logs

**Solutions**:
```bash
# Check Tesseract installation
flyctl ssh console
tesseract --version
tesseract --list-langs

# Test PDF processing
python -c "from rag_system import ResourceProcessor; rp = ResourceProcessor(); print('OCR dependencies OK')"
```

#### 4. Memory Issues

**Symptoms**: App crashes during RAG update

**Solutions**:
```bash
# Temporarily increase memory for deployment
flyctl scale memory 512

# After deployment, scale back down
flyctl scale memory 256

# Or skip RAG update during deployment and update manually later
flyctl secrets set SKIP_RAG_UPDATE="true"
flyctl deploy
flyctl secrets unset SKIP_RAG_UPDATE
curl -X POST https://manas-portfolio-backend.fly.dev/rag/update
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TOGETHER_API_KEY` | Together AI API key | - | Yes |
| `OPENAI_API_KEY` | OpenAI API key | - | No |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | No |
| `SKIP_RAG_UPDATE` | Skip RAG update on startup | `false` | No |
| `ENABLE_RAG` | Enable RAG system | `true` | No |
| `VECTOR_DB_PATH` | Vector database path | `/app/vector_db` | No |
| `RESOURCES_DIR` | Resources directory | `/app/resources` | No |

## Resource Management

### Adding New Resources

1. **Update resources.yaml**:
   ```yaml
   resources:
     projects:
       github_repos:
         - url: "https://github.com/manassanjay/new-project"
           description: "New project description"
           type: "project"
   ```

2. **Deploy with automatic RAG update**:
   ```bash
   flyctl deploy
   ```

3. **Verify update**:
   ```bash
   curl https://manas-portfolio-backend.fly.dev/rag/stats
   ```

### Updating Resume

1. **Replace PDF file**: Update `resources/Manas_Sanjay_Pakalapati_Resume.pdf`

2. **Deploy**: The OCR system will automatically extract text from the new PDF

3. **Test**: Ask the chatbot about your updated information

## Performance Optimization

### Reduce Deployment Time

- Use `SKIP_RAG_UPDATE=true` for code-only changes
- Update RAG database separately using API endpoint

### Optimize Memory Usage

- RAG update requires more memory temporarily
- Consider scaling up during deployment, then scaling down

### Monitor Database Size

```bash
# Check database size
flyctl ssh console
du -sh /app/vector_db/
```

## Security Considerations

1. **API Keys**: Always use `flyctl secrets set` for API keys
2. **Volume Security**: Vector database is isolated per app
3. **HTTPS**: All traffic is automatically encrypted
4. **Resource Access**: Only public resources are processed

## Backup and Recovery

### Backup Vector Database

```bash
# Create backup
flyctl ssh console
tar -czf vector_db_backup.tar.gz /app/vector_db/

# Download backup (from local machine)
flyctl ssh sftp get vector_db_backup.tar.gz
```

### Restore from Backup

```bash
# Upload backup
flyctl ssh sftp put vector_db_backup.tar.gz

# Restore
flyctl ssh console
tar -xzf vector_db_backup.tar.gz -C /app/
```

### Force Database Rebuild

```bash
# Option 1: Use API endpoint
curl -X POST https://manas-portfolio-backend.fly.dev/rag/update

# Option 2: Use command line script
flyctl ssh console
python update_rag_database.py --force --verbose
```

## Cost Optimization

The deployment is optimized for Fly.io's free tier:

- **Auto-stop/start**: Machines stop when idle
- **Minimal memory**: 256MB base allocation
- **Shared CPU**: Uses free tier resources
- **Persistent volume**: 1GB for vector database

**Estimated costs** (beyond free tier):
- Volume storage: ~$0.15/GB/month
- Additional compute: Only when scaling beyond free tier

## Next Steps

1. **Monitor Performance**: Use Fly.io metrics dashboard
2. **Set up Alerts**: Configure alerts for app health
3. **Optimize Resources**: Adjust based on usage patterns
4. **Scale as Needed**: Increase resources for production load

## Support

- **Fly.io Docs**: https://fly.io/docs/
- **Fly.io Community**: https://community.fly.io/
- **RAG System Issues**: Check logs and use test scripts
- **API Documentation**: Visit `/docs` endpoint on your deployed app
