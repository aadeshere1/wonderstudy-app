'use client';

import { useState } from 'react';

export interface FlashcardProps {
  front: string;
  back: string;
  hint?: string;
  index?: number;
  total?: number;
  onFlip?: (isFlipped: boolean) => void;
  onSpeak?: () => void;
}

/** Pick a font-size that fits the text length comfortably in the card. */
function pickFontSize(text: string): string {
  const len = text.length;
  if (len > 200) return 'clamp(0.85rem,2.5vw,1.05rem)';
  if (len > 100) return 'clamp(1rem,3vw,1.3rem)';
  if (len > 50)  return 'clamp(1.2rem,4vw,1.8rem)';
  if (len > 20)  return 'clamp(1.5rem,5vw,2.4rem)';
  return 'clamp(2rem,7vw,3.5rem)';
}

/**
 * Render flashcard text with nice formatting:
 * - Lines starting with "•" → styled bullet rows
 * - Lines starting with "Tip:" → dimmed italic note
 * - Everything else → normal paragraph
 * - Plain text (no bullets) → white-space pre-line, centred
 */
function FlashcardText({ text, fontSize }: { text: string; fontSize: string }) {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
  const hasBullets = lines.some(l => l.startsWith('•'));

  if (!hasBullets) {
    return (
      <p style={{ fontSize, whiteSpace: 'pre-line', textAlign: 'center', lineHeight: 1.5, margin: 0 }}>
        {text}
      </p>
    );
  }

  return (
    <div style={{ fontSize, width: '100%', display: 'flex', flexDirection: 'column', gap: 6 }}>
      {lines.map((line, i) => {
        if (line.startsWith('•')) {
          const content = line.slice(1).trim();
          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'baseline',
                gap: 8,
                padding: '5px 10px',
                borderRadius: 8,
                background: 'rgba(99,102,241,0.08)',
                lineHeight: 1.45,
              }}
            >
              <span style={{ color: '#a78bfa', flexShrink: 0, fontSize: '0.9em' }}>●</span>
              <span style={{ color: 'var(--ws-text)' }}>{content}</span>
            </div>
          );
        }
        // Tip / section note
        const isTip = line.toLowerCase().startsWith('tip:') || line.toLowerCase().startsWith('note:');
        return (
          <p
            key={i}
            style={{
              margin: '4px 0 0',
              lineHeight: 1.5,
              fontSize: '0.88em',
              color: isTip ? 'var(--ws-text-muted)' : 'var(--ws-text)',
              fontStyle: isTip ? 'italic' : 'normal',
              textAlign: 'center',
              padding: isTip ? '4px 8px' : undefined,
            }}
          >
            {line}
          </p>
        );
      })}
    </div>
  );
}

