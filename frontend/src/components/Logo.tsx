import React from 'react';

interface LogoProps {
  size?: number;
  className?: string;
}

const Logo: React.FC<LogoProps> = ({ size = 32, className = "" }) => {
  return (
    <div className={`flex items-center justify-center ${className}`}>
      <svg 
        width={size} 
        height={size} 
        viewBox="0 0 48 48" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
        className="drop-shadow-sm"
      >
        {/* Background circle with gradient */}
        <defs>
          <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#8b5cf6" />
            <stop offset="50%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#3b82f6" />
          </linearGradient>
        </defs>
        
        {/* Main circle */}
        <circle cx="24" cy="24" r="22" fill="url(#logoGradient)" stroke="#ffffff" strokeWidth="2"/>
        
        {/* Letter M */}
        <path 
          d="M12 32V16h4l4 8 4-8h4v16h-3V21l-3 6h-2l-3-6v11h-3z" 
          fill="white" 
          strokeWidth="0.5"
          stroke="rgba(255,255,255,0.3)"
        />
        
        {/* Small AI accent dot */}
        <circle cx="34" cy="14" r="3" fill="#10b981" stroke="#ffffff" strokeWidth="1"/>
        <circle cx="34" cy="14" r="1.5" fill="#ffffff"/>
      </svg>
    </div>
  );
};

export default Logo;
