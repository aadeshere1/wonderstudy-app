'use client';

import { useEffect, useState } from 'react';

export interface TimerProps {
  seconds: number;
  totalSeconds?: number;
  isActive?: boolean;
  onTimeUp?: () => void;
  variant?: 'default' | 'warning' | 'critical';
}

export const Timer = ({
  seconds,
  totalSeconds = 60,
  isActive = true,
  onTimeUp,
  variant = 'default',
}: TimerProps) => {
  const [displaySeconds, setDisplaySeconds] = useState(seconds);

  useEffect(() => {
    setDisplaySeconds(seconds);
  }, [seconds]);

  useEffect(() => {
    if (!isActive || displaySeconds <= 0) return;
    const timer = setInterval(() => {
      setDisplaySeconds((prev) => {
        const next = prev - 1;
        if (next <= 0) { onTimeUp?.(); return 0; }
        return next;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [isActive, displaySeconds, onTimeUp]);

  // Auto-upgrade variant based on time left
  let displayVariant = variant;
  if (displaySeconds <= 10 && displaySeconds > 0 && variant === 'default') displayVariant = 'warning';
  if (displaySeconds <= 0) displayVariant = 'critical';

  const strokeColor = {
    default: '#60a5fa',
    warning: '#fbbf24',
    critical: '#f87171',
  }[displayVariant];

  const textColor = {
    default: '#60a5fa',
    warning: '#fbbf24',
    critical: '#f87171',
  }[displayVariant];

  // SVG ring math
  const r = 38;
  const circumference = 2 * Math.PI * r; // ≈ 238.76
  const progress = totalSeconds > 0 ? Math.max(0, displaySeconds / totalSeconds) : 1;
  const dashOffset = circumference * (1 - progress);

  const minutes = Math.floor(displaySeconds / 60);
  const secs = displaySeconds % 60;
  const timeStr = minutes > 0
    ? `${minutes}:${secs.toString().padStart(2, '0')}`
    : `${displaySeconds}`;

  return (
    <div className="relative flex-shrink-0" style={{ width: 90, height: 90 }}>
      {/* SVG ring */}
      <svg
        width="90"
        height="90"
        viewBox="0 0 90 90"
        style={{ transform: 'rotate(-90deg)' }}
        className="absolute inset-0"
      >
        {/* background track */}
        <circle
          cx="45" cy="45" r={r}
          fill="none"
          stroke="rgba(255,255,255,0.08)"
          strokeWidth="6"
        />
        {/* progress arc */}
        <circle
          cx="45" cy="45" r={r}
          fill="none"
          stroke={strokeColor}
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          style={{ transition: 'stroke-dashoffset 0.9s linear, stroke 0.5s' }}
        />
      </svg>

      {/* centred number */}
      <div
        className="absolute inset-0 flex items-center justify-center font-display text-2xl"
        style={{ color: textColor }}
      >
        {timeStr}
      </div>
    </div>
  );
};
