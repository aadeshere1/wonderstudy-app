'use client';

import { useEffect, useState } from 'react';
import { useGamification } from '@/contexts/GamificationContext';

export default function LevelUpModal() {
  const { pendingLevelUp, clearLevelUp } = useGamification();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (pendingLevelUp) {
      setVisible(true);
      const t = setTimeout(() => {
        setVisible(false);
        setTimeout(clearLevelUp, 400);
      }, 3500);
      return () => clearTimeout(t);
    }
  }, [pendingLevelUp, clearLevelUp]);

  if (!pendingLevelUp || !visible) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'rgba(0,0,0,0.5)',
        backdropFilter: 'blur(6px)',
        animation: 'levelFadeIn 0.4s ease',
      }}
      onClick={() => { setVisible(false); setTimeout(clearLevelUp, 400); }}
    >
      <style>{`
        @keyframes levelFadeIn {
          from { opacity: 0; }
          to   { opacity: 1; }
        }
        @keyframes levelBounce {
          0%   { transform: scale(0.5) rotate(-10deg); opacity: 0; }
          60%  { transform: scale(1.1) rotate(3deg); opacity: 1; }
          80%  { transform: scale(0.95) rotate(-1deg); }
          100% { transform: scale(1) rotate(0); }
        }
        @keyframes sparkle {
          0%, 100% { transform: scale(1);   opacity: 1; }
          50%       { transform: scale(1.3); opacity: 0.6; }
        }
      `}</style>

      <div
        style={{
          background: 'var(--ws-surface)',
          borderRadius: 28,
          padding: '48px 40px',
          textAlign: 'center',
          maxWidth: 320,
          width: '90vw',
          boxShadow: `0 24px 80px rgba(0,0,0,0.35), 0 0 0 2px rgba(255,255,255,0.1)`,
          animation: 'levelBounce 0.6s cubic-bezier(0.175,0.885,0.32,1.275)',
        }}
        onClick={e => e.stopPropagation()}
      >
        {/* Sparkles */}
        <div style={{ fontSize: '1.5rem', marginBottom: 8, animation: 'sparkle 0.8s ease infinite' }}>
          ✨ ✨ ✨
        </div>

        {/* Level emoji (big) */}
        <div
          style={{
            width: 96,
            height: 96,
            borderRadius: 24,
            background: pendingLevelUp.color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '3rem',
            margin: '0 auto 16px',
            boxShadow: '0 12px 40px rgba(0,0,0,0.25)',
          }}
        >
          {pendingLevelUp.emoji}
        </div>

        {/* Level up text */}
        <div
          style={{
            fontFamily: 'var(--font-fredoka-one)',
            fontSize: '0.9rem',
            letterSpacing: '0.15em',
            textTransform: 'uppercase',
            background: pendingLevelUp.color,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            marginBottom: 6,
          }}
        >
          Level Up!
        </div>

        <div
          style={{
            fontFamily: 'var(--font-fredoka-one)',
            fontSize: '2.2rem',
            color: 'var(--ws-text)',
            lineHeight: 1.1,
            marginBottom: 8,
          }}
        >
          {pendingLevelUp.title}
        </div>

        <div
          style={{
            fontFamily: 'var(--font-nunito)',
            fontSize: '0.85rem',
            color: 'var(--ws-text-muted)',
            marginBottom: 24,
          }}
        >
          You reached Level {pendingLevelUp.level}!
        </div>

        <button
          onClick={() => { setVisible(false); setTimeout(clearLevelUp, 400); }}
          style={{
            padding: '10px 32px',
            borderRadius: 14,
            background: pendingLevelUp.color,
            border: 'none',
            color: 'white',
            fontFamily: 'var(--font-fredoka-one)',
            fontSize: '1rem',
            cursor: 'pointer',
            boxShadow: '0 4px 16px rgba(0,0,0,0.2)',
          }}
        >
          Awesome! 🎉
        </button>
      </div>
    </div>
  );
}
