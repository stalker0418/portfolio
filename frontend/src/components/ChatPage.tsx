import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, ArrowLeft, Sparkles } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { API_ENDPOINTS, axiosConfig } from '../config/api';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const ChatPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const initialMessage = location.state?.initialMessage || '';
  
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hi! I'm Manas's AI assistant. Ask me anything about his experience, skills, or projects!",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle initial message from hero section
  useEffect(() => {
    if (initialMessage) {
      setInputMessage(initialMessage);
      // Auto-focus the input after a short delay
      setTimeout(() => {
        inputRef.current?.focus();
      }, 500);
    }
  }, [initialMessage]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      // Call the backend API
      const response = await axios.post(API_ENDPOINTS.CHAT, {
        message: inputMessage
      }, axiosConfig);

      const botMessage: Message = {
        id: messages.length + 2,
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: messages.length + 2,
        text: "I'm sorry, I'm having trouble connecting right now. Please try again later!",
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <motion.header 
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="border-b border-white/20 glass-elevated sticky top-0 z-10"
      >
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <motion.button
            onClick={() => navigate('/')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-2 text-gray-700 hover:text-primary-600 transition-colors duration-200 font-medium"
          >
            <ArrowLeft size={20} />
            <span>Back to Portfolio</span>
          </motion.button>
          
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-primary rounded-full flex items-center justify-center shadow-lg">
              <Bot size={18} />
            </div>
            <div>
              <h1 className="font-semibold text-gray-800">Chat with Manas's AI</h1>
              <p className="text-xs text-gray-600">Powered by AI • Ask me anything</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2 text-primary-700">
            <Sparkles size={16} />
            <span className="text-sm font-medium">AI Assistant</span>
          </div>
        </div>
      </motion.header>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-8">
          <div className="space-y-6">
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex items-start gap-4 max-w-[80%] ${
                  message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}>
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                    message.sender === 'user' 
                      ? 'bg-gradient-primary' 
                      : 'bg-gradient-secondary'
                  }`}>
                    {message.sender === 'user' ? <User size={18} /> : <Bot size={18} />}
                  </div>
                  <div className={`rounded-2xl px-6 py-4 ${
                    message.sender === 'user'
                      ? 'bg-gradient-primary text-white'
                      : 'bg-gradient-to-br from-primary-50 to-primary-100 border border-primary-200 text-gray-800'
                  }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
                    <p className={`text-xs mt-2 ${
                      message.sender === 'user' 
                        ? 'text-white/70' 
                        : 'text-gray-600'
                    }`}>
                      {formatTime(message.timestamp)}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
            
            {/* Typing Indicator */}
            {isTyping && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex justify-start"
              >
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-gradient-secondary rounded-full flex items-center justify-center">
                    <Bot size={18} />
                  </div>
                  <div className="bg-gradient-to-br from-primary-50 to-primary-100 border border-primary-200 rounded-2xl px-6 py-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-secondary-500 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-accent-500 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Message Input */}
        <motion.div 
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="border-t border-white/20 glass-elevated sticky bottom-0 p-6"
        >
          <form onSubmit={sendMessage} className="max-w-4xl mx-auto">
            <div className="flex gap-4 items-end">
              <div className="flex-1 relative">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Ask me anything about Manas..."
                  className="w-full px-6 py-4 glass-strong rounded-2xl focus:border-primary-500 focus:outline-none text-gray-800 placeholder-gray-500 resize-none font-medium"
                  disabled={isTyping}
                />
                <div className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500">
                  <kbd className="px-2 py-1 text-xs glass-light rounded">Enter</kbd>
                </div>
              </div>
              <motion.button
                type="submit"
                disabled={!inputMessage.trim() || isTyping}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-6 py-4 bg-gradient-primary hover:bg-gradient-secondary disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-2xl transition-all duration-200 flex items-center justify-center min-w-[60px] shadow-lg"
              >
                <Send size={20} />
              </motion.button>
            </div>
            <p className="text-xs text-gray-600 mt-3 text-center">
              Press Enter to send • This AI assistant knows about Manas's experience, projects, and skills
            </p>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default ChatPage;


