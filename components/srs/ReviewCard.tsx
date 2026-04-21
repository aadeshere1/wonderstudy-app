'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getDueCards } from '@/lib/srs/store';

interface Props {
  classNum: string;
  subject: string;
  lesson: string;
  lessonId: string;
}

export default function ReviewCard({ classNum, subject, lesson, lessonId }: Props) {
  const { user } = useAuth();
  const [dueCount, setDueCount] = useState<number | null>(null);

  useEffect(() => {
    getDueCards(user?.uid ?? null, lessonId).then((cards) => {
      setDueCount(cards.length);
    });
  }, [user, lessonId]);

  const hasDue = dueCount !== null && dueCount > 0;

  return (
    <Link
      href={`/class/${classNum}/${subject}/${lesson}/review`}
      className="block group"
    >
      <div
        className="rounded-2xl p-px transition-all duration-200 group-hover:-translate-y-0.5"
        style={{ border: '1px solid var(--ws-border)', boxShadow: '0 4px 20px rgba(99,102,241,0.3)' }}
      >
        <div
          className="rounded-2xl flex items-center gap-5 px-6 py-5"
          style={{ background: 'var(--ws-card-inner)' }}
        >
          {/* Icon circle */}
          <div
            className="flex-shrink-0 w-14 h-14 rounded-2xl flex items-center justify-center text-3xl"
            style={{
              background: 'linear-gradient(135deg,#6366f1,#a78bfa)',
              boxShadow: '0 4px 14px rgba(99,102,241,0.4)',
            }}
          >
            🔁
          </div>

          {/* Text */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-0.5">
              <span className="font-display text-xl text-theme">Review</span>

              {/* Due badge */}
              {dueCount === null ? (
                <span
                  className="text-xs font-bold px-2 py-0.5 rounded-full"
                  style={{ background: 'rgba(99,102,241,0.15)', color: '#a5b4fc' }}
                >
                  …
                </span>
              ) : hasDue ? (
                <span
                  className="text-xs font-bold px-2 py-0.5 rounded-full"
                  style={{ background: 'rgba(251,191,36,0.2)', color: '#fbbf24' }}
                >
                  {dueCount} due
                </span>
              ) : (
                <span
                  className="text-xs font-bold px-2 py-0.5 rounded-full"
                  style={{ background: 'rgba(52,211,153,0.15)', color: '#34d399' }}
                >
                  All caught up ✓
                </span>
              )}
            </div>
            <p className="text-xs" style={{ color: 'var(--ws-text-muted)' }}>
              Revisit cards using spaced repetition
            </p>
          </div>

          {/* Arrow */}
          <div
            className="flex-shrink-0 font-display text-xl transition-transform duration-200 group-hover:translate-x-1"
            style={{ color: 'var(--ws-text-dim)' }}
          >
            →
          </div>
        </div>
      </div>
    </Link>
  );
}
