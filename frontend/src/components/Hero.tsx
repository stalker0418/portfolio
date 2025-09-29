import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ChevronDown, Github, Linkedin, Mail, Download, MessageSquare, Send, Sparkles, Bot, User } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import PaintCursor from './PaintCursor';

const Hero: React.FC = () => {
  const navigate = useNavigate();
  const [chatMessage, setChatMessage] = useState('');
  const [typewriterText, setTypewriterText] = useState('');
  const fullText = 'AI Engineer & Research Enthusiast 🚀';

  // Typewriter effect
  useEffect(() => {
    let index = 0;
    const timer = setInterval(() => {
      if (index <= fullText.length) {
        setTypewriterText(fullText.slice(0, index));
        index++;
      } else {
        clearInterval(timer);
      }
    }, 80);

    return () => clearInterval(timer);
  }, [fullText]);

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
    <section id="home" className="min-h-screen flex items-center relative overflow-hidden py-24 md:py-32">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Gradient Orbs */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-purple-200 to-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-96 h-96 bg-gradient-to-r from-blue-200 to-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse delay-1000"></div>
        <div className="absolute bottom-20 left-1/3 w-80 h-80 bg-gradient-to-r from-pink-200 to-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse delay-2000"></div>
        
        {/* Floating Particles */}
        <div className="absolute inset-0">
          {[...Array(15)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-purple-300 rounded-full opacity-40 animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 3}s`
              }}
            ></div>
          ))}
        </div>
      </div>

      <div className="container mx-auto px-6 grid lg:grid-cols-2 gap-12 items-center relative z-10">
        {/* Left Side - Intro Content */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="text-left relative z-10"
        >
          <motion.div
            variants={itemVariants}
            className="mb-8"
          >
            <h1 className="text-[48px] md:text-[56px] lg:text-[64px] font-bold mb-6 tracking-tight leading-[1.05] text-gray-800">
              Hi, I'm{' '}
              <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                Manas Sanjay
              </span>
            </h1>
            <p className="text-[24px] md:text-[28px] lg:text-[32px] font-bold text-gray-700 mb-8 h-10 leading-tight">
              {typewriterText}
              <span className="animate-pulse text-purple-600">|</span>
            </p>
            <p className="text-lg font-medium text-gray-600 leading-relaxed mb-8">
              Turning caffeine into code and code into smarter AI!
            </p>
          </motion.div>

          <motion.div
            variants={itemVariants}
            className="flex flex-col sm:flex-row items-start gap-4 mb-12"
          >
            <motion.button
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-4 rounded-full font-semibold transition-all duration-300 flex items-center gap-2 h-14 shadow-lg hover:shadow-xl"
            >
              <Download size={20} />
              Download Resume
            </motion.button>
            
            <motion.a
              href="#contact"
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              className="border-2 border-purple-600 text-purple-600 hover:bg-purple-600 hover:text-white px-8 py-4 rounded-full font-semibold transition-all duration-300 h-14 flex items-center justify-center"
            >
              Get In Touch
            </motion.a>
          </motion.div>

          <motion.div
            variants={itemVariants}
            className="flex items-center gap-8 mb-16"
          >
            <motion.a
              href="https://github.com/stalker0418"
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.2, rotate: 5 }}
              whileTap={{ scale: 0.9 }}
              className="text-gray-600 hover:text-purple-600 transition-all duration-300 p-3 rounded-full hover:bg-purple-50"
            >
              <Github size={28} />
            </motion.a>
            <motion.a
              href="https://www.linkedin.com/in/manas-sanjay/"
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.2, rotate: -5 }}
              whileTap={{ scale: 0.9 }}
              className="text-gray-600 hover:text-purple-600 transition-all duration-300 p-3 rounded-full hover:bg-purple-50"
            >
              <Linkedin size={28} />
            </motion.a>
            <motion.a
              href="mailto:pakalapati.sanjay@gmail.com"
              whileHover={{ scale: 1.2, rotate: 5 }}
              whileTap={{ scale: 0.9 }}
              className="text-gray-600 hover:text-purple-600 transition-all duration-300 p-3 rounded-full hover:bg-purple-50"
            >
              <Mail size={28} />
            </motion.a>
          </motion.div>
        </motion.div>

        {/* Right Side - Chat Bot */}
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="relative"
        >
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
            className="max-w-lg mx-auto relative"
          >
            {/* Modern container */}
            <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-8 border border-purple-200 shadow-2xl">
              <div className="mb-6 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <div className="p-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500">
                    <MessageSquare className="text-white" size={20} />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-800">Ask My AI Assistant</h3>
                </div>
                <p className="text-base text-gray-600 font-medium">
                  Get instant answers about my experience, projects, and skills
                </p>
              </div>
            
            <form onSubmit={handleChatSubmit} className="relative">
              <div className="relative bg-gray-50 rounded-2xl p-1 border border-gray-200">
                <input
                  type="text"
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  placeholder="Ask me about my projects, skills, or experience..."
                  className="w-full px-6 py-4 bg-transparent text-gray-800 placeholder-gray-500 focus:outline-none rounded-xl text-base"
                />
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={!chatMessage.trim()}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white p-3 rounded-xl transition-all duration-200 shadow-lg"
                >
                  <Send size={18} />
                </motion.button>
              </div>
              <div className="mt-6">
                <span className="text-sm text-gray-600 block text-center mb-3 font-medium">Try asking:</span>
                <div className="flex flex-wrap items-center justify-center gap-2">
                  {[
                    "Show me your best project",
                    "What tools do you use?",
                    "Tell me about your AI experience",
                    "What's your latest job?",
                    "How did you get into AI?"
                  ].map((prompt, index) => (
                    <motion.button
                      key={index}
                      type="button"
                      onClick={() => setChatMessage(prompt)}
                      whileHover={{ scale: 1.05, y: -2 }}
                      whileTap={{ scale: 0.95 }}
                      className="px-4 py-2 text-sm bg-purple-50 hover:bg-purple-100 text-purple-700 hover:text-purple-800 rounded-full border border-purple-200 hover:border-purple-300 transition-all duration-200 shadow-sm hover:shadow-md font-medium"
                    >
                      {prompt}
                    </motion.button>
                  ))}
                </div>
              </div>
            </form>
            </div>
          </motion.div>
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
          className="text-[#64748b] hover:text-primary-500 transition-colors duration-200"
        >
          <ChevronDown size={32} />
        </motion.a>
      </motion.div>
    </section>
  );
};

export default Hero;
