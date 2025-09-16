import os
import asyncio
from typing import Dict, List, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import chromadb
from chromadb.config import Settings

class RAGChatbot:
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        self.is_initialized = False
        
        # Portfolio data - This would typically come from your resume/database
        self.portfolio_data = {
            "personal_info": {
                "name": "Manas Sanjay Pakalapati",
                "title": "AI Engineer & Full-Stack Developer",
                "email": "manas.sanjay@example.com",
                "location": "San Francisco, CA",
                "summary": "Passionate AI Engineer and Full-Stack Developer with expertise in building intelligent systems and scalable web applications."
            },
            "skills": {
                "ai_ml": ["Python", "TensorFlow", "PyTorch", "LangChain", "OpenAI API", "Hugging Face", "RAG Systems", "Vector Databases"],
                "frontend": ["React", "TypeScript", "Next.js", "Tailwind CSS", "Framer Motion", "Redux"],
                "backend": ["FastAPI", "Node.js", "Express.js", "PostgreSQL", "MongoDB", "Redis"],
                "tools": ["Git", "Docker", "AWS", "Linux", "Kubernetes", "CI/CD"]
            },
            "projects": [
                {
                    "name": "AI-Powered Portfolio",
                    "description": "An intelligent portfolio website with integrated chatbot using RAG technology for answering questions about experience and projects.",
                    "technologies": ["React", "TypeScript", "FastAPI", "LangChain", "OpenAI"],
                    "highlights": ["RAG implementation", "Real-time chat", "Responsive design"]
                },
                {
                    "name": "E-Commerce Platform",
                    "description": "Full-stack e-commerce solution with modern UI, payment integration, and admin dashboard.",
                    "technologies": ["Next.js", "Node.js", "MongoDB", "Stripe", "Tailwind"],
                    "highlights": ["Payment processing", "Admin dashboard", "Inventory management"]
                },
                {
                    "name": "Data Analytics Dashboard",
                    "description": "Interactive dashboard for visualizing complex datasets with real-time updates.",
                    "technologies": ["React", "Python", "FastAPI", "PostgreSQL", "D3.js"],
                    "highlights": ["Real-time data", "Custom visualizations", "Performance optimization"]
                }
            ],
            "experience": [
                {
                    "role": "AI Engineer",
                    "company": "Tech Startup",
                    "duration": "2023 - Present",
                    "description": "Developing AI-powered applications and implementing machine learning solutions for business problems.",
                    "achievements": ["Built RAG systems", "Improved model accuracy by 25%", "Led AI integration projects"]
                },
                {
                    "role": "Full-Stack Developer",
                    "company": "Software Company",
                    "duration": "2021 - 2023",
                    "description": "Developed and maintained web applications using modern technologies.",
                    "achievements": ["Reduced load times by 40%", "Built scalable APIs", "Mentored junior developers"]
                }
            ],
            "education": {
                "degree": "Bachelor's in Computer Science",
                "institution": "University Name",
                "year": "2021",
                "relevant_courses": ["Machine Learning", "Data Structures", "Web Development", "Database Systems"]
            }
        }

    async def initialize(self):
        """Initialize the RAG system with embeddings and vector store"""
        try:
            # Initialize OpenAI embeddings (you'll need to set OPENAI_API_KEY)
            # For demo purposes, we'll use a fallback if no API key is provided
            openai_api_key = os.getenv("OPENAI_API_KEY")
            
            if openai_api_key:
                self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
                self.llm = ChatOpenAI(
                    temperature=0.7,
                    model_name="gpt-3.5-turbo",
                    openai_api_key=openai_api_key
                )
            else:
                print("⚠️ OpenAI API key not found. Using fallback responses.")
                self.embeddings = None
                self.llm = None

            # Create documents from portfolio data
            documents = self._create_documents()
            
            if self.embeddings:
                # Initialize Chroma vector store
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory="./chroma_db"
                )
                
                # Create QA chain
                self._setup_qa_chain()
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"Error initializing RAG system: {e}")
            self.is_initialized = True  # Still mark as initialized for fallback
            return False

    def _create_documents(self) -> List[Document]:
        """Create LangChain documents from portfolio data"""
        documents = []
        
        # Personal information
        personal_text = f"""
        Name: {self.portfolio_data['personal_info']['name']}
        Title: {self.portfolio_data['personal_info']['title']}
        Email: {self.portfolio_data['personal_info']['email']}
        Location: {self.portfolio_data['personal_info']['location']}
        Summary: {self.portfolio_data['personal_info']['summary']}
        """
        documents.append(Document(page_content=personal_text, metadata={"type": "personal_info"}))
        
        # Skills
        for category, skills in self.portfolio_data['skills'].items():
            skills_text = f"{category.replace('_', ' ').title()} Skills: {', '.join(skills)}"
            documents.append(Document(page_content=skills_text, metadata={"type": "skills", "category": category}))
        
        # Projects
        for project in self.portfolio_data['projects']:
            project_text = f"""
            Project: {project['name']}
            Description: {project['description']}
            Technologies: {', '.join(project['technologies'])}
            Key Highlights: {', '.join(project['highlights'])}
            """
            documents.append(Document(page_content=project_text, metadata={"type": "project", "name": project['name']}))
        
        # Experience
        for exp in self.portfolio_data['experience']:
            exp_text = f"""
            Role: {exp['role']} at {exp['company']} ({exp['duration']})
            Description: {exp['description']}
            Key Achievements: {', '.join(exp['achievements'])}
            """
            documents.append(Document(page_content=exp_text, metadata={"type": "experience", "role": exp['role']}))
        
        # Education
        edu = self.portfolio_data['education']
        edu_text = f"""
        Education: {edu['degree']} from {edu['institution']} ({edu['year']})
        Relevant Courses: {', '.join(edu['relevant_courses'])}
        """
        documents.append(Document(page_content=edu_text, metadata={"type": "education"}))
        
        return documents

    def _setup_qa_chain(self):
        """Setup the QA chain with custom prompt"""
        if not self.vectorstore or not self.llm:
            return
            
        prompt_template = """
        You are Manas Sanjay's AI assistant. You help visitors learn about Manas's background, skills, projects, and experience.
        
        Use the following context to answer questions about Manas Sanjay:
        {context}
        
        Question: {question}
        
        Guidelines:
        - Be friendly, professional, and enthusiastic about Manas's work
        - If the question is about Manas's skills, projects, or experience, provide detailed information
        - If asked about contact information, provide the email and suggest reaching out
        - If the information isn't in the context, politely say you don't have that specific information
        - Keep responses conversational but informative
        - Highlight Manas's expertise in AI, machine learning, and full-stack development
        
        Answer:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt}
        )

    async def get_response(self, question: str) -> Dict[str, Any]:
        """Get response from the RAG system"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            if self.qa_chain:
                # Use RAG system
                response = self.qa_chain.run(question)
                return {
                    "answer": response,
                    "confidence": 0.9,
                    "source": "rag"
                }
            else:
                # Fallback responses
                return self._get_fallback_response(question)
                
        except Exception as e:
            print(f"Error getting response: {e}")
            return {
                "answer": "I'm sorry, I'm having trouble processing your question right now. Please try asking something else!",
                "confidence": 0.1,
                "source": "error"
            }

    def _get_fallback_response(self, question: str) -> Dict[str, Any]:
        """Provide fallback responses when RAG system is not available"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["skill", "technology", "tech", "programming"]):
            return {
                "answer": "Manas is skilled in AI/ML technologies like Python, TensorFlow, PyTorch, and LangChain. He's also proficient in full-stack development with React, TypeScript, FastAPI, and modern web technologies. His expertise spans from building intelligent systems to creating scalable web applications.",
                "confidence": 0.8,
                "source": "fallback"
            }
        
        elif any(word in question_lower for word in ["project", "work", "built", "developed"]):
            return {
                "answer": "Manas has worked on several exciting projects including this AI-powered portfolio with RAG chatbot capabilities, e-commerce platforms with payment integration, and data analytics dashboards. His projects showcase his ability to combine AI technologies with practical web applications.",
                "confidence": 0.8,
                "source": "fallback"
            }
        
        elif any(word in question_lower for word in ["experience", "background", "career"]):
            return {
                "answer": "Manas is an AI Engineer and Full-Stack Developer with experience in building intelligent systems and scalable web applications. He has worked on AI integration projects, improved model accuracy, and led development teams while focusing on performance optimization and modern technologies.",
                "confidence": 0.8,
                "source": "fallback"
            }
        
        elif any(word in question_lower for word in ["contact", "email", "reach", "hire"]):
            return {
                "answer": "You can reach Manas at manas.sanjay@example.com. He's always interested in discussing new opportunities, collaborations, and innovative projects in AI and web development!",
                "confidence": 0.9,
                "source": "fallback"
            }
        
        elif any(word in question_lower for word in ["education", "study", "degree"]):
            return {
                "answer": "Manas has a Bachelor's degree in Computer Science with relevant coursework in Machine Learning, Data Structures, Web Development, and Database Systems. His educational background provides a strong foundation for his work in AI and software development.",
                "confidence": 0.8,
                "source": "fallback"
            }
        
        else:
            return {
                "answer": "I'm here to help you learn about Manas Sanjay! You can ask me about his skills, projects, experience, education, or how to contact him. What would you like to know?",
                "confidence": 0.7,
                "source": "fallback"
            }

    async def get_portfolio_summary(self) -> str:
        """Get a summary of the portfolio"""
        return f"""
        {self.portfolio_data['personal_info']['name']} is a {self.portfolio_data['personal_info']['title']} 
        based in {self.portfolio_data['personal_info']['location']}. 
        
        He specializes in AI/ML technologies and full-stack web development, with expertise in 
        Python, React, FastAPI, and modern AI frameworks like LangChain and OpenAI. 
        
        His recent projects include AI-powered applications, e-commerce platforms, and data analytics dashboards. 
        Manas is passionate about combining cutting-edge AI technologies with practical web solutions.
        """
