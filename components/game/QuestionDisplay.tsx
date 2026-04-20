'use client';

export interface QuestionDisplayProps {
  displayText: string;
  spokenText?: string;
  icon?: string;
  size?: 'sm' | 'md' | 'lg';
  isAnimating?: boolean;
  onSpeak?: () => void;
}

/**
 * Tries to render a math expression like "7 × 8 = ?" with coloured parts.
 * Falls back to plain text when the pattern doesn't match.
 */
function MathQuestion({ text }: { text: string }) {
  // Match: <A> <op> <B> = <answer>  where op can be ×, ÷, +, -, x, *
  const match = text.match(/^(.+?)\s*([×÷+\-x*\/])\s*(.+?)\s*=\s*(.+)$/);
  if (match) {
    const [, a, op, b, ans] = match;
    return (
      <div
        className="text-center leading-none"
        style={{ fontFamily: 'var(--font-fredoka-one), cursive', fontSize: 'clamp(2.4rem,10vw,4.2rem)' }}
      >
        <span style={{ color: '#fbbf24' }}>{a}</span>
        <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: '0.6em' }}> {op} </span>
        <span style={{ color: '#f87171' }}>{b}</span>
        <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: '0.6em' }}> = </span>
        <span style={{ color: 'rgba(255,255,255,0.2)' }}>{ans}</span>
      </div>
    );
  }
  // Fallback: plain big text
  return (
    <div
      className="text-center text-theme leading-tight max-w-2xl"
      style={{ fontFamily: 'var(--font-fredoka-one), cursive', fontSize: 'clamp(2rem,8vw,3.5rem)' }}
    >
      {text}
    </div>
  );
}

export const QuestionDisplay = ({
  displayText,
  spokenText,
  icon,
  isAnimating = false,
  onSpeak,
}: QuestionDisplayProps) => {
  return (
    <div className={`flex flex-col items-center gap-4 ${isAnimating ? 'animate-fadeUp' : ''}`}>
      {/* Optional icon above the question */}
      {icon && (
        <div className={`text-5xl ${isAnimating ? 'animate-bounce' : ''}`}>{icon}</div>
      )}

      {/* Main question */}
      <MathQuestion text={displayText} />

      {/* Circular speak button, matches HTML's q-speak-btn */}
      {onSpeak && (
        <button
          onClick={onSpeak}
          title="Hear question"
          style={{
            width: 52,
            height: 52,
            borderRadius: '50%',
            background: '#252545',
            border: '2px solid rgba(255,255,255,0.1)',
            fontSize: '1.4rem',
            cursor: 'pointer',
            transition: 'all 0.2s',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = '#34d399';
            e.currentTarget.style.transform = 'scale(1.1)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)';
            e.currentTarget.style.transform = 'scale(1)';
          }}
        >
          🔊
        </button>
      )}
    </div>
  );
};
