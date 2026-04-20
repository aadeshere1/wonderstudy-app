'use client';

import Link from 'next/link';
import { Nav } from '@/components/layout';
import { useGamification } from '@/contexts/GamificationContext';
import { getLevelForXP, getXPProgress, LEVELS } from '@/lib/gamification/levels';
import { ALL_BADGES, RARITY_COLORS } from '@/lib/gamification/badges';

export default function ProfileClient() {
  const { data } = useGamification();
  const level = getLevelForXP(data.totalXP);
  const { current, needed, pct } = getXPProgress(data.totalXP);
  const earned = new Set(data.badgesEarned);

  return (
    <>
      <Nav title="WonderStudy" />

      <main className="relative z-10 max-w-2xl mx-auto px-4 pb-16">

        {/* ── Hero ── */}
        <div className="text-center pt-10 pb-6">
          <div
            style={{
              width: 88,
              height: 88,
              borderRadius: 22,
              background: level.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '3rem',
              margin: '0 auto 16px',
              boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
            }}
          >
            {level.emoji}
          </div>

          <h1
            className="font-display text-3xl mb-1"
            style={{ color: 'var(--ws-text)' }}
          >
            {level.title}
          </h1>
          <div style={{ color: 'var(--ws-text-muted)', fontSize: '0.85rem', fontFamily: 'var(--font-nunito)', fontWeight: 700 }}>
            Level {level.level} · {data.totalXP} XP total
          </div>
        </div>

        {/* ── XP Progress bar ── */}
        <div className="card mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="font-display text-base" style={{ color: 'var(--ws-text)' }}>XP Progress</span>
            <span style={{ fontSize: '0.75rem', color: 'var(--ws-text-muted)', fontFamily: 'var(--font-nunito)', fontWeight: 700 }}>
              {needed > 0 ? `${current} / ${needed} to Level ${level.level + 1}` : '👑 Max Level!'}
            </span>
          </div>
          <div style={{ height: 12, background: 'var(--ws-card2)', borderRadius: 99, overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${pct}%`, background: level.color, borderRadius: 99, transition: 'width 0.6s ease' }} />
          </div>
        </div>

        {/* ── Stats row ── */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 20 }}>
          {[
            { emoji: '🎯', value: data.totalQuestions, label: 'Questions' },
            { emoji: '✅', value: data.totalCorrect, label: 'Correct' },
            { emoji: '🔥', value: data.dailyStreak, label: 'Day Streak' },
          ].map(stat => (
            <div key={stat.label} className="card text-center" style={{ padding: '16px 8px' }}>
              <div style={{ fontSize: '1.6rem', marginBottom: 4 }}>{stat.emoji}</div>
              <div className="font-display text-2xl" style={{ color: 'var(--ws-text)' }}>{stat.value}</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--ws-text-muted)', fontFamily: 'var(--font-nunito)', fontWeight: 700 }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* ── More stats ── */}
        <div className="card mb-6">
          <div className="font-display text-xl mb-3" style={{ color: 'var(--ws-text)' }}>📊 Stats</div>
          {[
            ['🏆', 'Best Streak', `${data.maxStreak} correct in a row`],
            ['🎮', 'Sessions Done', `${data.sessionsCompleted} sessions`],
            ['📖', 'Teach Sessions', `${data.teachSessions} lessons`],
            ['🔁', 'Review Sessions', `${data.reviewSessions} reviews`],
            ['🏅', 'Badges Earned', `${data.badgesEarned.length} / ${ALL_BADGES.length}`],
          ].map(([emoji, label, value]) => (
            <div key={String(label)} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid var(--ws-border)' }}>
              <span style={{ fontFamily: 'var(--font-nunito)', fontWeight: 800, color: 'var(--ws-text)', fontSize: '0.85rem' }}>{emoji} {label}</span>
              <span style={{ fontFamily: 'var(--font-nunito)', fontWeight: 700, color: 'var(--ws-text-muted)', fontSize: '0.85rem' }}>{value}</span>
            </div>
          ))}
        </div>

        {/* ── Level ladder ── */}
        <div className="card mb-6">
          <div className="font-display text-xl mb-3" style={{ color: 'var(--ws-text)' }}>⬆️ Levels</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {LEVELS.map(lvl => {
              const isUnlocked = data.totalXP >= lvl.minXP;
              const isCurrent  = lvl.level === level.level;
              return (
                <div
                  key={lvl.level}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    padding: '10px 12px',
                    borderRadius: 12,
                    background: isCurrent ? 'var(--ws-card2)' : 'transparent',
                    border: isCurrent ? `1px solid var(--ws-border)` : '1px solid transparent',
                    opacity: isUnlocked ? 1 : 0.4,
                  }}
                >
                  <div style={{ width: 36, height: 36, borderRadius: 9, background: isUnlocked ? lvl.color : 'var(--ws-card2)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem', flexShrink: 0 }}>
                    {isUnlocked ? lvl.emoji : '🔒'}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontFamily: 'var(--font-fredoka-one)', fontSize: '1rem', color: 'var(--ws-text)' }}>
                      Level {lvl.level} · {lvl.title}
                      {isCurrent && <span style={{ marginLeft: 8, fontSize: '0.65rem', fontFamily: 'var(--font-nunito)', fontWeight: 800, background: lvl.color, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>YOU ARE HERE</span>}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--ws-text-muted)', fontFamily: 'var(--font-nunito)', fontWeight: 700 }}>
                      {lvl.maxXP === Infinity ? `${lvl.minXP}+ XP` : `${lvl.minXP} – ${lvl.maxXP} XP`}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Badges ── */}
        <div className="card mb-6">
          <div className="font-display text-xl mb-1" style={{ color: 'var(--ws-text)' }}>🏅 Badges</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--ws-text-muted)', fontFamily: 'var(--font-nunito)', fontWeight: 700, marginBottom: 16 }}>
            {data.badgesEarned.length} of {ALL_BADGES.length} unlocked
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: 12 }}>
            {ALL_BADGES.map(badge => {
              const unlocked = earned.has(badge.id);
              const colors   = RARITY_COLORS[badge.rarity];
              return (
                <div
                  key={badge.id}
                  title={`${badge.name}: ${badge.description}`}
                  style={{
                    borderRadius: 14,
                    padding: '12px 8px',
                    textAlign: 'center',
                    background: unlocked ? colors.bg : 'var(--ws-card2)',
                    border: `1px solid ${unlocked ? colors.border : 'var(--ws-border)'}`,
                    opacity: unlocked ? 1 : 0.45,
                    transition: 'all 0.2s',
                  }}
                >
                  <div style={{ fontSize: '1.8rem', filter: unlocked ? 'none' : 'grayscale(1)' }}>{badge.emoji}</div>
                  <div style={{ fontSize: '0.65rem', fontFamily: 'var(--font-nunito)', fontWeight: 800, color: unlocked ? colors.text : 'var(--ws-text-muted)', marginTop: 4, lineHeight: 1.2 }}>{badge.name}</div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="text-center mt-6">
          <Link href="/" style={{ color: 'var(--ws-text-dim)', fontFamily: 'var(--font-nunito)', fontWeight: 800, fontSize: '0.85rem', textDecoration: 'none' }}>
            ← Back to home
          </Link>
        </div>
      </main>
    </>
  );
}
