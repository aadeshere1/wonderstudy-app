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
        className={`relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br ${gradient} p-px transition-all duration-200 group-hover:-translate-y-1`}
        style={{ boxShadow: `0 4px 20px ${glow}` }}
      >
        {/* inner dark surface */}
        <div className="rounded-2xl bg-card/80 backdrop-blur-sm px-6 py-7 flex flex-col items-center justify-center text-center gap-3 h-full"
          style={{ background: 'rgba(30, 30, 56, 0.85)' }}>

          {/* icon with gradient circle bg */}
          <div
            className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center text-3xl shadow-lg`}
            style={{ boxShadow: `0 6px 20px ${glow}` }}
          >
            {icon}
          </div>

          <div>
            <h3 className="font-display text-xl text-white">{title}</h3>
            {subtitle && (
              <p className="text-xs text-muted mt-1">{subtitle}</p>
            )}
          </div>

          {/* play button */}
          <div
            className={`mt-1 px-5 py-1.5 rounded-full bg-gradient-to-r ${gradient} font-black text-xs text-white shadow-md`}
          >
            Play Now →
          </div>
        </div>
      </div>
    </Link>
  );
};
