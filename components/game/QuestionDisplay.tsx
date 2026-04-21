'use client';

export interface QuestionDisplayProps {
  displayText: string;
  spokenText?: string;
  icon?: string;
  size?: 'sm' | 'md' | 'lg';
  isAnimating?: boolean;
  onSpeak?: () => void;
  /** Inline SVG markup from the geometry plugin — rendered as a diagram above the question */
  svgDiagram?: string;
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
        <span style={{ color: 'var(--ws-text-dim)', fontSize: '0.6em' }}> {op} </span>
        <span style={{ color: '#f87171' }}>{b}</span>
        <span style={{ color: 'var(--ws-text-dim)', fontSize: '0.6em' }}> = </span>
        <span style={{ color: 'var(--ws-text-muted)' }}>{ans}</span>
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
  svgDiagram,
}: QuestionDisplayProps) => {
  return (
    <div className={`flex flex-col items-center gap-4 ${isAnimating ? 'animate-fadeUp' : ''}`}>
      {/* Optional icon above the question */}
      {icon && (
        <div className={`text-5xl ${isAnimating ? 'animate-bounce' : ''}`}>{icon}</div>
      )}

      {/* Geometry SVG diagram */}
      {svgDiagram && (
        <div
          className="w-full max-w-xs mx-auto rounded-2xl overflow-hidden"
          style={{
            background: 'var(--ws-card2)',
            border: '1.5px solid var(--ws-border)',
            padding: '12px 8px 8px',
            boxShadow: '0 4px 16px rgba(99,102,241,0.12)',
          }}
          dangerouslySetInnerHTML={{ __html: svgDiagram }}
        />
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
            background: 'var(--ws-card2)',
            border: '2px solid var(--ws-border)',
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
            e.currentTarget.style.borderColor = 'var(--ws-border)';
            e.currentTarget.style.transform = 'scale(1)';
          }}
        >
          🔊
        </button>
      )}
    </div>
  );
};
