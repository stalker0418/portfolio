import React from 'react';
import { motion } from 'framer-motion';
import { Code, Brain, Zap, Users } from 'lucide-react';

const About: React.FC = () => {
  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI & Machine Learning",
      description: "Expertise in building intelligent systems using modern AI frameworks and techniques."
    },
    {
      icon: <Code className="w-8 h-8" />,
      title: "Full-Stack Development",
      description: "Proficient in both frontend and backend technologies for complete web solutions."
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Performance Optimization",
      description: "Focus on creating fast, efficient, and scalable applications."
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Team Collaboration",
      description: "Strong communication skills and experience working in agile development teams."
    }
  ];

  return (
    <section id="about" className="py-24 md:py-32 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0">
        <div className="absolute top-20 right-20 w-64 h-64 bg-gradient-to-r from-purple-200/30 to-pink-200/30 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 left-20 w-80 h-80 bg-gradient-to-r from-blue-200/30 to-indigo-200/30 rounded-full blur-3xl"></div>
      </div>
      
      <div className="container mx-auto px-6 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-[32px] md:text-[36px] font-bold mb-6 text-gray-800 tracking-tight">
            About <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">Me</span>
          </h2>
          <p className="text-lg font-medium text-gray-600 max-w-3xl mx-auto leading-relaxed">
            I'm a passionate AI Engineer and Full-Stack Developer with a strong background in 
            building intelligent systems and scalable web applications. I love combining 
            cutting-edge AI technologies with modern web development to create innovative solutions.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.05, y: -5 }}
              className="bg-white/80 backdrop-blur-lg rounded-xl p-6 text-center border border-purple-200 hover:border-purple-300 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              <div className="text-purple-600 mb-4 flex justify-center">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">{feature.title}</h3>
              <p className="text-base font-medium text-gray-600 leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="bg-white/80 backdrop-blur-lg rounded-2xl p-8 max-w-4xl mx-auto border border-purple-200 shadow-xl"
        >
          <h3 className="text-2xl font-bold mb-8 text-center text-gray-800">My Journey</h3>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-xl font-semibold mb-4 text-purple-600">Education & Background</h4>
              <p className="text-base font-medium text-gray-600 leading-relaxed">
                With a strong foundation in computer science and artificial intelligence, 
                I've dedicated my career to exploring the intersection of AI and web development. 
                My passion for technology drives me to continuously learn and adapt to new challenges.
              </p>
            </div>
            <div>
              <h4 className="text-xl font-semibold mb-4 text-purple-600">Current Focus</h4>
              <p className="text-base font-medium text-gray-600 leading-relaxed">
                Currently focused on developing AI-powered applications, implementing RAG systems, 
                and creating intelligent chatbots. I enjoy working with modern frameworks like 
                React, FastAPI, and various AI/ML libraries to build comprehensive solutions.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default About;
