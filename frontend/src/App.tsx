import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Header from './components/Header';
import Hero from './components/Hero';
import About from './components/About';
import Projects from './components/Projects';
import Skills from './components/Skills';
import Contact from './components/Contact';
import ChatBot from './components/ChatBot';
import ChatPage from './components/ChatPage';
import './App.css';

const queryClient = new QueryClient();

// Home page component
const HomePage: React.FC = () => (
  <>
    <Header />
    <main>
      <Hero />
      <About />
      <Projects />
      <Skills />
      <Contact />
    </main>
    <ChatBot />
  </>
);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App min-h-screen bg-dark-900 text-white">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/chat" element={<ChatPage />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;