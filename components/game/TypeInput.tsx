'use client';

import { useEffect, useRef, useState } from 'react';

export interface TypeInputProps {
  placeholder?: string;
  onSubmit: (input: string) => void;
  disabled?: boolean;
  autoFocus?: boolean;
  maxLength?: number;
  hint?: string;
  isCorrect?: boolean;
  feedback?: string;
}

export const TypeInput = ({
  placeholder = '?',
  onSubmit,
  disabled = false,
  autoFocus = true,
  maxLength,
  hint,
  isCorrect,
  feedback,
}: TypeInputProps) => {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && inputRef.current && !disabled) {
      inputRef.current.focus();
    }
  }, [autoFocus, disabled]);

  const handleSubmit = () => {
    if (input.trim()) {
      onSubmit(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !disabled) handleSubmit();
  };

  // Border & text colour feedback
  let borderColor = 'rgba(255,255,255,0.12)';
  let textColor = 'white';
  if (isCorrect === true)  { borderColor = '#34d399'; textColor = '#34d399'; }
  if (isCorrect === false) { borderColor = '#f87171'; textColor = '#f87171'; }

  return (
    <div className="w-full max-w-sm mx-auto flex flex-col gap-3 items-center">
      {/* Hint */}
      {hint && (
        <div className="text-sm font-bold px-3 py-2 rounded-lg w-full" style={{ background: 'rgba(96,165,250,0.1)', color: '#60a5fa' }}>
          💡 {hint}
        </div>
      )}

      {/* Input row */}
      <div className="flex gap-3 w-full items-center">
        <input
          ref={inputRef}
          type="number"
          min={0}
          max={9999}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          maxLength={maxLength}
          placeholder={placeholder}
          style={{
            flex: 1,
            background: '#1e1e38',
            border: `3px solid ${borderColor}`,
            borderRadius: '16px',
            color: textColor,
            fontFamily: 'var(--font-fredoka-one), cursive',
            fontSize: '2rem',
            textAlign: 'center',
            padding: '14px',
            outline: 'none',
            transition: 'border-color 0.2s',
          }}
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !input.trim()}
          style={{
            padding: '14px 22px',
            borderRadius: '16px',
            background: 'linear-gradient(135deg,#a78bfa,#f87171)',
            border: 'none',
            color: 'white',
            fontFamily: 'var(--font-fredoka-one), cursive',
            fontSize: '1.2rem',
            cursor: disabled ? 'not-allowed' : 'pointer',
            opacity: (disabled || !input.trim()) ? 0.5 : 1,
            transition: 'all 0.2s',
          }}
        >
          →
        </button>
      </div>

      {/* Feedback */}
      {feedback && (
        <div
          className="font-display text-lg text-center w-full py-1"
          style={{ color: isCorrect ? '#34d399' : '#f87171' }}
        >
          {feedback}
        </div>
      )}
    </div>
  );
};