export const Flashcard = ({
  front,
  back,
  hint,
  index,
  total,
  onFlip,
  onSpeak,
}: FlashcardProps) => {
  const [isFlipped, setIsFlipped] = useState(false);

  const handleFlip = () => {
    const next = !isFlipped;
    setIsFlipped(next);
    onFlip?.(next);
  };

  const progress = index !== undefined && total !== undefined ? `${index + 1} / ${total}` : null;

  return (
    <div className="flex flex-col items-center gap-4 w-full" style={{ maxWidth: 600 }}>

      {/* ── Card counter ── */}
      {progress && (
        <div className="flex items-center gap-2">
          <span className="text-xs uppercase tracking-widest font-bold" style={{ color: 'var(--ws-text-muted)' }}>
            Card {progress}
          </span>
          {/* dot-track */}
          <div className="flex gap-1">
            {Array.from({ length: total ?? 0 }, (_, i) => (
              <div
                key={i}
                className="rounded-full transition-all duration-300"
                style={{
                  width: i === index ? 18 : 6,
                  height: 6,
                  background: i === index
                    ? 'linear-gradient(90deg,#a78bfa,#f87171)'
                    : 'var(--ws-border)',
                }}
              />
            ))}
          </div>
        </div>
      )}

      {/* ── 3-D flip container ─────────────────────────────────────────── */}
      {/*
        The OUTER div provides perspective.
        The INNER div is what actually rotates (transform-style: preserve-3d).
        Both faces are absolute inside the inner div.
      */}
      <div
        className="w-full relative cursor-pointer select-none"
        style={{
          perspective: '1200px',
          /* fixed-ratio card: 3:2 */
          paddingBottom: 'clamp(220px, 45vw, 360px)',
        }}
        onClick={handleFlip}
        role="button"
        aria-label={isFlipped ? 'Show front' : 'Show back'}
      >
        {/* Inner rotating shell */}
        <div
          className="absolute inset-0"
          style={{
            transformStyle: 'preserve-3d',
            transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
            transition: 'transform 0.55s cubic-bezier(0.4,0.2,0.2,1)',
          }}
        >
          {/* ── FRONT ── */}
          <div
            className="absolute inset-0 rounded-2xl flex flex-col items-center justify-center p-6 overflow-hidden"
            style={{
              backfaceVisibility: 'hidden',
              background: 'linear-gradient(135deg, rgba(167,139,250,0.25), rgba(96,165,250,0.15))',
              border: '2px solid rgba(167,139,250,0.45)',
              boxShadow: '0 8px 32px rgba(167,139,250,0.2)',
            }}
          >
            {/* label */}
            <div
              className="absolute top-3 left-4 text-xs font-bold uppercase tracking-widest px-2 py-0.5 rounded-full"
              style={{ background: 'rgba(167,139,250,0.2)', color: '#a78bfa' }}
            >
              Question
            </div>

            {/* scrollable content */}
            <div
              className="w-full overflow-y-auto font-display text-theme"
              style={{ maxHeight: '100%' }}
            >
              <FlashcardText text={front} fontSize={pickFontSize(front)} />
            </div>

            {hint && (
              <div
                className="absolute bottom-3 text-xs font-bold px-3 py-1 rounded-full"
                style={{ background: 'rgba(96,165,250,0.15)', color: '#60a5fa' }}
              >
                💡 {hint}
              </div>
            )}

            {/* tap hint */}
            <div
              className="absolute bottom-3 right-4 text-xs"
              style={{ color: 'var(--ws-text-dim)' }}
            >
              Tap to flip ↓
            </div>
          </div>

          {/* ── BACK ── */}
          <div
            className="absolute inset-0 rounded-2xl flex flex-col p-6 overflow-hidden"
            style={{
              backfaceVisibility: 'hidden',
              transform: 'rotateY(180deg)',
              background: 'linear-gradient(135deg, rgba(52,211,153,0.25), rgba(248,113,113,0.15))',
              border: '2px solid rgba(52,211,153,0.45)',
              boxShadow: '0 8px 32px rgba(52,211,153,0.2)',
            }}
          >
            {/* label */}
            <div
              className="text-xs font-bold uppercase tracking-widest px-2 py-0.5 rounded-full self-start mb-3 flex-shrink-0"
              style={{ background: 'rgba(52,211,153,0.2)', color: '#34d399' }}
            >
              Answer
            </div>

            {/* scrollable content */}
            <div
              className="w-full flex-1 overflow-y-auto font-display text-theme"
              style={{ minHeight: 0 }}
            >
              <FlashcardText text={back} fontSize={pickFontSize(back)} />
            </div>

            {/* tap hint */}
            <div
              className="flex-shrink-0 text-right text-xs mt-2"
              style={{ color: 'var(--ws-text-dim)' }}
            >
              Tap to flip ↑
            </div>
          </div>
        </div>
      </div>

      {/* ── Controls row ── */}
      <div className="flex items-center gap-3">
        <button
          onClick={handleFlip}
          style={{
            padding: '9px 20px',
            borderRadius: '30px',
            border: '2px solid rgba(167,139,250,0.3)',
            background: 'rgba(167,139,250,0.12)',
            color: '#a78bfa',
            fontFamily: 'var(--font-nunito),sans-serif',
            fontWeight: 800,
            fontSize: '0.85rem',
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
        >
          {isFlipped ? '← Show Front' : 'Show Answer →'}
        </button>

        {onSpeak && (
          <button
            onClick={(e) => { e.stopPropagation(); onSpeak(); }}
            title="Hear it"
            style={{
              width: 44,
              height: 44,
              borderRadius: '50%',
              background: 'var(--ws-card2)',
              border: '2px solid var(--ws-border)',
              fontSize: '1.2rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s',
            }}
            onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#34d399'; }}
            onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--ws-border)'; }}
          >
            🔊
          </button>
        )}
      </div>
    </div>
  );
};
