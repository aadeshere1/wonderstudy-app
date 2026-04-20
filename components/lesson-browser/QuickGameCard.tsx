import Link from 'next/link';

export interface QuickGameCardProps {
  id: string;
  title: string;
  icon?: string;
  subtitle?: string;
  /** Tailwind gradient classes, e.g. "from-purple to-coral" */
  gradient?: string;
  /** CSS box-shadow glow colour string */
  glow?: string;
}

export const QuickGameCard = ({
  id,
  title,
  icon = '🎮',
  subtitle,
  gradient = 'from-purple to-coral',
  glow = 'rgba(167,139,250,0.35)',
}: QuickGameCardProps) => {
  return (
    <Link href={`/play/${id}`} className="block group">
      <div
        className={`relative overflow-hidden rounded-2xl bg-gradient-to-br ${gradient} p-px transition-all duration-200 group-hover:-translate-y-1`}
        style={{ boxShadow: `0 4px 20px ${glow}`, border: '1px solid var(--ws-border)' }}
      >
        {/* inner surface — themed */}
        <div
          className="rounded-2xl backdrop-blur-sm px-6 py-7 flex flex-col items-center justify-center text-center gap-3 h-full"
          style={{ background: 'var(--ws-card)' }}
        >
          {/* icon with gradient circle bg */}
          <div
            className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center text-3xl shadow-lg`}
            style={{ boxShadow: `0 6px 20px ${glow}` }}
          >
            {icon}
          </div>

          <div>
            <h3 className="font-display text-xl text-theme">{title}</h3>
            {subtitle && (
              <p className="text-xs mt-1" style={{ color: 'var(--ws-text-muted)' }}>{subtitle}</p>
            )}
          </div>

          {/* play button — always white text on gradient bg */}
          <div
            className={`mt-1 px-5 py-1.5 rounded-full bg-gradient-to-r ${gradient} font-black text-xs shadow-md`}
            style={{ color: 'white' }}
          >
            Play Now →
          </div>
        </div>
      </div>
    </Link>
  );
};
