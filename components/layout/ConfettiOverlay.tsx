"use client";

import { useEffect, useState } from "react";
import { createConfetti } from "@/lib/utils/helpers";

export interface ConfettiOverlayProps {
  active?: boolean;
  count?: number;
}

export const ConfettiOverlay = ({ active = false, count = 50 }: ConfettiOverlayProps) => {
  const [particles, setParticles] = useState<any[]>([]);

  useEffect(() => {
    if (active) {
      setParticles(createConfetti(count));
      // Auto-clear after animation
      const timer = setTimeout(() => setParticles([]), 1200);
      return () => clearTimeout(timer);
    }
  }, [active, count]);

  if (!particles.length) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      {particles.map((particle, i) => (
        <div
          key={i}
          className="absolute w-2.5 h-2.5 rounded animate-cfFall"
          style={{
            left: particle.left,
            top: "-10px",
            backgroundColor: particle.color,
            animationDelay: particle.delay,
          }}
        />
      ))}
    </div>
  );
};
