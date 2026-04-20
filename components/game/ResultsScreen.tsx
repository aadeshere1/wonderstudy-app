'use client';

import { Button } from '@/components/ui';

export interface ResultsScreenProps {
  score: number;
  correct: number;
  wrong: number;
  streak: number;
  playerName?: string;
  playerColor?: string;
  accuracy?: number;
  timeSpent?: number;
  questionsCount?: number;
  message?: string;
  onRestart?: () => void;
  onExit?: () => void;
  showConfetti?: boolean;
}

const colorMap: Record<string, string> = {
  0: 'from-blue to-purple',
  1: 'from-coral to-pink',
  2: 'from-mint to-blue',
  3: 'from-gold to-coral',
  4: 'from-purple to-blue',
  5: 'from-pink to-purple',
};

export const ResultsScreen = ({
  score,
  correct,
  wrong,
  streak,
  playerName,
  playerColor = '0',
  accuracy,
  timeSpent,
  questionsCount,
  message,
  onRestart,
  onExit,
  showConfetti = true,
}: ResultsScreenProps) => {
  const total = correct + wrong;
  const finalAccuracy = accuracy !== undefined ? accuracy : (total > 0 ? Math.round((correct / total) * 100) : 0);
  const gradientClass = colorMap[playerColor] || colorMap['0'];

  // Performance message
  let performanceMsg = 'Good job! 🎉';
  if (finalAccuracy === 100) {
    performanceMsg = 'Perfect! 🌟';
  } else if (finalAccuracy >= 80) {
    performanceMsg = 'Excellent! ⭐';
  } else if (finalAccuracy >= 60) {
    performanceMsg = 'Great effort! 💪';
  } else if (finalAccuracy >= 40) {
    performanceMsg = 'Keep practicing! 📚';
  } else {
    performanceMsg = 'Try again! 🚀';
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-8 py-8 px-4">
      {/* Celebration Icon */}
      <div className="text-6xl animate-bounce">{finalAccuracy === 100 ? '🏆' : '🎉'}</div>

      {/* Main Score Display */}
      <div className={`bg-gradient-to-r ${gradientClass} bg-clip-text text-transparent`}>
        <div className="text-7xl font-black">
          {score}
        </div>
      </div>

      {/* Performance Message */}
      <div className="text-3xl font-bold text-theme text-center">
        {message || performanceMsg}
      </div>

      {/* Player Name */}
      {playerName && (
        <div className="text-xl text-muted">
          Great work, <span className="text-theme font-bold">{playerName}</span>!
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 max-w-sm w-full">
        {/* Correct */}
        <div className="bg-mint/20 border border-mint rounded-lg p-4 text-center">
          <div className="text-3xl font-bold text-mint">✓</div>
          <div className="text-sm text-muted mt-2">Correct</div>
          <div className="text-2xl font-black text-theme">{correct}</div>
        </div>

        {/* Wrong */}
        <div className="bg-coral/20 border border-coral rounded-lg p-4 text-center">
          <div className="text-3xl font-bold text-coral">✗</div>
          <div className="text-sm text-muted mt-2">Wrong</div>
          <div className="text-2xl font-black text-theme">{wrong}</div>
        </div>

        {/* Accuracy */}
        <div className="bg-blue/20 border border-blue rounded-lg p-4 text-center">
          <div className="text-3xl font-bold text-blue">%</div>
          <div className="text-sm text-muted mt-2">Accuracy</div>
          <div className="text-2xl font-black text-theme">{finalAccuracy}%</div>
        </div>

        {/* Streak */}
        <div className="bg-gold/20 border border-gold rounded-lg p-4 text-center">
          <div className="text-3xl font-bold text-gold">🔥</div>
          <div className="text-sm text-muted mt-2">Best Streak</div>
          <div className="text-2xl font-black text-theme">{streak}</div>
        </div>
      </div>

      {/* Additional Stats */}
      <div className="flex flex-col gap-2 text-center text-sm">
        {questionsCount && (
          <div className="text-muted">
            Answered <span className="text-theme font-bold">{questionsCount}</span> questions
          </div>
        )}
        {timeSpent && (
          <div className="text-muted">
            Time spent: <span className="text-theme font-bold">{timeSpent}s</span>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 flex-wrap justify-center max-w-sm w-full">
        {onRestart && (
          <Button variant="primary" size="lg" onClick={onRestart} className="flex-1">
            🔄 Try Again
          </Button>
        )}
        {onExit && (
          <Button variant="secondary" size="lg" onClick={onExit} className="flex-1">
            ← Home
          </Button>
        )}
      </div>
    </div>
  );
};
