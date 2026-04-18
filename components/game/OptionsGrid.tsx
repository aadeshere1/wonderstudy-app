'use client';

export interface OptionsGridProps {
  options: string[];
  onSelect: (option: string) => void;
  disabled?: boolean;
  selectedOption?: string;
  correctOption?: string;
  wrongOption?: string;
  columns?: 1 | 2 | 3 | 4;
  size?: 'sm' | 'md' | 'lg';
}

const columnMap = {
  1: 'grid-cols-1 max-w-sm',
  2: 'grid-cols-2 max-w-lg',
  3: 'grid-cols-3 max-w-xl',
  4: 'grid-cols-4 max-w-2xl',
};

export const OptionsGrid = ({
  options,
  onSelect,
  disabled = false,
  selectedOption,
  correctOption,
  wrongOption,
  columns = 2,
}: OptionsGridProps) => {
  return (
    <div className={`grid ${columnMap[columns]} gap-3 w-full mx-auto px-4`}>
      {options.map((option, idx) => {
        const isCorrect = option === correctOption;
        const isWrong = option === wrongOption;
        const isSelected = option === selectedOption;

        // Use longhand border properties throughout — never mix border shorthand
        // with borderColor/borderWidth/borderStyle or React warns about conflicts.
        let style: React.CSSProperties = {
          padding: '16px',
          borderRadius: '16px',
          borderWidth: '2px',
          borderStyle: 'solid',
          borderColor: 'rgba(255,255,255,0.1)',
          background: '#1e1e38',
          color: '#f0f4ff',
          fontFamily: 'var(--font-fredoka-one), cursive',
          fontSize: '1.5rem',
          cursor: disabled ? 'default' : 'pointer',
          textAlign: 'center',
          transition: 'all 0.18s',
          opacity: disabled && !isCorrect && !isWrong ? 0.7 : 1,
        };

        if (isCorrect) {
          style = {
            ...style,
            background: 'linear-gradient(135deg,#15803d,#22c55e)',
            borderColor: '#34d399',
            transform: 'scale(1.04)',
            color: 'white',
          };
        } else if (isWrong) {
          style = {
            ...style,
            background: 'linear-gradient(135deg,#991b1b,#f87171)',
            borderColor: '#f87171',
            color: 'white',
            animation: 'shake 0.35s ease',
          };
        } else if (isSelected) {
          style = {
            ...style,
            borderColor: '#a78bfa',
            color: '#a78bfa',
          };
        }

        return (
          <button
            key={idx}
            onClick={() => !disabled && onSelect(option)}
            disabled={disabled}
            style={style}
            onMouseEnter={(e) => {
              if (!disabled && !isCorrect && !isWrong) {
                const el = e.currentTarget;
                el.style.borderColor = '#a78bfa';
                el.style.transform = 'translateY(-3px)';
                el.style.boxShadow = '0 6px 20px rgba(167,139,250,0.3)';
              }
            }}
            onMouseLeave={(e) => {
              if (!disabled && !isCorrect && !isWrong) {
                const el = e.currentTarget;
                el.style.borderColor = 'rgba(255,255,255,0.1)';
                el.style.transform = 'translateY(0)';
                el.style.boxShadow = 'none';
              }
            }}
          >
            {option}
          </button>
        );
      })}
    </div>
  );
};
