import React, { useEffect, useRef, useState, useCallback } from 'react';

interface PaintPoint {
  x: number;
  y: number;
  timestamp: number;
}

interface FluidTrail {
  id: number;
  points: PaintPoint[];
  color: string;
  opacity: number;
  timestamp: number;
}

const PaintCursor: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [trails, setTrails] = useState<FluidTrail[]>([]);
  const trailIdRef = useRef(0);
  const animationRef = useRef<number>();
  const lastMousePosRef = useRef({ x: 0, y: 0 });
  const isMouseMovingRef = useRef(false);

  const colors = [
    'rgba(16, 185, 129, 0.8)',   // Green
    'rgba(245, 158, 11, 0.8)',   // Orange  
    'rgba(217, 70, 239, 0.8)',   // Purple
    'rgba(59, 130, 246, 0.8)',   // Blue
  ];

  const drawFluidTrail = useCallback((ctx: CanvasRenderingContext2D, trail: FluidTrail) => {
    if (trail.points.length < 2) return;

    ctx.globalAlpha = trail.opacity;
    ctx.strokeStyle = trail.color;
    ctx.lineWidth = 8;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Create smooth curves through points
    ctx.beginPath();
    ctx.moveTo(trail.points[0].x, trail.points[0].y);

    for (let i = 1; i < trail.points.length - 2; i++) {
      const cp1x = (trail.points[i].x + trail.points[i + 1].x) / 2;
      const cp1y = (trail.points[i].y + trail.points[i + 1].y) / 2;
      ctx.quadraticCurveTo(trail.points[i].x, trail.points[i].y, cp1x, cp1y);
    }

    // Draw the last segment
    if (trail.points.length > 1) {
      const lastPoint = trail.points[trail.points.length - 1];
      const secondLastPoint = trail.points[trail.points.length - 2];
      ctx.quadraticCurveTo(secondLastPoint.x, secondLastPoint.y, lastPoint.x, lastPoint.y);
    }

    ctx.stroke();

    // Add flowing gradient effect
    const gradient = ctx.createRadialGradient(
      trail.points[trail.points.length - 1]?.x || 0,
      trail.points[trail.points.length - 1]?.y || 0,
      0,
      trail.points[trail.points.length - 1]?.x || 0,
      trail.points[trail.points.length - 1]?.y || 0,
      30
    );
    gradient.addColorStop(0, trail.color);
    gradient.addColorStop(1, 'transparent');

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(
      trail.points[trail.points.length - 1]?.x || 0,
      trail.points[trail.points.length - 1]?.y || 0,
      15,
      0,
      Math.PI * 2
    );
    ctx.fill();
  }, []);

  const animate = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas with slight trail effect
    ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Update and draw trails
    setTrails(prevTrails => {
      const now = Date.now();
      const updatedTrails = prevTrails
        .map(trail => ({
          ...trail,
          opacity: Math.max(0, trail.opacity - 0.02), // Fade out gradually
          points: trail.points.filter(point => now - point.timestamp < 2000) // Keep points for 2 seconds
        }))
        .filter(trail => trail.opacity > 0.1 && trail.points.length > 0);

      // Draw all trails
      updatedTrails.forEach(trail => drawFluidTrail(ctx, trail));

      return updatedTrails;
    });

    animationRef.current = requestAnimationFrame(animate);
  }, [drawFluidTrail]);

  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    if (!container || !canvas) return;

    // Set canvas size
    const resizeCanvas = () => {
      const rect = container.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    let currentTrail: FluidTrail | null = null;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const now = Date.now();

      // Calculate movement speed for dynamic effects
      const dx = x - lastMousePosRef.current.x;
      const dy = y - lastMousePosRef.current.y;
      const speed = Math.sqrt(dx * dx + dy * dy);

      lastMousePosRef.current = { x, y };
      isMouseMovingRef.current = true;

      // Create new trail if none exists or if mouse moved significantly
      if (!currentTrail || speed > 5) {
        currentTrail = {
          id: trailIdRef.current++,
          points: [],
          color: colors[trailIdRef.current % colors.length],
          opacity: 1.0,
          timestamp: now,
        };

        setTrails(prev => [...prev, currentTrail!]);
      }

      // Add point to current trail
      if (currentTrail) {
        const newPoint: PaintPoint = { x, y, timestamp: now };
        currentTrail.points.push(newPoint);
        
        // Limit trail length for performance
        if (currentTrail.points.length > 20) {
          currentTrail.points.shift();
        }
      }
    };

    const handleMouseEnter = () => {
      container.style.cursor = 'none';
      isMouseMovingRef.current = true;
    };

    const handleMouseLeave = () => {
      container.style.cursor = 'default';
      isMouseMovingRef.current = false;
      currentTrail = null;
    };

    const handleMouseStop = () => {
      setTimeout(() => {
        if (!isMouseMovingRef.current) {
          currentTrail = null;
        }
      }, 100);
    };

    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseenter', handleMouseEnter);
    container.addEventListener('mouseleave', handleMouseLeave);
    container.addEventListener('mousestop', handleMouseStop);

    // Start animation loop
    animate();

    return () => {
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeEventListener('mouseenter', handleMouseEnter);
      container.removeEventListener('mouseleave', handleMouseLeave);
      container.removeEventListener('mousestop', handleMouseStop);
      window.removeEventListener('resize', resizeCanvas);
      
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate]);

  return (
    <div 
      ref={containerRef}
      className="absolute inset-0 pointer-events-none overflow-hidden"
      style={{ zIndex: 10 }}
    >
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
        style={{ mixBlendMode: 'multiply' }}
      />
      
    </div>
  );
};

export default PaintCursor;
