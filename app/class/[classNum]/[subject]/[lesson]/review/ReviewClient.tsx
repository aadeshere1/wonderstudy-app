'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getDueCards, recordAnswer } from '@/lib/srs/store';
import { applyAnswer } from '@/lib/srs/algorithm';
import type { SRSCard } from '@/lib/srs/types';
import type { LessonData } from '@/lib/engine/types';
import { OptionsGrid } from '@/components/game';
import { ConfettiOverlay } from '@/components/layout';

interface Props {
  classNum: string;
  subject: string;
  lesson: string;
  initialLesson: LessonData | null;
}

type ReviewState = 'loading' | 'empty' | 'question' | 'answered' | 'done';

interface ReviewQuestion {
  card: SRSCard;
  question: string;
  answer: string;
  options: string[];
  explanation: string;
  hint?: string;
}

function buildQuestions(lesson: LessonData, dueCards: SRSCard[]): ReviewQuestion[] {
  const questions: ReviewQuestion[] = [];

  for (const card of dueCards) {
    const section = card.section as 'practice' | 'challenge';
    const items = lesson[section]?.items;
    if (!items || card.index >= items.length) continue;

    const item = items[card.index] as any;
    if (!item?.question || !item?.answer || !item?.options) continue;

    questions.push({
      card,
      question:    item.question,
      answer:      item.answer,
      options:     item.options,
      explanation: item.explanation || '',
      hint:        item.hint,
    });
  }

  // Shuffle
  return questions.sort(() => Math.random() - 0.5);
}

