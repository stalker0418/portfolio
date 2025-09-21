import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronDown, Github, Linkedin, Mail, Download, MessageSquare, Send, Sparkles, Bot, User } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import PaintCursor from './PaintCursor';

const Hero: React.FC = () => {
  const navigate = useNavigate();
  const [chatMessage, setChatMessage] = useState('');

  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (chatMessage.trim()) {
      navigate('/chat', { state: { initialMessage: chatMessage } });
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: 0.3,
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  };

  const chatVariants = {
    hidden: { scale: 0.8, opacity: 0, y: 50 },
    visible: {
      scale: 1,
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 20,
        delay: 0.8
      }
    }
  };

  return (
    <section id="home" className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Paint Cursor Effect */}
      <PaintCursor />
      
      {/* Floating Background Orbs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="floating-orb floating-orb-1"></div>
        <div className="floating-orb floating-orb-2"></div>
        <div className="floating-orb floating-orb-3"></div>
      </div>

      {/* Main Content */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="container mx-auto px-6 relative z-20"
      >
        <div className="grid lg:grid-cols-2 gap-12 items-center min-h-screen">
          {/* Left Side - Personal Info */}
          <motion.div
            variants={itemVariants}
            className="text-left space-y-8"
          >
            <div className="space-y-4">
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-primary rounded-full text-white text-sm font-medium"
              >
                <Sparkles size={16} />
                Available for new opportunities
              </motion.div>
              
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight">
                Hi, I'm{' '}
                <span className="gradient-text block">Manas Sanjay</span>
              </h1>
              
              <p className="text-xl md:text-2xl text-gray-600 font-medium">
                AI Engineer & Full-Stack Developer
              </p>
              
              <p className="text-lg text-gray-700 max-w-lg leading-relaxed">
                Passionate about building intelligent systems and creating seamless user experiences 
                with cutting-edge AI technologies and modern web development.
              </p>
            </div>

            <motion.div
              variants={itemVariants}
              className="flex flex-col sm:flex-row items-start gap-4"
            >
              <motion.button
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="group px-8 py-4 rounded-2xl font-semibold flex items-center gap-3 bg-gradient-primary hover:bg-gradient-secondary text-white border-0 shadow-lg transition-all duration-300 hover:shadow-xl hover:shadow-primary-500/25"
              >
                <Download size={20} className="group-hover:animate-bounce" />
                Download Resume
              </motion.button>
              
              <motion.a
                href="#contact"
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 rounded-2xl font-semibold text-gray-700 hover:text-white glass-light border-2 border-primary-500/30 hover:bg-gradient-primary hover:border-primary-500 transition-all duration-300 hover:shadow-lg"
              >
                Get In Touch
              </motion.a>
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="flex items-center gap-6"
            >
              <motion.a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.2, rotate: 5 }}
                className="w-12 h-12 glass rounded-full flex items-center justify-center text-gray-600 hover:text-primary-500 transition-colors duration-200"
              >
                <Github size={20} />
              </motion.a>
              <motion.a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.2, rotate: -5 }}
                className="w-12 h-12 glass rounded-full flex items-center justify-center text-gray-600 hover:text-primary-500 transition-colors duration-200"
              >
                <Linkedin size={20} />
              </motion.a>
              <motion.a
                href="mailto:your.email@example.com"
                whileHover={{ scale: 1.2, rotate: 5 }}
                className="w-12 h-12 glass rounded-full flex items-center justify-center text-gray-600 hover:text-primary-500 transition-colors duration-200"
              >
                <Mail size={20} />
              </motion.a>
            </motion.div>
          </motion.div>

          {/* Right Side - Chat Interface (Main Focus) */}
          <motion.div
            variants={chatVariants}
            className="relative"
          >
            <div className="glass-elevated p-8 relative overflow-hidden">
              {/* Subtle glow effect */}
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-primary-500/10 via-secondary-500/5 to-accent-500/10 opacity-50"></div>
              
              <div className="relative z-10">
                {/* Chat Header */}
                <div className="text-center mb-8">
                  <div className="inline-flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 bg-gradient-primary rounded-full flex items-center justify-center text-white shadow-lg">
                      <Bot size={20} />
                    </div>
                    <div className="text-left">
                      <h3 className="text-2xl font-bold gradient-text">AI Assistant</h3>
                      <p className="text-sm text-gray-600">Powered by advanced AI</p>
                    </div>
                  </div>
                  <p className="text-gray-700 text-lg">
                    Ask me anything about my experience, projects, and skills
                  </p>
                </div>

                {/* Sample Chat Messages */}
                <div className="space-y-4 mb-8 max-h-64 overflow-y-auto">
                  <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 1.2 }}
                    className="flex items-start gap-3"
                  >
                    <div className="w-8 h-8 bg-gradient-secondary rounded-full flex items-center justify-center text-white flex-shrink-0">
                      <Bot size={14} />
                    </div>
                    <div className="bg-gradient-to-br from-primary-50 to-primary-100 border border-primary-200 rounded-2xl rounded-tl-sm px-4 py-3 max-w-xs">
                      <p className="text-sm text-gray-800 font-medium">
                        Hi! I'm Manas's AI assistant. I can tell you about his projects, skills, and experience. What would you like to know?
                      </p>
                    </div>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 1.4 }}
                    className="flex items-start gap-3 justify-end"
                  >
                    <div className="bg-gradient-primary rounded-2xl rounded-tr-sm px-4 py-3 text-white max-w-xs">
                      <p className="text-sm">
                        What are his main technical skills?
                      </p>
                    </div>
                    <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center flex-shrink-0">
                      <User size={14} />
                    </div>
                  </motion.div>
                </div>
                
                {/* Chat Input */}
                <form onSubmit={handleChatSubmit} className="relative">
                  <div className="relative glass-strong rounded-2xl p-1">
                    <input
                      type="text"
                      value={chatMessage}
                      onChange={(e) => setChatMessage(e.target.value)}
                      placeholder="Ask me about my projects, skills, or experience..."
                      className="w-full px-6 py-4 bg-transparent text-gray-800 placeholder-gray-500 focus:outline-none rounded-xl text-lg font-medium"
                    />
                    <motion.button
                      type="submit"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      disabled={!chatMessage.trim()}
                      className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gradient-primary hover:bg-gradient-secondary disabled:bg-gray-300 disabled:cursor-not-allowed text-white p-3 rounded-xl transition-all duration-200 shadow-lg"
                    >
                      <Send size={18} />
                    </motion.button>
                  </div>
                  
                  {/* Quick Suggestions */}
                  <div className="flex flex-wrap items-center justify-center gap-3 mt-4">
                    <span className="text-xs text-gray-600 font-medium">Try asking:</span>
                    <button
                      type="button"
                      onClick={() => setChatMessage("What are your main skills?")}
                      className="text-xs px-3 py-1 glass-light rounded-full text-primary-700 hover:text-primary-800 hover:glass-card transition-all duration-200 font-medium"
                    >
                      "What are your main skills?"
                    </button>
                    <button
                      type="button"
                      onClick={() => setChatMessage("Tell me about your projects")}
                      className="text-xs px-3 py-1 glass-light rounded-full text-primary-700 hover:text-primary-800 hover:glass-card transition-all duration-200 font-medium"
                    >
                      "Tell me about your projects"
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          variants={itemVariants}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <motion.a
            href="#about"
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-12 h-12 glass rounded-full flex items-center justify-center text-gray-600 hover:text-primary-500 transition-colors duration-200"
          >
            <ChevronDown size={24} />
          </motion.a>
        </motion.div>
      </motion.div>
    </section>
  );
};

export default Hero;
