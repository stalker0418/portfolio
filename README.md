# Manas Sanjay - AI Portfolio

An intelligent portfolio website built with React and FastAPI, featuring an AI-powered chatbot that can answer questions about my experience, skills, and projects using RAG (Retrieval Augmented Generation) technology.

## 🚀 Features

- **Modern React Frontend** with smooth animations using Framer Motion
- **AI-Powered Chatbot** with RAG capabilities for intelligent responses
- **Responsive Design** that works on all devices
- **FastAPI Backend** for high-performance API endpoints
- **Real-time Chat** with streaming responses
- **Professional UI** inspired by modern portfolio designs

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Query** for API state management
- **Lucide React** for icons

### Backend
- **FastAPI** for high-performance APIs
- **LangChain** for RAG implementation
- **OpenAI API** for language model
- **ChromaDB** for vector storage
- **Pydantic** for data validation

## 📦 Installation

### Prerequisites
- Node.js 16+ 
- Python 3.9+
- uv package manager ([install here](https://docs.astral.sh/uv/getting-started/installation/))
- OpenAI API key (optional, fallback responses available)

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend

# Install uv if you haven't already
# curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies using uv
uv sync

# Optional: Add your OpenAI API key to .env file
# OPENAI_API_KEY=your_key_here

# Run the server
uv run run.py
```

## 🎯 Usage

1. **Start the backend server**: `cd backend && uv run run.py`
2. **Start the frontend**: `cd frontend && npm start`
3. **Open your browser** to `http://localhost:3000`
4. **Chat with the AI assistant** using the chat bubble in the bottom right

## 🤖 AI Chatbot Features

The AI assistant can help visitors learn about:
- Technical skills and expertise
- Project details and achievements
- Professional experience
- Educational background
- Contact information

The chatbot uses RAG technology to provide accurate, context-aware responses based on portfolio data.

## 🔧 Configuration

### Environment Variables (Backend)
- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `DEBUG`: Enable debug mode (default: True)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 8000)

## 📚 API Documentation

When running the backend, visit:
- **Interactive docs**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🎨 Customization

### Adding Your Information
1. Update `backend/chatbot/rag_system.py` with your personal information
2. Modify the portfolio data in the `portfolio_data` dictionary
3. Customize the frontend components with your details

### Styling
- Modify `frontend/tailwind.config.js` for custom colors and themes
- Update component styles in the respective `.tsx` files
- Add custom animations in `frontend/src/index.css`

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy the build folder
```

### Backend (Railway/Heroku/AWS)
```bash
cd backend
# Set environment variables in your deployment platform
# Deploy with the provided Dockerfile or requirements.txt
```

## 🤝 Contributing

Feel free to fork this project and customize it for your own portfolio! If you have suggestions for improvements, please open an issue or submit a pull request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact

- **Email**: manas.sanjay@example.com
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/your-profile)
- **GitHub**: [Your GitHub](https://github.com/your-username)

---

Built with ❤️ using React, FastAPI, and AI technologies.
