'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { isAdmin } from '@/lib/admin/config';
import { subscribeToStudents } from '@/lib/admin/queries';
import { getXPProgress } from '@/lib/gamification/levels';
import type { StudentSummary } from '@/lib/admin/types';
import StudentDetail from './StudentDetail';

function relativeTime(iso: string) {
  if (!iso) return 'Never';
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 2) return 'Just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 7) return `${days}d ago`;
  return new Date(iso).toLocaleDateString();
}

function StudentCard({ student, onClick }: { student: StudentSummary; onClick: () => void }) {
  const accuracy = student.totalQuestions > 0
    ? Math.round((student.totalCorrect / student.totalQuestions) * 100) : 0;
  const xpProg = getXPProgress(student.totalXP);

  return (
    <button
      onClick={onClick}
      style={{
        background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
        borderRadius: 20, padding: 20, cursor: 'pointer', textAlign: 'left',
        width: '100%', transition: 'all 0.18s',
        fontFamily: 'var(--font-nunito),sans-serif',
      }}
      onMouseEnter={(e) => {
        (e.currentTarget as HTMLElement).style.transform = 'translateY(-2px)';
        (e.currentTarget as HTMLElement).style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)';
        (e.currentTarget as HTMLElement).style.borderColor = '#a78bfa';
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLElement).style.transform = '';
        (e.currentTarget as HTMLElement).style.boxShadow = '';
        (e.currentTarget as HTMLElement).style.borderColor = 'var(--ws-border)';
      }}
    >
      {/* Top row: avatar + name + last seen */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
        <div style={{ position: 'relative', flexShrink: 0 }}>
          {student.photoURL ? (
            <img
              src={student.photoURL}
              referrerPolicy="no-referrer"
              alt={student.name}
              style={{ width: 48, height: 48, borderRadius: '50%', objectFit: 'cover' }}
            />
          ) : (
            <div style={{
              width: 48, height: 48, borderRadius: '50%',
              background: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 20, fontWeight: 900, color: 'white',
            }}>
              {student.name[0]?.toUpperCase() ?? '?'}
            </div>
          )}
          {/* level badge */}
          <div style={{
            position: 'absolute', bottom: -3, right: -3,
            background: 'var(--ws-surface)', border: '1.5px solid var(--ws-border)',
            borderRadius: '50%', width: 20, height: 20,
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11,
          }}>
            {student.levelEmoji}
          </div>
        </div>

        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{
            fontFamily: 'var(--font-fredoka-one),cursive', fontSize: '1rem',
            color: 'var(--ws-text)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
          }}>
            {student.name}
          </div>
          <div style={{
            fontSize: '0.72rem', color: 'var(--ws-text-muted)', marginTop: 1,
            whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
          }}>
            {student.email}
          </div>
        </div>

        <div style={{ textAlign: 'right', flexShrink: 0 }}>
          <div style={{ fontSize: '0.68rem', color: 'var(--ws-text-muted)' }}>last seen</div>
          <div style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--ws-text)' }}>
            {relativeTime(student.lastSeen)}
          </div>
        </div>
      </div>

      {/* Level + XP bar */}
      <div style={{ marginBottom: 14 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
          <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#a78bfa' }}>
            Lv {student.level} {student.levelTitle}
          </span>
          <span style={{ fontSize: '0.7rem', color: 'var(--ws-text-muted)' }}>
            {student.totalXP} XP
          </span>
        </div>
        <div style={{
          height: 5, borderRadius: 3, background: 'var(--ws-card2)', overflow: 'hidden',
        }}>
          <div style={{
            width: `${xpProg.pct}%`, height: '100%',
            background: 'linear-gradient(90deg,#a78bfa,#60a5fa)', borderRadius: 3,
          }} />
        </div>
      </div>

      {/* Stats row */}
      <div style={{ display: 'flex', gap: 0, borderTop: '1px solid var(--ws-border)', paddingTop: 12 }}>
        {[
          { label: 'Questions', value: student.totalQuestions, color: 'var(--ws-text)' },
          { label: 'Accuracy', value: `${accuracy}%`, color: accuracy >= 80 ? '#34d399' : accuracy >= 60 ? '#fbbf24' : '#f87171' },
          { label: 'Streak', value: `🔥${student.dailyStreak}`, color: '#f97316' },
          { label: 'Lessons', value: student.lessonsVisited.length, color: '#60a5fa' },
        ].map(({ label, value, color }, i, arr) => (
          <div key={label} style={{
            flex: 1, textAlign: 'center',
            borderRight: i < arr.length - 1 ? '1px solid var(--ws-border)' : 'none',
          }}>
            <div style={{ fontSize: '0.95rem', fontWeight: 900, color }}>{value}</div>
            <div style={{ fontSize: '0.62rem', color: 'var(--ws-text-muted)', fontWeight: 700 }}>{label}</div>
          </div>
        ))}
      </div>
    </button>
  );
}

