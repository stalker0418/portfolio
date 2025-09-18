import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronDown, Github, Linkedin, Mail, Download, MessageSquare, Send } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

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

  return (
    <section id="home" className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background Animation */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="container mx-auto px-6 text-center relative z-10"
      >
        <motion.div
          variants={itemVariants}
          className="mb-8"
        >
          <h1 className="text-5xl md:text-7xl font-bold mb-4">
            Hi, I'm{' '}
            <span className="gradient-text">Manas Sanjay</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-6">
            AI Engineer & Full-Stack Developer
          </p>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            Passionate about building intelligent systems and creating seamless user experiences 
            with cutting-edge AI technologies and modern web development.
          </p>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-primary-500 hover:bg-primary-600 text-white px-8 py-3 rounded-full font-semibold transition-colors duration-200 flex items-center gap-2"
          >
            <Download size={20} />
            Download Resume
          </motion.button>
          
          <motion.a
            href="#contact"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="border border-primary-500 text-primary-500 hover:bg-primary-500 hover:text-white px-8 py-3 rounded-full font-semibold transition-all duration-200"
          >
            Get In Touch
          </motion.a>
        </motion.div>

        {/* Chat Input Box */}
        <motion.div
          variants={itemVariants}
          className="mb-12"
        >
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
            className="max-w-2xl mx-auto"
          >
            <div className="mb-4 text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <MessageSquare className="text-primary-500" size={20} />
                <h3 className="text-lg font-semibold text-white">Ask My AI Assistant</h3>
              </div>
              <p className="text-sm text-gray-400">
                Get instant answers about my experience, projects, and skills
              </p>
            </div>
            
            <form onSubmit={handleChatSubmit} className="relative">
              <div className="relative glass rounded-2xl p-1 border border-primary-500/20">
                <input
                  type="text"
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  placeholder="Ask me about my projects, skills, or experience..."
                  className="w-full px-6 py-4 bg-transparent text-white placeholder-gray-400 focus:outline-none rounded-xl"
                />
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={!chatMessage.trim()}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-primary-500 hover:bg-primary-600 disabled:bg-gray-600 disabled:cursor-not-allowed text-white p-3 rounded-xl transition-all duration-200"
                >
                  <Send size={18} />
                </motion.button>
              </div>
              <div className="flex items-center justify-center gap-4 mt-3">
                <span className="text-xs text-gray-500">Try asking:</span>
                <button
                  type="button"
                  onClick={() => setChatMessage("What are your main skills?")}
                  className="text-xs text-primary-400 hover:text-primary-300 transition-colors"
                >
                  "What are your main skills?"
                </button>
                <button
                  type="button"
                  onClick={() => setChatMessage("Tell me about your projects")}
                  className="text-xs text-primary-400 hover:text-primary-300 transition-colors"
                >
                  "Tell me about your projects"
                </button>
              </div>
            </form>
          </motion.div>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="flex items-center justify-center gap-6 mb-16"
        >
          <motion.a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.2, rotate: 5 }}
            className="text-gray-400 hover:text-primary-500 transition-colors duration-200"
          >
            <Github size={24} />
          </motion.a>
          <motion.a
            href="https://linkedin.com"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.2, rotate: -5 }}
            className="text-gray-400 hover:text-primary-500 transition-colors duration-200"
          >
            <Linkedin size={24} />
          </motion.a>
          <motion.a
            href="mailto:your.email@example.com"
            whileHover={{ scale: 1.2, rotate: 5 }}
            className="text-gray-400 hover:text-primary-500 transition-colors duration-200"
          >
            <Mail size={24} />
          </motion.a>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <motion.a
            href="#about"
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="text-gray-400 hover:text-primary-500 transition-colors duration-200"
          >
            <ChevronDown size={32} />
          </motion.a>
        </motion.div>
      </motion.div>
    </section>
  );
};

export default Hero;
