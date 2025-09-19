// API Configuration
const isDevelopment = process.env.NODE_ENV === 'development';
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const isVercelDeployment = window.location.hostname.includes('vercel.app');

// Backend API URL configuration
export const API_BASE_URL = (() => {
  if (isDevelopment || isLocalhost) {
    return 'http://localhost:8000';
  }
  
  // If deployed on Vercel, use environment variable or default
  if (isVercelDeployment) {
    return process.env.REACT_APP_API_URL || 'https://your-backend-url.com';
  }
  
  // Fallback for other production environments
  return process.env.REACT_APP_API_URL || 'https://your-backend-url.com';
})();

// API endpoints
export const API_ENDPOINTS = {
  CHAT: `${API_BASE_URL}/chat`,
  HEALTH: `${API_BASE_URL}/health`,
  PORTFOLIO_SUMMARY: `${API_BASE_URL}/api/portfolio/summary`,
} as const;

// Axios default configuration
export const axiosConfig = {
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
};
