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
    <section id="about" className="py-20 bg-dark-800/50">
      <div className="container mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            About <span className="gradient-text">Me</span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
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
              whileHover={{ scale: 1.05 }}
              className="glass rounded-xl p-6 text-center"
            >
              <div className="text-primary-500 mb-4 flex justify-center">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="glass rounded-2xl p-8 max-w-4xl mx-auto"
        >
          <h3 className="text-2xl font-bold mb-6 text-center">My Journey</h3>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-xl font-semibold mb-4 text-primary-500">Education & Background</h4>
              <p className="text-gray-300 leading-relaxed">
                With a strong foundation in computer science and artificial intelligence, 
                I've dedicated my career to exploring the intersection of AI and web development. 
                My passion for technology drives me to continuously learn and adapt to new challenges.
              </p>
            </div>
            <div>
              <h4 className="text-xl font-semibold mb-4 text-primary-500">Current Focus</h4>
              <p className="text-gray-300 leading-relaxed">
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
