'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useGamification } from '@/contexts/GamificationContext';
import { getLevelForXP, getXPProgress } from '@/lib/gamification/levels';

export default function XPBar() {
  const { data } = useGamification();
  const [showTooltip, setShowTooltip] = useState(false);

  const level = getLevelForXP(data.totalXP);
  const { current, needed, pct } = getXPProgress(data.totalXP);

  return (
    <Link
      href="/profile"
      style={{ textDecoration: 'none' }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, position: 'relative' }}>
        {/* Level badge */}
        <div
          style={{
            width: 36,
            height: 36,
            borderRadius: 10,
            background: level.color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.2rem',
            flexShrink: 0,
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
          }}
        >
          {level.emoji}
        </div>

        {/* XP bar (hidden on small screens) */}
        <div
          className="hidden sm:flex"
          style={{ flexDirection: 'column', gap: 2, minWidth: 80 }}
        >
          <div
            style={{
              fontSize: '0.65rem',
              fontWeight: 800,
              fontFamily: 'var(--font-nunito)',
              color: 'var(--ws-text-muted)',
              letterSpacing: '0.03em',
            }}
          >
            Lv {level.level} · {level.title}
          </div>
          <div
            style={{
              height: 5,
              background: 'var(--ws-border)',
              borderRadius: 99,
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                height: '100%',
                width: `${pct}%`,
                background: level.color,
                borderRadius: 99,
                transition: 'width 0.5s ease',
              }}
            />
          </div>
        </div>

        {/* Tooltip */}
        {showTooltip && (
          <div
            style={{
              position: 'absolute',
              top: '110%',
              right: 0,
              background: 'var(--ws-surface)',
              border: '1px solid var(--ws-border)',
              borderRadius: 12,
              padding: '10px 14px',
              whiteSpace: 'nowrap',
              zIndex: 100,
              boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
              fontFamily: 'var(--font-nunito)',
            }}
          >
            <div style={{ fontWeight: 900, color: 'var(--ws-text)', fontSize: '0.8rem', marginBottom: 4 }}>
              {level.emoji} {level.title} · Level {level.level}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--ws-text-muted)' }}>
              {needed > 0
                ? `${current} / ${needed} XP to next level`
                : `👑 Max level reached!`}
            </div>
            <div style={{ fontSize: '0.7rem', color: 'var(--ws-text-dim)', marginTop: 2 }}>
              🔥 {data.dailyStreak} day streak · 🏅 {data.badgesEarned.length} badges
            </div>
          </div>
        )}
      </div>
    </Link>
  );
}
