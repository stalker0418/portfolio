import React, { useEffect, useRef } from 'react';
import './WaterAnimation.css';

const WaterAnimation: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const ripplesRef = useRef<Array<{
    x: number;
    y: number;
    radius: number;
    opacity: number;
    color: string;
  }>>([]);
  
  const floatingShapesRef = useRef<Array<{
    x: number;
    y: number;
    size: number;
    speed: number;
    angle: number;
    type: 'node' | 'connection' | 'binary' | 'circuit' | 'spark';
    opacity: number;
    pulse?: number;
  }>>([]);

  const colors = [
    '#3b82f6', // Blue
    '#8b5cf6', // Purple  
    '#ec4899', // Pink
    '#10b981', // Emerald
    '#f59e0b', // Amber
    '#ef4444', // Red
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Initialize floating AI shapes
    const initFloatingShapes = () => {
      floatingShapesRef.current = [];
      for (let i = 0; i < 20; i++) {
        floatingShapesRef.current.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 12 + 6,
          speed: Math.random() * 0.8 + 0.3,
          angle: Math.random() * Math.PI * 2,
          type: ['node', 'connection', 'binary', 'circuit', 'spark'][Math.floor(Math.random() * 5)] as 'node' | 'connection' | 'binary' | 'circuit' | 'spark',
          opacity: Math.random() * 0.4 + 0.15,
        });
      }
    };

    initFloatingShapes();

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      // Create ripple on mouse move with some throttling
      if (Math.random() > 0.6) {
        ripplesRef.current.push({
          x,
          y,
          radius: 0,
          opacity: 1,
          color: colors[Math.floor(Math.random() * colors.length)]
        });
      }
    };

    const animate = () => {
      // Clear canvas with very light overlay
      ctx.fillStyle = 'rgba(243, 232, 255, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update and draw floating AI shapes
      floatingShapesRef.current.forEach((shape, index) => {
        // Initialize pulse if not exists
        if (shape.pulse === undefined) {
          shape.pulse = Math.random() * Math.PI * 2;
        }
        
        // Update position with slight curve
        shape.angle += Math.sin(Date.now() * 0.001 + index) * 0.01;
        shape.x += Math.cos(shape.angle) * shape.speed;
        shape.y += Math.sin(shape.angle) * shape.speed;
        shape.pulse += 0.05;

        // Wrap around screen
        if (shape.x < -30) shape.x = canvas.width + 30;
        if (shape.x > canvas.width + 30) shape.x = -30;
        if (shape.y < -30) shape.y = canvas.height + 30;
        if (shape.y > canvas.height + 30) shape.y = -30;

        // Dynamic opacity with pulse
        const pulseOpacity = shape.opacity + Math.sin(shape.pulse) * 0.1;

        // Draw shapes based on type
        ctx.save();
        ctx.globalAlpha = Math.max(0.1, pulseOpacity);
        
        if (shape.type === 'node') {
          // Draw glowing neural network node
          const gradient = ctx.createRadialGradient(shape.x, shape.y, 0, shape.x, shape.y, shape.size * 2);
          gradient.addColorStop(0, '#8b5cf6');
          gradient.addColorStop(0.5, '#a855f7');
          gradient.addColorStop(1, 'transparent');
          
          ctx.beginPath();
          ctx.arc(shape.x, shape.y, shape.size + Math.sin(shape.pulse) * 2, 0, Math.PI * 2);
          ctx.fillStyle = gradient;
          ctx.fill();
          
          // Inner core
          ctx.beginPath();
          ctx.arc(shape.x, shape.y, shape.size * 0.6, 0, Math.PI * 2);
          ctx.fillStyle = '#c084fc';
          ctx.fill();
          
        } else if (shape.type === 'connection') {
          // Draw animated connection lines
          const lineLength = shape.size + Math.sin(shape.pulse) * 4;
          ctx.beginPath();
          ctx.moveTo(shape.x - lineLength, shape.y);
          ctx.lineTo(shape.x + lineLength, shape.y);
          ctx.moveTo(shape.x, shape.y - lineLength);
          ctx.lineTo(shape.x, shape.y + lineLength);
          ctx.strokeStyle = '#6366f1';
          ctx.lineWidth = 3;
          ctx.lineCap = 'round';
          ctx.stroke();
          
          // Add glowing effect
          ctx.shadowColor = '#6366f1';
          ctx.shadowBlur = 10;
          ctx.stroke();
          ctx.shadowBlur = 0;
          
        } else if (shape.type === 'binary') {
          // Draw glowing binary code
          const binary = Math.floor(Date.now() / 500 + index) % 2 === 0 ? '1' : '0';
          ctx.font = `bold ${shape.size}px 'Courier New', monospace`;
          ctx.fillStyle = '#10b981';
          ctx.shadowColor = '#10b981';
          ctx.shadowBlur = 8;
          ctx.fillText(binary, shape.x - shape.size/2, shape.y + shape.size/2);
          ctx.shadowBlur = 0;
          
        } else if (shape.type === 'circuit') {
          // Draw circuit board pattern
          const size = shape.size;
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 2;
          ctx.beginPath();
          // Draw circuit paths
          ctx.moveTo(shape.x - size, shape.y);
          ctx.lineTo(shape.x - size/2, shape.y);
          ctx.lineTo(shape.x - size/2, shape.y - size/2);
          ctx.lineTo(shape.x + size/2, shape.y - size/2);
          ctx.lineTo(shape.x + size/2, shape.y + size/2);
          ctx.lineTo(shape.x + size, shape.y + size/2);
          ctx.stroke();
          
          // Add circuit nodes
          ctx.beginPath();
          ctx.arc(shape.x - size/2, shape.y - size/2, 2, 0, Math.PI * 2);
          ctx.arc(shape.x + size/2, shape.y + size/2, 2, 0, Math.PI * 2);
          ctx.fillStyle = '#fbbf24';
          ctx.fill();
          
        } else if (shape.type === 'spark') {
          // Draw electric spark
          const sparkSize = shape.size + Math.sin(shape.pulse * 2) * 3;
          ctx.strokeStyle = '#ec4899';
          ctx.lineWidth = 2;
          ctx.lineCap = 'round';
          
          // Draw spark lines
          for (let i = 0; i < 6; i++) {
            const sparkAngle = (i * Math.PI) / 3 + shape.pulse;
            const startX = shape.x + Math.cos(sparkAngle) * sparkSize * 0.3;
            const startY = shape.y + Math.sin(sparkAngle) * sparkSize * 0.3;
            const endX = shape.x + Math.cos(sparkAngle) * sparkSize;
            const endY = shape.y + Math.sin(sparkAngle) * sparkSize;
            
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.stroke();
          }
          
          // Add glow effect
          ctx.shadowColor = '#ec4899';
          ctx.shadowBlur = 15;
          ctx.beginPath();
          ctx.arc(shape.x, shape.y, 3, 0, Math.PI * 2);
          ctx.fillStyle = '#f472b6';
          ctx.fill();
          ctx.shadowBlur = 0;
        }
        
        ctx.restore();
      });

      // Update and draw ripples
      ripplesRef.current = ripplesRef.current.filter(ripple => {
        ripple.radius += 5;
        ripple.opacity -= 0.015;

        if (ripple.opacity > 0) {
          ctx.save();
          
          // Main ripple with gradient
          const gradient = ctx.createRadialGradient(
            ripple.x, ripple.y, ripple.radius * 0.8,
            ripple.x, ripple.y, ripple.radius
          );
          gradient.addColorStop(0, `${ripple.color}00`);
          gradient.addColorStop(1, `${ripple.color}${Math.floor(ripple.opacity * 180).toString(16).padStart(2, '0')}`);
          
          ctx.beginPath();
          ctx.arc(ripple.x, ripple.y, ripple.radius, 0, Math.PI * 2);
          ctx.strokeStyle = gradient;
          ctx.lineWidth = 4;
          ctx.stroke();

          // Add glow effect
          ctx.shadowColor = ripple.color;
          ctx.shadowBlur = 15;
          ctx.beginPath();
          ctx.arc(ripple.x, ripple.y, ripple.radius * 0.7, 0, Math.PI * 2);
          ctx.strokeStyle = `${ripple.color}${Math.floor(ripple.opacity * 120).toString(16).padStart(2, '0')}`;
          ctx.lineWidth = 2;
          ctx.stroke();
          
          // Inner pulse
          ctx.shadowBlur = 0;
          ctx.beginPath();
          ctx.arc(ripple.x, ripple.y, ripple.radius * 0.4, 0, Math.PI * 2);
          ctx.strokeStyle = `${ripple.color}${Math.floor(ripple.opacity * 255).toString(16).padStart(2, '0')}`;
          ctx.lineWidth = 1;
          ctx.stroke();

          ctx.restore();
          return true;
        }
        return false;
      });

      requestAnimationFrame(animate);
    };

    window.addEventListener('mousemove', handleMouseMove);
    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className="water-animation">
      <canvas ref={canvasRef} className="water-canvas" />
    </div>
  );
};

export default WaterAnimation;
