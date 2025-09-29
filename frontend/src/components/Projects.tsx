import React from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Github, Brain, Globe, Database } from 'lucide-react';

const Projects: React.FC = () => {
  const projects = [
    {
      title: "AI-Powered Portfolio",
      description: "An intelligent portfolio website with integrated chatbot using RAG technology for answering questions about my experience and projects.",
      tech: ["React", "TypeScript", "FastAPI", "LangChain", "OpenAI"],
      icon: <Brain className="w-6 h-6" />,
      github: "#",
      live: "#",
      image: "/api/placeholder/400/250"
    },
    {
      title: "E-Commerce Platform",
      description: "Full-stack e-commerce solution with modern UI, payment integration, and admin dashboard for managing products and orders.",
      tech: ["Next.js", "Node.js", "MongoDB", "Stripe", "Tailwind"],
      icon: <Globe className="w-6 h-6" />,
      github: "#",
      live: "#",
      image: "/api/placeholder/400/250"
    },
    {
      title: "Data Analytics Dashboard",
      description: "Interactive dashboard for visualizing complex datasets with real-time updates and customizable charts and metrics.",
      tech: ["React", "Python", "FastAPI", "PostgreSQL", "D3.js"],
      icon: <Database className="w-6 h-6" />,
      github: "#",
      live: "#",
      image: "/api/placeholder/400/250"
    }
  ];

  return (
    <section id="projects" className="py-24 md:py-32 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0">
        <div className="absolute top-10 left-10 w-72 h-72 bg-gradient-to-r from-pink-200/30 to-purple-200/30 rounded-full blur-3xl"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-gradient-to-r from-blue-200/30 to-indigo-200/30 rounded-full blur-3xl"></div>
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
            Featured <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">Projects</span>
          </h2>
          <p className="text-lg font-medium text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Here are some of my recent projects that showcase my skills in AI, 
            full-stack development, and creating innovative solutions.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-8">
          {projects.map((project, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -8, rotateY: 5 }}
              className="bg-white/80 backdrop-blur-lg rounded-xl overflow-hidden group perspective-1000 transform-style-preserve-3d hover:shadow-2xl transition-all duration-300 border border-purple-200 hover:border-purple-300"
              style={{ transformStyle: 'preserve-3d' }}
            >
              {/* Project Image */}
              <div className="relative h-48 bg-gradient-to-br from-purple-100 to-pink-100 flex items-center justify-center overflow-hidden">
                <motion.div 
                  className="text-purple-600 z-10"
                  whileHover={{ scale: 1.2, rotate: 10 }}
                  transition={{ duration: 0.3 }}
                >
                  {project.icon}
                </motion.div>
                <div className="absolute inset-0 bg-gradient-to-br from-purple-200/20 to-pink-200/20 group-hover:from-purple-200/40 group-hover:to-pink-200/40 transition-all duration-300"></div>
                
                {/* Floating particles on hover */}
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  {[...Array(5)].map((_, i) => (
                    <motion.div
                      key={i}
                      className="absolute w-2 h-2 bg-primary-400/60 rounded-full"
                      initial={{ 
                        x: Math.random() * 100 + '%',
                        y: Math.random() * 100 + '%',
                        scale: 0 
                      }}
                      whileHover={{ 
                        scale: 1,
                        y: [null, -20, -40],
                        opacity: [0.6, 0.3, 0]
                      }}
                      transition={{ 
                        duration: 2,
                        delay: i * 0.1,
                        repeat: Infinity 
                      }}
                    />
                  ))}
                </div>
              </div>

              {/* Project Content */}
              <div className="p-6">
                <h3 className="text-xl font-bold mb-3 text-gray-800 group-hover:text-purple-600 transition-colors duration-200">
                  {project.title}
                </h3>
                <p className="text-gray-600 mb-4 leading-relaxed">
                  {project.description}
                </p>

                {/* Tech Stack */}
                <div className="flex flex-wrap gap-2 mb-6">
                  {project.tech.map((tech, techIndex) => (
                    <span
                      key={techIndex}
                      className="px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded-full border border-purple-200"
                    >
                      {tech}
                    </span>
                  ))}
                </div>

                {/* Project Links */}
                <div className="flex gap-4">
                  <motion.a
                    href={project.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex items-center gap-2 text-gray-600 hover:text-purple-600 transition-colors duration-200"
                  >
                    <Github size={18} />
                    Code
                  </motion.a>
                  <motion.a
                    href={project.live}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className="flex items-center gap-2 text-gray-600 hover:text-purple-600 transition-colors duration-200"
                  >
                    <ExternalLink size={18} />
                    Live Demo
                  </motion.a>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <motion.a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="inline-flex items-center gap-2 border border-purple-600 text-purple-600 hover:bg-purple-600 hover:text-white px-6 py-3 rounded-full font-semibold transition-all duration-200"
          >
            <Github size={20} />
            View All Projects
          </motion.a>
        </motion.div>
      </div>
    </section>
  );
};

export default Projects;
