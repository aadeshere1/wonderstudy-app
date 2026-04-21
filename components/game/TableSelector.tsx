'use client';

import { useState } from 'react';

export interface TableSelectorProps {
  /** Game title shown at the top */
  title: string;
  /** Emoji icon */
  icon: string;
  /** Short description under the title */
  description?: string;
  /** "multiply" | "divide" — affects chip label */
  operation?: 'multiply' | 'divide' | string;
  /** Highest table number available (default 12) */
  maxTable?: number;
  /** Tables pre-selected on first render */
  defaultSelected?: number[];
  onStart: (selectedTables: number[]) => void;
  onBack: () => void;
}

export const TableSelector = ({
  title,
  icon,
  description,
  operation = 'multiply',
  maxTable = 12,
  defaultSelected = [2, 5, 10],
  onStart,
  onBack,
}: TableSelectorProps) => {
  const [selected, setSelected] = useState<Set<number>>(new Set(defaultSelected));

  const tables = Array.from({ length: maxTable }, (_, i) => i + 1);

  const toggle = (n: number) =>
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(n) ? next.delete(n) : next.add(n);
      return next;
    });

  const selectAll  = () => setSelected(new Set(tables));
  const clearAll   = () => setSelected(new Set());

  const opSymbol = operation === 'divide' ? '÷' : '×';

  const canStart = selected.size > 0;

  return (
    <div className="fixed inset-0 flex flex-col overflow-hidden" style={{ background: 'var(--ws-bg)' }}>

      {/* ── Top bar ── */}
      <div
        className="flex-shrink-0 flex items-center justify-between px-4 py-3"
        style={{ background: 'var(--ws-surface)', borderBottom: '1px solid var(--ws-border)' }}
      >
        <button
          onClick={onBack}
          style={{ background: 'none', border: 'none', color: 'var(--ws-text-muted)', fontWeight: 800, fontSize: '0.85rem', cursor: 'pointer', fontFamily: 'var(--font-nunito),sans-serif' }}
        >
          ← Back
        </button>
        <div
          className="font-display text-base"
          style={{ background: 'linear-gradient(135deg,#fbbf24,#f87171)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}
        >
          {icon} {title}
        </div>
        <div style={{ width: 60 }} />
      </div>

      {/* ── Scrollable body ── */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-lg mx-auto px-4 py-8 flex flex-col gap-8">

          {/* Hero */}
          <div className="text-center">
            <div className="text-6xl mb-3">{icon}</div>
            <h1
              className="font-display text-3xl mb-1"
              style={{ background: 'linear-gradient(135deg,#fbbf24,#f87171)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}
            >
              {title}
            </h1>
            {description && (
              <p className="text-sm" style={{ color: 'var(--ws-text-muted)' }}>{description}</p>
            )}
          </div>

          {/* ── Table chips ── */}
          <div
            className="rounded-2xl p-5"
            style={{ background: 'var(--ws-card)', border: '1px solid var(--ws-border)' }}
          >
            {/* Row header */}
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="font-black text-theme text-sm">Choose Tables</div>
                <div className="text-xs mt-0.5" style={{ color: 'var(--ws-text-muted)' }}>
                  {selected.size === 0
                    ? 'Pick at least one'
                    : selected.size === maxTable
                    ? 'All tables selected'
                    : `${selected.size} table${selected.size > 1 ? 's' : ''} selected`}
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={selectAll}
                  style={{
                    padding: '5px 12px',
                    borderRadius: '8px',
                    background: 'var(--ws-card2)',
                    border: '1px solid var(--ws-border)',
                    color: 'var(--ws-text)',
                    fontWeight: 800,
                    fontSize: '0.75rem',
                    cursor: 'pointer',
                    fontFamily: 'var(--font-nunito),sans-serif',
                  }}
                >
                  All
                </button>
                <button
                  onClick={clearAll}
                  style={{
                    padding: '5px 12px',
                    borderRadius: '8px',
                    background: 'var(--ws-card2)',
                    border: '1px solid var(--ws-border)',
                    color: 'var(--ws-text)',
                    fontWeight: 800,
                    fontSize: '0.75rem',
                    cursor: 'pointer',
                    fontFamily: 'var(--font-nunito),sans-serif',
                  }}
                >
                  Clear
                </button>
              </div>
            </div>

            {/* Chip grid */}
            <div className="flex flex-wrap gap-2">
              {tables.map((n) => {
                const active = selected.has(n);
                return (
                  <button
                    key={n}
                    onClick={() => toggle(n)}
                    style={{
                      width: 52,
                      height: 52,
                      borderRadius: '12px',
                      border: active ? '2px solid #34d399' : '2px solid var(--ws-border)',
                      background: active
                        ? 'linear-gradient(135deg,#34d399,#0891b2)'
                        : 'var(--ws-card2)',
                      color: 'var(--ws-text)',
                      fontFamily: 'var(--font-fredoka-one),cursive',
                      fontSize: '1.1rem',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      transition: 'all 0.15s',
                      transform: active ? 'scale(1.08)' : 'scale(1)',
                      boxShadow: active ? '0 4px 12px rgba(52,211,153,0.4)' : 'none',
                      position: 'relative',
                    }}
                    title={`${opSymbol}${n} table`}
                  >
                    {n}
                    {active && (
                      <span
                        style={{
                          position: 'absolute',
                          top: -6,
                          right: -6,
                          width: 14,
                          height: 14,
                          borderRadius: '50%',
                          background: '#34d399',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '0.5rem',
                          fontWeight: 900,
                          color: 'var(--ws-bg)',
                        }}
                      >
                        ✓
                      </span>
                    )}
                  </button>
                );
              })}
            </div>

            {/* Quick-picks row */}
            <div className="flex flex-wrap gap-2 mt-4 pt-4" style={{ borderTop: '1px solid var(--ws-border)' }}>
              <span className="text-xs font-bold self-center" style={{ color: 'var(--ws-text-dim)' }}>Quick pick:</span>
              {[
                { label: 'Easy', tables: [2, 5, 10] },
                { label: 'Medium', tables: [3, 4, 6, 7, 8] },
                { label: 'Hard', tables: [7, 8, 9, 11, 12] },
              ].map((preset) => (
                <button
                  key={preset.label}
                  onClick={() => setSelected(new Set(preset.tables))}
                  style={{
                    padding: '4px 12px',
                    borderRadius: '20px',
                    border: '2px solid var(--ws-border)',
                    background: 'transparent',
                    color: 'var(--ws-text-muted)',
                    fontWeight: 800,
                    fontSize: '0.75rem',
                    cursor: 'pointer',
                    fontFamily: 'var(--font-nunito),sans-serif',
                    transition: 'all 0.15s',
                  }}
                  onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#a78bfa'; e.currentTarget.style.color = '#a78bfa'; }}
                  onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--ws-border)'; e.currentTarget.style.color = 'var(--ws-text-muted)'; }}
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>

          {/* Preview of selected */}
          {selected.size > 0 && (
            <div className="text-center text-sm" style={{ color: 'var(--ws-text-muted)' }}>
              Practising:{' '}
              <span className="font-black" style={{ color: '#34d399' }}>
                {Array.from(selected).sort((a, b) => a - b).map((n) => `${opSymbol}${n}`).join(', ')}
              </span>
            </div>
          )}

        </div>
      </div>

      {/* ── Start button ── */}
      <div
        className="flex-shrink-0 flex justify-center px-4 py-5"
        style={{ background: 'var(--ws-surface)', borderTop: '1px solid var(--ws-border)' }}
      >
        <button
          onClick={() => canStart && onStart(Array.from(selected).sort((a, b) => a - b))}
          disabled={!canStart}
          style={{
            padding: '16px 48px',
            borderRadius: '16px',
            background: canStart
              ? 'linear-gradient(135deg,#fbbf24,#f97316)'
              : 'rgba(251,191,36,0.25)',
            border: 'none',
            color: canStart ? '#1a1a2e' : 'rgba(251,191,36,0.4)',
            fontFamily: 'var(--font-fredoka-one),cursive',
            fontSize: '1.2rem',
            fontWeight: 900,
            cursor: canStart ? 'pointer' : 'not-allowed',
            boxShadow: canStart ? '0 4px 20px rgba(251,191,36,0.45)' : 'none',
            transition: 'all 0.2s',
            minWidth: 220,
          }}
          onMouseEnter={(e) => { if (canStart) e.currentTarget.style.transform = 'translateY(-2px)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; }}
        >
          🚀 Start Challenge!
        </button>
      </div>
    </div>
  );
};