/** Skeleton card shown while the real-time subscription hasn't emitted yet */
function SkeletonCard() {
  return (
    <div style={{
      background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
      borderRadius: 20, padding: 20, overflow: 'hidden',
    }}>
      {[72, 100, 60, 40].map((w, i) => (
        <div key={i} style={{
          height: i === 0 ? 48 : 12, width: `${w}%`,
          borderRadius: 8, marginBottom: i === 0 ? 14 : 8,
          background: 'linear-gradient(90deg, var(--ws-card2) 25%, var(--ws-border) 50%, var(--ws-card2) 75%)',
          backgroundSize: '200% 100%',
          animation: 'shimmer 1.5s infinite',
        }} />
      ))}
    </div>
  );
}

export default function AdminDashboard() {
  const { user, loading: authLoading } = useAuth();
  // null = not yet received first snapshot; [] = received but empty
  const [students, setStudents] = useState<StudentSummary[] | null>(null);
  const [selected, setSelected] = useState<StudentSummary | null>(null);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<'lastSeen' | 'questions' | 'accuracy' | 'name'>('lastSeen');

  // Real-time subscription — UI auto-updates whenever any student's data changes
  useEffect(() => {
    if (!user || !isAdmin(user.email)) return;
    const unsub = subscribeToStudents(
      (s) => setStudents(s),
      () => setStudents([]), // on error fall back to empty
    );
    return unsub; // cleanup on unmount
  }, [user]);

  const dataLoading = students === null; // snapshot not yet received
  const studentList = students ?? [];

  // ── Auth guard ───────────────────────────────────────────────────────────
  if (authLoading) {
    return (
      <div style={{
        minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: 'var(--ws-bg)',
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>⏳</div>
          <div style={{
            fontFamily: 'var(--font-fredoka-one),cursive',
            fontSize: '1.4rem', color: '#a78bfa',
          }}>Checking access…</div>
        </div>
      </div>
    );
  }

  if (!user || !isAdmin(user.email)) {
    return (
      <div style={{
        minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: 'var(--ws-bg)', padding: 24,
      }}>
        <div style={{ textAlign: 'center', maxWidth: 380 }}>
          <div style={{ fontSize: 64, marginBottom: 16 }}>🔒</div>
          <div style={{
            fontFamily: 'var(--font-fredoka-one),cursive',
            fontSize: '1.8rem', color: 'var(--ws-text)', marginBottom: 8,
          }}>Admin only</div>
          <p style={{ color: 'var(--ws-text-muted)', marginBottom: 24, lineHeight: 1.6 }}>
            {user
              ? `Your account (${user.email}) does not have admin access.`
              : 'Please sign in with your admin account to access this page.'}
          </p>
          <Link
            href="/"
            style={{
              display: 'inline-block', padding: '12px 28px', borderRadius: 14,
              background: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
              color: 'white', fontFamily: 'var(--font-fredoka-one),cursive',
              fontSize: '1rem', textDecoration: 'none',
            }}
          >← Back to app</Link>
        </div>
      </div>
    );
  }

  // ── Student detail view ───────────────────────────────────────────────────
  if (selected) {
    return <StudentDetail student={selected} onBack={() => setSelected(null)} />;
  }

  // ── Filter + sort ─────────────────────────────────────────────────────────
  const q = search.toLowerCase().trim();
  let visible = q
    ? studentList.filter(
        (s) => s.name.toLowerCase().includes(q) || s.email.toLowerCase().includes(q)
      )
    : [...studentList];

  visible = visible.sort((a, b) => {
    if (sortBy === 'lastSeen') return (b.lastSeen ?? '').localeCompare(a.lastSeen ?? '');
    if (sortBy === 'questions') return b.totalQuestions - a.totalQuestions;
    if (sortBy === 'accuracy') {
      const accA = a.totalQuestions > 0 ? a.totalCorrect / a.totalQuestions : 0;
      const accB = b.totalQuestions > 0 ? b.totalCorrect / b.totalQuestions : 0;
      return accB - accA;
    }
    return a.name.localeCompare(b.name);
  });

  // ── Aggregate stats ───────────────────────────────────────────────────────
  const totalStudents = studentList.length;
  const totalQs = studentList.reduce((s, x) => s + x.totalQuestions, 0);
  const activeStudents = studentList.filter((x) => x.totalQuestions > 0);
  const avgAcc = activeStudents.length > 0
    ? Math.round(
        activeStudents.reduce((s, x) =>
          s + (x.totalCorrect / x.totalQuestions) * 100, 0
        ) / activeStudents.length
      )
    : 0;
  const activeToday = studentList.filter((s) => {
    if (!s.lastSeen) return false;
    return Date.now() - new Date(s.lastSeen).getTime() < 24 * 60 * 60 * 1000;
  }).length;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--ws-bg)' }}>

      {/* ── Top nav ── */}
      <div style={{
        background: 'var(--ws-surface)', borderBottom: '1px solid var(--ws-border)',
        padding: '14px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        flexWrap: 'wrap', gap: 12,
      }}>
        <div style={{
          fontFamily: 'var(--font-fredoka-one),cursive', fontSize: '1.2rem',
          background: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
          WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
        }}>
          👩‍🏫 Sikshya Admin
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          {/* Live indicator */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.75rem', color: '#34d399', fontWeight: 800 }}>
            <div style={{
              width: 8, height: 8, borderRadius: '50%', background: '#34d399',
              boxShadow: '0 0 0 0 rgba(52,211,153,0.4)',
              animation: 'pulse 2s infinite',
            }} />
            Live
          </div>
          <Link
            href="/"
            style={{
              fontSize: '0.82rem', fontWeight: 800, color: 'var(--ws-text-muted)',
              textDecoration: 'none', fontFamily: 'var(--font-nunito),sans-serif',
            }}
          >← Back to app</Link>
        </div>
      </div>

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '24px 16px' }}>

        {/* ── Summary strip ── */}
        <div style={{
          display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 24,
        }}>
          {[
            { label: 'Total students', value: totalStudents, emoji: '👩‍🎓', color: '#a78bfa' },
            { label: 'Active today', value: activeToday, emoji: '✅', color: '#34d399' },
            { label: 'Total questions answered', value: totalQs, emoji: '📝', color: '#60a5fa' },
            { label: 'Avg accuracy', value: `${avgAcc}%`, emoji: '🎯', color: avgAcc >= 80 ? '#34d399' : avgAcc >= 60 ? '#fbbf24' : '#f87171' },
          ].map(({ label, value, emoji, color }) => (
            <div key={label} style={{
              flex: '1 1 160px',
              background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
              borderRadius: 18, padding: '16px 20px',
              display: 'flex', alignItems: 'center', gap: 14,
            }}>
              <div style={{ fontSize: 28 }}>{emoji}</div>
              <div>
                <div style={{
                  fontFamily: 'var(--font-fredoka-one),cursive',
                  fontSize: '1.4rem', color, lineHeight: 1,
                }}>{value}</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--ws-text-muted)', fontWeight: 700, marginTop: 2 }}>
                  {label}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* ── Search + sort ── */}
        <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap' }}>
          <input
            type="search"
            placeholder="🔍  Search by name or email…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              flex: 1, minWidth: 200, padding: '10px 16px', borderRadius: 12,
              border: '1px solid var(--ws-border)', background: 'var(--ws-card)',
              color: 'var(--ws-text)', fontFamily: 'var(--font-nunito),sans-serif',
              fontSize: '0.88rem', outline: 'none',
            }}
          />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
            style={{
              padding: '10px 14px', borderRadius: 12, border: '1px solid var(--ws-border)',
              background: 'var(--ws-card)', color: 'var(--ws-text)',
              fontFamily: 'var(--font-nunito),sans-serif', fontSize: '0.85rem', cursor: 'pointer',
            }}
          >
            <option value="lastSeen">Sort: Last active</option>
            <option value="questions">Sort: Most questions</option>
            <option value="accuracy">Sort: Best accuracy</option>
            <option value="name">Sort: Name A–Z</option>
          </select>
        </div>

        {/* ── Student grid ── */}
        {dataLoading ? (
          // Skeleton placeholders — shown until first Firestore snapshot arrives
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: 16,
          }}>
            <style>{`
              @keyframes shimmer {
                0%   { background-position: -200% 0; }
                100% { background-position:  200% 0; }
              }
              @keyframes pulse {
                0%   { box-shadow: 0 0 0 0 rgba(52,211,153,0.4); }
                70%  { box-shadow: 0 0 0 8px rgba(52,211,153,0);  }
                100% { box-shadow: 0 0 0 0 rgba(52,211,153,0);    }
              }
            `}</style>
            {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
          </div>
        ) : visible.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '64px', color: 'var(--ws-text-muted)' }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>🕵️</div>
            <div style={{
              fontFamily: 'var(--font-fredoka-one),cursive',
              fontSize: '1.2rem', color: 'var(--ws-text)', marginBottom: 8,
            }}>
              {search ? 'No matches found' : 'No students yet'}
            </div>
            <p style={{ fontSize: '0.85rem' }}>
              {search
                ? 'Try a different name or email.'
                : 'Students will appear here after they log in and start studying.'}
            </p>
          </div>
        ) : (
          <>
            <style>{`
              @keyframes shimmer {
                0%   { background-position: -200% 0; }
                100% { background-position:  200% 0; }
              }
              @keyframes pulse {
                0%   { box-shadow: 0 0 0 0 rgba(52,211,153,0.4); }
                70%  { box-shadow: 0 0 0 8px rgba(52,211,153,0);  }
                100% { box-shadow: 0 0 0 0 rgba(52,211,153,0);    }
              }
            `}</style>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
              gap: 16,
            }}>
              {visible.map((s) => (
                <StudentCard key={s.uid} student={s} onClick={() => setSelected(s)} />
              ))}
            </div>
          </>
        )}

        {/* ── Footer note ── */}
        <div style={{
          marginTop: 32, padding: '12px 16px', borderRadius: 12,
          background: 'rgba(167,139,250,0.07)', border: '1px solid rgba(167,139,250,0.2)',
          fontSize: '0.75rem', color: 'var(--ws-text-muted)', lineHeight: 1.6,
        }}>
          💡 <strong>Tip:</strong> Click any student to see their full question-by-question breakdown.
          Questions highlighted in red are ones the student answered correctly less than 60% of the time —
          great candidates for targeted revision. This data is updated in real-time as students practice.
        </div>
      </div>
    </div>
  );
}
