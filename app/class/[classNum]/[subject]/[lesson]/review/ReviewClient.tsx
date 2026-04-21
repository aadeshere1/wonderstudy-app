'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getDueCards, recordAnswer } from '@/lib/srs/store';
import { applyAnswer } from '@/lib/srs/algorithm';
import { shuffleArray } from '@/lib/utils/helpers';
import type { SRSCard } from '@/lib/srs/types';
import type { LessonData } from '@/lib/engine/types';
import { OptionsGrid } from '@/components/game';
import { ConfettiOverlay } from '@/components/layout';
import { useGamification } from '@/contexts/GamificationContext';
import { recordQuestionProgress } from '@/lib/admin/queries';

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
      // Shuffle options so the correct answer isn't always in the same slot
      options:     shuffleArray([...item.options]),
      explanation: item.explanation || '',
      hint:        item.hint,
    });
  }

  // Shuffle question order with a proper Fisher-Yates shuffle
  return shuffleArray(questions);
}

export default function ReviewClient({ classNum, subject, lesson, initialLesson }: Props) {
  const router = useRouter();
  const { user } = useAuth();
  const { onAnswer: gamOnAnswer, onSessionEnd } = useGamification();

  const [state, setState]         = useState<ReviewState>('loading');
  const [questions, setQuestions] = useState<ReviewQuestion[]>([]);
  const [current, setCurrent]     = useState(0);
  const [selected, setSelected]   = useState<string | null>(null);
  const [correct, setCorrect]     = useState<boolean | null>(null);
  const [hintShown, setHintShown] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, wrong: 0 });

  // Running streak within this review session (for XP bonus calculation)
  const reviewStreakRef = useRef(0);

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
      reviewStreakRef.current += 1;
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 1200);
      setSessionStats(s => ({ ...s, correct: s.correct + 1 }));
    } else {
      reviewStreakRef.current = 0;
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

    // Record XP + badge progress
    gamOnAnswer(isCorrect, 'review', reviewStreakRef.current).catch(console.error);
    // Record per-question accuracy for admin dashboard
    if (user) {
      recordQuestionProgress(user, q.card.lessonId, q.card.section, q.card.index, isCorrect)
        .catch(console.error);
    }
  }, [state, questions, current, user, initialLesson, hintShown, gamOnAnswer]);

  const handleNext = useCallback(() => {
    if (current + 1 >= questions.length) {
      onSessionEnd('review').catch(console.error);
      setState('done');
    } else {
      setCurrent(c => c + 1);
      setSelected(null);
      setCorrect(null);
      setHintShown(false);
      setState('question');
    }
  }, [current, questions.length, onSessionEnd]);

  // ── Loading ──────────────────────────────────────────────────────────────
  if (state === 'loading') {
    return (
      <div className="fixed inset-0 flex items-center justify-center" style={{ background: 'var(--ws-bg)' }}>
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
      <div className="fixed inset-0 flex items-center justify-center p-4" style={{ background: 'var(--ws-bg)' }}>
        <div className="text-center max-w-sm">
          <div className="text-6xl mb-4">✅</div>
          <div className="font-display text-2xl text-theme mb-2">Nothing due!</div>
          <p className="text-sm mb-6" style={{ color: 'var(--ws-text-muted)' }}>
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
      <div className="fixed inset-0 flex items-center justify-center p-4" style={{ background: 'var(--ws-bg)' }}>
        <ConfettiOverlay active={pct === 100} />
        <div className="text-center max-w-sm w-full">
          <div className="text-7xl mb-4">{emoji}</div>
          <div className="font-display text-3xl text-theme mb-2">Review done!</div>
          <div className="font-display text-xl mb-6" style={{ color: '#fbbf24' }}>{pct}% correct</div>

          <div className="rounded-2xl p-5 mb-6 flex justify-around" style={{ background: 'var(--ws-card)', border: '1px solid var(--ws-border)' }}>
            <div className="text-center">
              <div className="font-display text-3xl" style={{ color: '#34d399' }}>{sessionStats.correct}</div>
              <div className="text-xs mt-1" style={{ color: 'var(--ws-text-muted)' }}>Correct</div>
            </div>
            <div className="text-center">
              <div className="font-display text-3xl" style={{ color: '#f87171' }}>{sessionStats.wrong}</div>
              <div className="text-xs mt-1" style={{ color: 'var(--ws-text-muted)' }}>Wrong</div>
            </div>
            <div className="text-center">
              <div className="font-display text-3xl" style={{ color: '#a78bfa' }}>{total}</div>
              <div className="text-xs mt-1" style={{ color: 'var(--ws-text-muted)' }}>Total</div>
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
                reviewStreakRef.current = 0;
                setState('loading');
              }}
              style={{
                padding: '10px', borderRadius: 14, border: '1px solid var(--ws-border)',
                background: 'transparent', color: 'var(--ws-text-muted)',
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
    <div className="fixed inset-0 flex flex-col overflow-hidden" style={{ background: 'var(--ws-bg)' }}>
      <ConfettiOverlay active={showConfetti} />

      {/* Top bar */}
      <div className="flex-shrink-0 flex items-center justify-between px-4 py-3"
        style={{ background: 'var(--ws-surface)', borderBottom: '1px solid var(--ws-border)' }}>
        <button
          onClick={() => router.push(`/class/${classNum}/${subject}/${lesson}`)}
          style={{ background: 'none', border: 'none', color: 'var(--ws-text-muted)', fontWeight: 800, fontSize: '0.85rem', cursor: 'pointer', fontFamily: 'var(--font-nunito),sans-serif' }}
        >
          ← Back
        </button>
        <div className="font-display text-base" style={{ color: '#a78bfa' }}>
          🔁 Review
        </div>
        <div className="font-display text-sm" style={{ color: 'var(--ws-text-muted)' }}>
          {current + 1} / {questions.length}
        </div>
      </div>

      {/* Progress bar */}
      <div className="flex-shrink-0 h-1.5 mx-4 mt-1 rounded-full overflow-hidden" style={{ background: 'var(--ws-border)' }}>
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
          className="w-full max-w-lg rounded-2xl p-5 text-center font-display text-lg text-theme leading-snug"
          style={{ background: 'var(--ws-card)', border: '1px solid var(--ws-border)' }}
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
            style={{ background: correct ? 'rgba(52,211,153,0.1)' : 'rgba(248,113,113,0.1)', border: `1px solid ${correct ? 'rgba(52,211,153,0.3)' : 'rgba(248,113,113,0.3)'}`, color: 'var(--ws-text)' }}>
            {correct ? '✅' : '❌'} {q.explanation}
          </div>
        )}
      </div>

      {/* Next button */}
      {state === 'answered' && (
        <div className="flex-shrink-0 px-4 py-4" style={{ borderTop: '1px solid var(--ws-border)' }}>
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
