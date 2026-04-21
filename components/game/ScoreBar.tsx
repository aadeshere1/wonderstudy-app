'use client';

import { ReactNode } from 'react';

export interface ScoreBarProps {
  score: number;
  streak: number;
  correct: number;
  wrong: number;
  playerName?: string;
  playerColor?: string;
  questionCount?: number;
  currentQuestion?: number;
  showStreak?: boolean;
  extra?: ReactNode;
}

export const ScoreBar = ({
  score,
  streak,
  correct,
  wrong,
  playerName,
  showStreak = true,
  extra,
}: ScoreBarProps) => {
  return (
    <div
      className="flex items-center justify-between px-4 py-2 w-full"
      style={{ background: 'var(--ws-surface)', borderBottom: '1px solid var(--ws-border)' }}
    >
      {/* Score */}
      <div className="text-center min-w-[60px]">
        <div className="text-xs uppercase tracking-widest" style={{ color: 'var(--ws-text-dim)', letterSpacing: '1.5px' }}>Score</div>
        <div className="font-display text-2xl" style={{ color: '#fbbf24' }}>{score}</div>
      </div>

      {/* Player name / turn */}
      <div className="flex-1 flex justify-center px-4">
        {playerName ? (
          <div
            className="px-5 py-1.5 rounded-3xl font-display text-sm text-center"
            style={{ background: 'linear-gradient(135deg,#a78bfa,#f87171)', color: 'white' }}
          >
            {playerName}
          </div>
        ) : (
          <div
            className="px-5 py-1.5 rounded-3xl font-display text-sm"
            style={{ background: 'linear-gradient(135deg,#a78bfa,#f87171)', color: 'white' }}
          >
            Go! 🎯
          </div>
        )}
      </div>

      {/* Streak */}
      <div className="text-center min-w-[60px]">
        <div className="text-xs uppercase tracking-widest" style={{ color: 'var(--ws-text-dim)', letterSpacing: '1.5px' }}>Streak</div>
        <div className="font-display text-2xl flex items-center justify-center gap-1" style={{ color: '#34d399' }}>
          {showStreak && streak > 0 ? (
            <><span>🔥</span><span>{streak}</span></>
          ) : (
            <span>0</span>
          )}
        </div>
      </div>

      {/* Extra Content */}
      {extra && <div className="w-full flex justify-center mt-1">{extra}</div>}
    </div>
  );
};
