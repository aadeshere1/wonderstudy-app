'use client';

import { useEffect, useState, useCallback } from 'react';
import type { StudentSummary, QuestionProgress, QuestionProgressMap } from '@/lib/admin/types';
import { getStudentQuestionProgress, fetchLessonItems } from '@/lib/admin/queries';
import { BADGE_MAP } from '@/lib/gamification/badges';
import { getXPProgress } from '@/lib/gamification/levels';

interface Props {
  student: StudentSummary;
  onBack: () => void;
}

interface LessonItem {
  question: string;
  answer: string;
  options: string[];
}

type LessonItems = Record<string, LessonItem>;

// ── Question detail modal ──────────────────────────────────────────────────

interface ModalProps {
  q: QuestionProgress;
  item: LessonItem | undefined;
  formatLessonId: (id: string) => string;
  onClose: () => void;
}

function QuestionModal({ q, item, formatLessonId, onClose }: ModalProps) {
  const pct = q.totalAttempts > 0
    ? Math.round((q.correctAttempts / q.totalAttempts) * 100) : 0;
  const accuracyColor = pct >= 80 ? '#34d399' : pct >= 60 ? '#fbbf24' : '#f87171';
  const isStruggling = pct < 60 && q.totalAttempts >= 2;

  // Close on Escape key
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  return (
    /* Backdrop */
    <div
      onClick={onClose}
      style={{
        position: 'fixed', inset: 0, zIndex: 1000,
        background: 'rgba(0,0,0,0.55)', backdropFilter: 'blur(4px)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: 20,
      }}
    >
      {/* Panel — stop propagation so clicking inside doesn't close */}
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
          borderRadius: 24, padding: 28, maxWidth: 520, width: '100%',
          maxHeight: '90vh', overflowY: 'auto',
          boxShadow: '0 24px 64px rgba(0,0,0,0.35)',
          fontFamily: 'var(--font-nunito),sans-serif',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 20, gap: 12 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
              <span style={{
                display: 'inline-block', padding: '2px 10px', borderRadius: 10,
                fontSize: '0.7rem', fontWeight: 800,
                background: q.section === 'challenge' ? 'rgba(251,191,36,0.15)' : 'rgba(167,139,250,0.15)',
                color: q.section === 'challenge' ? '#fbbf24' : '#a78bfa',
              }}>
                {q.section}
              </span>
              <span style={{ fontSize: '0.72rem', color: 'var(--ws-text-muted)' }}>
                {formatLessonId(q.lessonId)}
              </span>
            </div>
            {isStruggling && (
              <div style={{
                display: 'inline-flex', alignItems: 'center', gap: 4,
                background: 'rgba(248,113,113,0.12)', border: '1px solid rgba(248,113,113,0.3)',
                borderRadius: 10, padding: '2px 8px',
                fontSize: '0.7rem', color: '#f87171', fontWeight: 800,
              }}>
                ⚠️ Needs attention
              </div>
            )}
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'var(--ws-card2)', border: 'none', borderRadius: 10,
              width: 32, height: 32, cursor: 'pointer', fontSize: '1rem',
              color: 'var(--ws-text-muted)', flexShrink: 0,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}
          >✕</button>
        </div>

        {/* Question text */}
        <div style={{
          background: 'var(--ws-surface)', border: '1px solid var(--ws-border)',
          borderRadius: 16, padding: '16px 18px', marginBottom: 20,
        }}>
          <div style={{ fontSize: '0.68rem', color: 'var(--ws-text-muted)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 6 }}>
            Question
          </div>
          <div style={{ fontSize: '1rem', color: 'var(--ws-text)', lineHeight: 1.5, fontWeight: 700 }}>
            {item?.question ?? `${formatLessonId(q.lessonId)} · question #${q.index + 1}`}
          </div>
        </div>

        {/* Options */}
        {item?.options && item.options.length > 0 && (
          <div style={{ marginBottom: 20 }}>
            <div style={{ fontSize: '0.68rem', color: 'var(--ws-text-muted)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 10 }}>
              Options
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {item.options.map((opt) => {
                const isCorrect = opt === item.answer;
                return (
                  <div
                    key={opt}
                    style={{
                      padding: '10px 14px', borderRadius: 12,
                      border: `1.5px solid ${isCorrect ? 'rgba(52,211,153,0.5)' : 'var(--ws-border)'}`,
                      background: isCorrect ? 'rgba(52,211,153,0.08)' : 'var(--ws-surface)',
                      display: 'flex', alignItems: 'center', gap: 10,
                      fontSize: '0.88rem', color: isCorrect ? '#34d399' : 'var(--ws-text)',
                      fontWeight: isCorrect ? 800 : 500,
                    }}
                  >
                    <span style={{
                      width: 20, height: 20, borderRadius: '50%', flexShrink: 0,
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: '0.7rem', fontWeight: 900,
                      background: isCorrect ? 'rgba(52,211,153,0.2)' : 'rgba(255,255,255,0.05)',
                      color: isCorrect ? '#34d399' : 'var(--ws-text-muted)',
                    }}>
                      {isCorrect ? '✓' : ''}
                    </span>
                    {opt}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Answer (if no options) */}
        {item?.answer && (!item.options || item.options.length === 0) && (
          <div style={{ marginBottom: 20 }}>
            <div style={{ fontSize: '0.68rem', color: 'var(--ws-text-muted)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 6 }}>
              Correct answer
            </div>
            <div style={{
              padding: '10px 14px', borderRadius: 12,
              border: '1.5px solid rgba(52,211,153,0.5)',
              background: 'rgba(52,211,153,0.08)',
              fontSize: '0.95rem', color: '#34d399', fontWeight: 800,
            }}>
              ✓ {item.answer}
            </div>
          </div>
        )}

        {/* Stats */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 10,
          paddingTop: 16, borderTop: '1px solid var(--ws-border)',
        }}>
          {[
            { label: 'Attempts', value: q.totalAttempts, color: 'var(--ws-text)' },
            { label: 'Correct', value: q.correctAttempts, color: '#34d399' },
            { label: 'Wrong', value: q.wrongAttempts, color: '#f87171' },
            { label: 'Accuracy', value: `${pct}%`, color: accuracyColor },
          ].map(({ label, value, color }) => (
            <div key={label} style={{ textAlign: 'center' }}>
              <div style={{
                fontFamily: 'var(--font-fredoka-one),cursive',
                fontSize: '1.4rem', color, lineHeight: 1,
              }}>{value}</div>
              <div style={{ fontSize: '0.65rem', color: 'var(--ws-text-muted)', fontWeight: 700, marginTop: 2 }}>
                {label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────────────────

function AccuracyBar({ pct }: { pct: number }) {
  const color = pct >= 80 ? '#34d399' : pct >= 60 ? '#fbbf24' : '#f87171';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 120 }}>
      <div style={{
        flex: 1, height: 8, borderRadius: 4, background: 'var(--ws-card2)',
        overflow: 'hidden',
      }}>
        <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: 4 }} />
      </div>
      <span style={{ fontSize: '0.75rem', color, fontWeight: 700, minWidth: 36 }}>{pct}%</span>
    </div>
  );
}

function StatBox({ label, value, color }: { label: string; value: string | number; color?: string }) {
  return (
    <div style={{
      background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
      borderRadius: 16, padding: '14px 18px', textAlign: 'center', minWidth: 90,
    }}>
      <div style={{
        fontSize: '1.5rem', fontWeight: 900,
        fontFamily: 'var(--font-fredoka-one),cursive',
        color: color ?? 'var(--ws-text)',
      }}>{value}</div>
      <div style={{ fontSize: '0.68rem', color: 'var(--ws-text-muted)', marginTop: 2, fontWeight: 700 }}>{label}</div>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────

export default function StudentDetail({ student, onBack }: Props) {
  const [questionMap, setQuestionMap] = useState<QuestionProgressMap>({});
  const [lessonItems, setLessonItems] = useState<LessonItems>({});
  const [loading, setLoading] = useState(true);
  const [activeLesson, setActiveLesson] = useState<string | 'all'>('all');
  const [modalQ, setModalQ] = useState<QuestionProgress | null>(null);

  const closeModal = useCallback(() => setModalQ(null), []);

  useEffect(() => {
    getStudentQuestionProgress(student.uid).then(async (qmap) => {
      setQuestionMap(qmap);

      // Fetch question text for all unique lessons
      const lessonIds = [...new Set(Object.values(qmap).map((q) => q.lessonId))];
      const all: LessonItems = {};
      await Promise.all(
        lessonIds.map(async (lid) => {
          const items = await fetchLessonItems(lid);
          Object.assign(all, items);
        })
      );
      setLessonItems(all);
      setLoading(false);
    });
  }, [student.uid]);

  const accuracy = student.totalQuestions > 0
    ? Math.round((student.totalCorrect / student.totalQuestions) * 100) : 0;
  const xpProg = getXPProgress(student.totalXP);

  // Group questions by lesson
  const allQuestions = Object.values(questionMap);
  const lessonIds = [...new Set(allQuestions.map((q) => q.lessonId))].sort();
  const filtered = activeLesson === 'all'
    ? allQuestions
    : allQuestions.filter((q) => q.lessonId === activeLesson);

  // Sort: worst accuracy first (most need attention)
  const sorted = [...filtered].sort((a, b) => {
    const pA = a.totalAttempts > 0 ? a.correctAttempts / a.totalAttempts : 0;
    const pB = b.totalAttempts > 0 ? b.correctAttempts / b.totalAttempts : 0;
    return pA - pB;
  });

  function formatLessonId(id: string) {
    return id
      .replace(/^class-(\d+)-/, 'Class $1 › ')
      .replace(/-/g, ' ')
      .replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function relativeTime(iso: string) {
    if (!iso) return '—';
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

  return (
    <div style={{ minHeight: '100vh', background: 'var(--ws-bg)', paddingBottom: 48 }}>

      {/* ── Question detail modal ── */}
      {modalQ && (
        <QuestionModal
          q={modalQ}
          item={lessonItems[modalQ.cardId]}
          formatLessonId={formatLessonId}
          onClose={closeModal}
        />
      )}

      {/* ── Header ── */}
      <div style={{
        background: 'var(--ws-surface)', borderBottom: '1px solid var(--ws-border)',
        padding: '14px 24px', display: 'flex', alignItems: 'center', gap: 12,
      }}>
        <button
          onClick={onBack}
          style={{
            background: 'none', border: 'none', color: 'var(--ws-text-muted)',
            fontSize: '0.85rem', fontWeight: 800, cursor: 'pointer',
            fontFamily: 'var(--font-nunito),sans-serif',
          }}
        >← All students</button>
        <span style={{ color: 'var(--ws-border)' }}>|</span>
        <span style={{ color: 'var(--ws-text)', fontWeight: 800, fontSize: '0.95rem' }}>
          {student.name}
        </span>
      </div>

      <div style={{ maxWidth: 900, margin: '0 auto', padding: '24px 16px' }}>

        {/* ── Hero card ── */}
        <div style={{
          background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
          borderRadius: 24, padding: 24, marginBottom: 20,
          display: 'flex', gap: 20, alignItems: 'center', flexWrap: 'wrap',
        }}>
          {/* Avatar */}
          <div style={{ position: 'relative', flexShrink: 0 }}>
            {student.photoURL ? (
              <img
                src={student.photoURL}
                referrerPolicy="no-referrer"
                alt={student.name}
                style={{ width: 72, height: 72, borderRadius: '50%', objectFit: 'cover' }}
              />
            ) : (
              <div style={{
                width: 72, height: 72, borderRadius: '50%',
                background: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 28, fontWeight: 900, color: 'white',
              }}>
                {student.name[0]?.toUpperCase()}
              </div>
            )}
            <div style={{
              position: 'absolute', bottom: -4, right: -4,
              background: 'var(--ws-surface)', border: '2px solid var(--ws-border)',
              borderRadius: '50%', width: 28, height: 28,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 14,
            }}>
              {student.levelEmoji}
            </div>
          </div>

          {/* Info */}
          <div style={{ flex: 1, minWidth: 180 }}>
            <div style={{
              fontFamily: 'var(--font-fredoka-one),cursive',
              fontSize: '1.3rem', color: 'var(--ws-text)', lineHeight: 1.2,
            }}>
              {student.name}
            </div>
            <div style={{ color: 'var(--ws-text-muted)', fontSize: '0.82rem', margin: '2px 0' }}>
              {student.email}
            </div>
            <div style={{
              display: 'inline-flex', alignItems: 'center', gap: 6,
              background: 'rgba(167,139,250,0.12)', border: '1px solid rgba(167,139,250,0.3)',
              borderRadius: 20, padding: '3px 10px', fontSize: '0.78rem',
              color: '#a78bfa', fontWeight: 800, marginTop: 4,
            }}>
              {student.levelEmoji} Level {student.level} · {student.levelTitle}
            </div>
            {/* XP bar */}
            <div style={{ marginTop: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                flex: 1, height: 6, borderRadius: 3, background: 'var(--ws-card2)', overflow: 'hidden',
              }}>
                <div style={{
                  width: `${xpProg.pct}%`, height: '100%',
                  background: 'linear-gradient(90deg,#a78bfa,#60a5fa)', borderRadius: 3,
                }} />
              </div>
              <span style={{ fontSize: '0.7rem', color: 'var(--ws-text-muted)', fontWeight: 700 }}>
                {student.totalXP} XP
              </span>
            </div>
          </div>

          {/* Last seen */}
          <div style={{ textAlign: 'right', flexShrink: 0 }}>
            <div style={{ fontSize: '0.7rem', color: 'var(--ws-text-muted)' }}>Last active</div>
            <div style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--ws-text)' }}>
              {relativeTime(student.lastSeen)}
            </div>
            <div style={{ fontSize: '0.65rem', color: 'var(--ws-text-dim)', marginTop: 2 }}>
              Joined {new Date(student.joinedAt).toLocaleDateString()}
            </div>
          </div>
        </div>

        {/* ── Stats row ── */}
        <div style={{
          display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 20,
          justifyContent: 'flex-start',
        }}>
          <StatBox label="Questions" value={student.totalQuestions} color="#a78bfa" />
          <StatBox label="Correct" value={student.totalCorrect} color="#34d399" />
          <StatBox label="Accuracy" value={`${accuracy}%`} color={accuracy >= 80 ? '#34d399' : accuracy >= 60 ? '#fbbf24' : '#f87171'} />
          <StatBox label="Daily Streak" value={`🔥${student.dailyStreak}`} color="#f97316" />
          <StatBox label="Best Streak" value={student.maxStreak} color="#fbbf24" />
          <StatBox label="Total XP" value={student.totalXP} color="#60a5fa" />
        </div>

        {/* ── Session counts ── */}
        <div style={{
          background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
          borderRadius: 20, padding: '16px 20px', marginBottom: 20,
        }}>
          <div style={{
            fontSize: '0.75rem', fontWeight: 800, color: 'var(--ws-text-muted)',
            textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 12,
          }}>Sessions completed</div>
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
            {[
              { label: '📚 Teach', val: student.teachSessions },
              { label: '⚡ Practice', val: student.sessionsCompleted },
              { label: '🏆 Challenge', val: student.sessionsCompleted },
              { label: '🔁 Review', val: student.reviewSessions },
            ].map(({ label, val }) => (
              <div key={label} style={{ textAlign: 'center' }}>
                <div style={{
                  fontFamily: 'var(--font-fredoka-one),cursive',
                  fontSize: '1.6rem', color: 'var(--ws-text)',
                }}>{val}</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--ws-text-muted)', fontWeight: 700 }}>
                  {label}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Badges ── */}
        {student.badgesEarned.length > 0 && (
          <div style={{
            background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
            borderRadius: 20, padding: '16px 20px', marginBottom: 20,
          }}>
            <div style={{
              fontSize: '0.75rem', fontWeight: 800, color: 'var(--ws-text-muted)',
              textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 12,
            }}>Badges earned ({student.badgesEarned.length})</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {student.badgesEarned.map((id) => {
                const badge = BADGE_MAP[id];
                if (!badge) return null;
                return (
                  <div key={id} title={badge.description} style={{
                    display: 'flex', alignItems: 'center', gap: 5,
                    background: 'var(--ws-card2)', border: '1px solid var(--ws-border)',
                    borderRadius: 20, padding: '4px 10px', fontSize: '0.78rem',
                    color: 'var(--ws-text)', fontWeight: 700,
                  }}>
                    {badge.emoji} {badge.name}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── Question accuracy breakdown ── */}
        <div style={{
          background: 'var(--ws-card)', border: '1px solid var(--ws-border)',
          borderRadius: 20, padding: '16px 20px',
        }}>
          <div style={{
            fontSize: '0.75rem', fontWeight: 800, color: 'var(--ws-text-muted)',
            textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 14,
          }}>
            Question accuracy
            {sorted.length > 0 && (
              <span style={{ fontWeight: 400, textTransform: 'none', marginLeft: 8, fontSize: '0.7rem' }}>
                — click any row to see full question &amp; answer
              </span>
            )}
          </div>

          {/* Lesson filter */}
          {lessonIds.length > 1 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
              {(['all', ...lessonIds] as const).map((lid) => (
                <button
                  key={lid}
                  onClick={() => setActiveLesson(lid)}
                  style={{
                    padding: '4px 12px', borderRadius: 20, border: 'none', cursor: 'pointer',
                    fontFamily: 'var(--font-nunito),sans-serif', fontWeight: 800, fontSize: '0.75rem',
                    background: activeLesson === lid
                      ? 'linear-gradient(135deg,#a78bfa,#60a5fa)'
                      : 'var(--ws-card2)',
                    color: activeLesson === lid ? 'white' : 'var(--ws-text-muted)',
                    transition: 'all 0.15s',
                  }}
                >
                  {lid === 'all' ? 'All lessons' : formatLessonId(lid)}
                </button>
              ))}
            </div>
          )}

          {loading ? (
            <div style={{ textAlign: 'center', padding: '32px', color: 'var(--ws-text-muted)' }}>
              Loading question data…
            </div>
          ) : sorted.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '32px', color: 'var(--ws-text-muted)' }}>
              No questions answered yet.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--ws-border)' }}>
                    {['Question', 'Section', 'Attempts', '✓ Correct', '✗ Wrong', 'Accuracy'].map((h) => (
                      <th key={h} style={{
                        padding: '6px 10px', textAlign: 'left',
                        color: 'var(--ws-text-muted)', fontWeight: 800,
                        fontSize: '0.7rem', textTransform: 'uppercase', whiteSpace: 'nowrap',
                      }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {sorted.map((q) => {
                    const pct = q.totalAttempts > 0
                      ? Math.round((q.correctAttempts / q.totalAttempts) * 100) : 0;
                    const qText = lessonItems[q.cardId];
                    const isStruggling = pct < 60 && q.totalAttempts >= 2;
                    return (
                      <tr
                        key={q.cardId}
                        onClick={() => setModalQ(q)}
                        title="Click to see full question and answer"
                        style={{
                          borderBottom: '1px solid var(--ws-border)',
                          background: isStruggling ? 'rgba(248,113,113,0.05)' : 'transparent',
                          cursor: 'pointer',
                          transition: 'background 0.12s',
                        }}
                        onMouseEnter={(e) => {
                          (e.currentTarget as HTMLElement).style.background =
                            isStruggling ? 'rgba(248,113,113,0.12)' : 'rgba(167,139,250,0.06)';
                        }}
                        onMouseLeave={(e) => {
                          (e.currentTarget as HTMLElement).style.background =
                            isStruggling ? 'rgba(248,113,113,0.05)' : 'transparent';
                        }}
                      >
                        <td style={{ padding: '9px 10px', color: 'var(--ws-text)', maxWidth: 280 }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                            {qText ? (
                              <span>
                                {qText.question.length > 65
                                  ? qText.question.slice(0, 63) + '…'
                                  : qText.question}
                              </span>
                            ) : (
                              <span style={{ color: 'var(--ws-text-muted)', fontStyle: 'italic' }}>
                                {formatLessonId(q.lessonId)} #{q.index + 1}
                              </span>
                            )}
                            <span style={{
                              flexShrink: 0, fontSize: '0.65rem', color: 'var(--ws-text-muted)',
                              opacity: 0.6,
                            }}>↗</span>
                          </div>
                        </td>
                        <td style={{ padding: '9px 10px', whiteSpace: 'nowrap' }}>
                          <span style={{
                            display: 'inline-block', padding: '2px 8px', borderRadius: 10,
                            fontSize: '0.7rem', fontWeight: 800,
                            background: q.section === 'challenge'
                              ? 'rgba(251,191,36,0.15)' : 'rgba(167,139,250,0.15)',
                            color: q.section === 'challenge' ? '#fbbf24' : '#a78bfa',
                          }}>
                            {q.section}
                          </span>
                        </td>
                        <td style={{ padding: '9px 10px', color: 'var(--ws-text)', textAlign: 'center' }}>
                          {q.totalAttempts}
                        </td>
                        <td style={{ padding: '9px 10px', color: '#34d399', textAlign: 'center', fontWeight: 800 }}>
                          {q.correctAttempts}
                        </td>
                        <td style={{ padding: '9px 10px', color: '#f87171', textAlign: 'center', fontWeight: 800 }}>
                          {q.wrongAttempts}
                        </td>
                        <td style={{ padding: '9px 10px', minWidth: 140 }}>
                          <AccuracyBar pct={pct} />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