export default function ReviewClient({ classNum, subject, lesson, initialLesson }: Props) {
  const router = useRouter();
  const { user } = useAuth();

  const [state, setState]         = useState<ReviewState>('loading');
  const [questions, setQuestions] = useState<ReviewQuestion[]>([]);
  const [current, setCurrent]     = useState(0);
  const [selected, setSelected]   = useState<string | null>(null);
  const [correct, setCorrect]     = useState<boolean | null>(null);
  const [hintShown, setHintShown] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, wrong: 0 });

  useEffect(() => {
    if (!initialLesson) { setState('empty'); return; }

    getDueCards(user?.uid ?? null, initialLesson.id).then((due) => {
      if (due.length === 0) { setState('empty'); return; }
      const qs = buildQuestions(initialLesson, due);
      if (qs.length === 0) { setState('empty'); return; }
      setQuestions(qs);
      setState('question');
    });
  }, [initialLesson, user]);

  const handleAnswer = useCallback(async (option: string) => {
    if (state !== 'question' || !initialLesson) return;
    const q = questions[current];
    const isCorrect = option === q.answer;

    setSelected(option);
    setCorrect(isCorrect);
    setState('answered');

    if (isCorrect) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 1200);
      setSessionStats(s => ({ ...s, correct: s.correct + 1 }));
    } else {
      setSessionStats(s => ({ ...s, wrong: s.wrong + 1 }));
    }

    // Save to SRS store
    await recordAnswer(
      user?.uid ?? null,
      q.card.lessonId,
      q.card.section,
      q.card.index,
      isCorrect,
      hintShown,
    );
  }, [state, questions, current, user, initialLesson, hintShown]);

  const handleNext = useCallback(() => {
    if (current + 1 >= questions.length) {
      setState('done');
    } else {
      setCurrent(c => c + 1);
      setSelected(null);
      setCorrect(null);
      setHintShown(false);
      setState('question');
    }
  }, [current, questions.length]);

  // ── Loading ──────────────────────────────────────────────────────────────
  if (state === 'loading') {
    return (
      <div className="fixed inset-0 flex items-center justify-center" style={{ background: '#0d0d1a' }}>
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">🔁</div>
          <div className="font-display text-2xl" style={{ color: '#a78bfa' }}>Loading your review…</div>
        </div>
      </div>
    );
  }

  // ── Empty (nothing due) ──────────────────────────────────────────────────
  if (state === 'empty') {
    return (
      <div className="fixed inset-0 flex items-center justify-center p-4" style={{ background: '#0d0d1a' }}>
        <div className="text-center max-w-sm">
          <div className="text-6xl mb-4">✅</div>
          <div className="font-display text-2xl text-white mb-2">Nothing due!</div>
          <p className="text-sm mb-6" style={{ color: 'rgba(240,244,255,0.5)' }}>
            You&apos;re all caught up. Practice more questions to add cards to your review queue.
          </p>
          <Link
            href={`/class/${classNum}/${subject}/${lesson}`}
            style={{
              display: 'inline-block', padding: '10px 28px', borderRadius: 14,
              background: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
              color: 'white', fontFamily: 'var(--font-fredoka-one),cursive',
              fontSize: '1rem', textDecoration: 'none',
            }}
          >
            ← Back to lesson
          </Link>
        </div>
      </div>
    );
  }

  // ── Done ─────────────────────────────────────────────────────────────────
  if (state === 'done') {
    const total   = sessionStats.correct + sessionStats.wrong;
    const pct     = Math.round((sessionStats.correct / total) * 100);
    const emoji   = pct === 100 ? '🏆' : pct >= 70 ? '🎉' : '💪';

    return (
      <div className="fixed inset-0 flex items-center justify-center p-4" style={{ background: '#0d0d1a' }}>
        <ConfettiOverlay active={pct === 100} />
        <div className="text-center max-w-sm w-full">
          <div className="text-7xl mb-4">{emoji}</div>
          <div className="font-display text-3xl text-white mb-2">Review done!</div>
          <div className="font-display text-xl mb-6" style={{ color: '#fbbf24' }}>{pct}% correct</div>

          <div className="rounded-2xl p-5 mb-6 flex justify-around" style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}>
            <div className="text-center">
              <div className="font-display text-3xl" style={{ color: '#34d399' }}>{sessionStats.correct}</div>
              <div className="text-xs mt-1" style={{ color: 'rgba(240,244,255,0.45)' }}>Correct</div>
            </div>
            <div className="text-center">
              <div className="font-display text-3xl" style={{ color: '#f87171' }}>{sessionStats.wrong}</div>
              <div className="text-xs mt-1" style={{ color: 'rgba(240,244,255,0.45)' }}>Wrong</div>
            </div>
            <div className="text-center">
              <div className="font-display text-3xl" style={{ color: '#a78bfa' }}>{total}</div>
              <div className="text-xs mt-1" style={{ color: 'rgba(240,244,255,0.45)' }}>Total</div>
            </div>
          </div>

          <div className="flex flex-col gap-3">
            <Link
              href={`/class/${classNum}/${subject}/${lesson}`}
              style={{
                display: 'block', padding: '12px', borderRadius: 14, textAlign: 'center',
                background: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
                color: 'white', fontFamily: 'var(--font-fredoka-one),cursive',
                fontSize: '1rem', textDecoration: 'none',
              }}
            >
              ← Back to lesson
            </Link>
            <button
              onClick={() => {
                setCurrent(0); setSelected(null); setCorrect(null);
                setHintShown(false); setSessionStats({ correct: 0, wrong: 0 });
                setState('loading');
              }}
              style={{
                padding: '10px', borderRadius: 14, border: '1px solid rgba(255,255,255,0.15)',
                background: 'transparent', color: 'rgba(240,244,255,0.6)',
                fontFamily: 'var(--font-nunito),sans-serif', fontWeight: 800,
                fontSize: '0.9rem', cursor: 'pointer',
              }}
            >
              🔁 Review again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── Question / Answered ──────────────────────────────────────────────────
  const q = questions[current];
  const progress = Math.round(((current) / questions.length) * 100);

  return (
    <div className="fixed inset-0 flex flex-col overflow-hidden" style={{ background: '#0d0d1a' }}>
      <ConfettiOverlay active={showConfetti} />

      {/* Top bar */}
      <div className="flex-shrink-0 flex items-center justify-between px-4 py-3"
        style={{ background: '#161628', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <button
          onClick={() => router.push(`/class/${classNum}/${subject}/${lesson}`)}
          style={{ background: 'none', border: 'none', color: 'rgba(240,244,255,0.45)', fontWeight: 800, fontSize: '0.85rem', cursor: 'pointer', fontFamily: 'var(--font-nunito),sans-serif' }}
        >
          ← Back
        </button>
        <div className="font-display text-base" style={{ color: '#a78bfa' }}>
          🔁 Review
        </div>
        <div className="font-display text-sm" style={{ color: 'rgba(240,244,255,0.45)' }}>
          {current + 1} / {questions.length}
        </div>
      </div>

      {/* Progress bar */}
      <div className="flex-shrink-0 h-1.5 mx-4 mt-1 rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.07)' }}>
        <div className="h-full rounded-full transition-all duration-500"
          style={{ width: `${progress}%`, background: 'linear-gradient(90deg,#a78bfa,#34d399)' }} />
      </div>

      {/* Question */}
      <div className="flex-1 flex flex-col items-center justify-center gap-5 px-4 overflow-y-auto py-4">
        {/* SRS interval badge */}
        <div className="text-xs px-3 py-1 rounded-full" style={{ background: 'rgba(167,139,250,0.15)', color: '#a78bfa' }}>
          📅 Due today · interval was {q.card.interval}d
        </div>

        <div
          className="w-full max-w-lg rounded-2xl p-5 text-center font-display text-lg text-white leading-snug"
          style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}
        >
          {q.question}
        </div>

        {/* Hint */}
        {!hintShown && q.hint && state === 'question' && (
          <button
            onClick={() => setHintShown(true)}
            style={{ fontSize: '0.78rem', color: '#fbbf24', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 800, fontFamily: 'var(--font-nunito),sans-serif' }}
          >
            💡 Show hint
          </button>
        )}
        {hintShown && q.hint && (
          <div className="text-sm px-4 py-2 rounded-xl" style={{ background: 'rgba(251,191,36,0.1)', color: '#fbbf24', border: '1px solid rgba(251,191,36,0.25)' }}>
            💡 {q.hint}
          </div>
        )}

        {/* Options */}
        <div className="w-full max-w-lg">
          <OptionsGrid
            options={q.options}
            onSelect={handleAnswer}
            columns={q.options.length <= 2 ? 1 : 2}
            disabled={state === 'answered'}
            correctOption={state === 'answered' ? q.answer : undefined}
            wrongOption={state === 'answered' && selected !== q.answer ? selected ?? undefined : undefined}
          />
        </div>

        {/* Explanation after answer */}
        {state === 'answered' && q.explanation && (
          <div className="w-full max-w-lg rounded-xl px-4 py-3 text-sm"
            style={{ background: correct ? 'rgba(52,211,153,0.1)' : 'rgba(248,113,113,0.1)', border: `1px solid ${correct ? 'rgba(52,211,153,0.3)' : 'rgba(248,113,113,0.3)'}`, color: 'rgba(240,244,255,0.8)' }}>
            {correct ? '✅' : '❌'} {q.explanation}
          </div>
        )}
      </div>

      {/* Next button */}
      {state === 'answered' && (
        <div className="flex-shrink-0 px-4 py-4" style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
          <button
            onClick={handleNext}
            style={{
              width: '100%', padding: '13px', borderRadius: 14, border: 'none',
              background: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
              color: 'white', fontFamily: 'var(--font-fredoka-one),cursive',
              fontSize: '1.1rem', cursor: 'pointer',
              boxShadow: '0 4px 15px rgba(167,139,250,0.35)',
            }}
          >
            {current + 1 >= questions.length ? '🏁 See results' : 'Next →'}
          </button>
        </div>
      )}
    </div>
  );
}
