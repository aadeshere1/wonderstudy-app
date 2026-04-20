'use client';

import { useEffect } from 'react';
import { useGamification } from '@/contexts/GamificationContext';
import { RARITY_COLORS } from '@/lib/gamification/badges';

export default function BadgeToast() {
  const { pendingBadges, clearBadge } = useGamification();

  // Auto-dismiss oldest badge after 3.5s
  useEffect(() => {
    if (pendingBadges.length === 0) return;
    const timer = setTimeout(() => {
      clearBadge(pendingBadges[0].id);
    }, 3500);
    return () => clearTimeout(timer);
  }, [pendingBadges, clearBadge]);

  if (pendingBadges.length === 0) return null;

  const badge = pendingBadges[0];
  const colors = RARITY_COLORS[badge.rarity];

  return (
    <div
      style={{
        position: 'fixed',
        top: 70,
        right: 16,
        zIndex: 9999,
        display: 'flex',
        flexDirection: 'column',
        gap: 10,
        pointerEvents: 'none',
        animation: 'badgeSlideIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275)',
      }}
    >
      <style>{`
        @keyframes badgeSlideIn {
          from { opacity: 0; transform: translateX(120px) scale(0.8); }
          to   { opacity: 1; transform: translateX(0) scale(1); }
        }
      `}</style>

      <div
        style={{
          background: 'var(--ws-surface)',
          border: `2px solid ${colors.border}`,
          borderRadius: 16,
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          minWidth: 240,
          maxWidth: 300,
          boxShadow: `0 8px 32px rgba(0,0,0,0.2), 0 0 0 1px ${colors.border}`,
          pointerEvents: 'auto',
        }}
        onClick={() => clearBadge(badge.id)}
      >
        {/* Badge emoji */}
        <div
          style={{
            width: 48,
            height: 48,
            borderRadius: 12,
            background: colors.bg,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.6rem',
            flexShrink: 0,
          }}
        >
          {badge.emoji}
        </div>

        {/* Text */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: '0.65rem',
              fontWeight: 900,
              letterSpacing: '0.08em',
              color: colors.text,
              textTransform: 'uppercase',
              fontFamily: 'var(--font-nunito)',
              marginBottom: 2,
            }}
          >
            🏅 Badge Unlocked · {badge.rarity}
          </div>
          <div
            style={{
              fontFamily: 'var(--font-fredoka-one)',
              fontSize: '1rem',
              color: 'var(--ws-text)',
              lineHeight: 1.2,
            }}
          >
            {badge.name}
          </div>
          <div
            style={{
              fontSize: '0.72rem',
              color: 'var(--ws-text-muted)',
              fontFamily: 'var(--font-nunito)',
              marginTop: 2,
            }}
          >
            {badge.description}
          </div>
        </div>
      </div>

      {/* Stack indicator */}
      {pendingBadges.length > 1 && (
        <div
          style={{
            fontSize: '0.7rem',
            color: 'var(--ws-text-muted)',
            textAlign: 'right',
            fontFamily: 'var(--font-nunito)',
            fontWeight: 700,
          }}
        >
          +{pendingBadges.length - 1} more
        </div>
      )}
    </div>
  );
}
