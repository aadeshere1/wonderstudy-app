import Link from 'next/link';

export interface LessonCardProps {
  id: string;
  title: string;
  description?: string;
  icon?: string;
  classNum?: number;
  subject?: string;
  difficulty?: 'beginner' | 'intermediate' | 'advanced';
}

const difficultyConfig = {
  beginner: {
    label: '⭐ Beginner',
    bg: 'rgba(52,211,153,0.18)',
    color: '#34d399',
    glow: 'rgba(52,211,153,0.25)',
  },
  intermediate: {
    label: '🔥 Intermediate',
    bg: 'rgba(251,191,36,0.18)',
    color: '#fbbf24',
    glow: 'rgba(251,191,36,0.25)',
  },
  advanced: {
    label: '🚀 Advanced',
    bg: 'rgba(248,113,113,0.18)',
    color: '#f87171',
    glow: 'rgba(248,113,113,0.25)',
  },
};

export const LessonCard = ({
  id,
  title,
  description,
  icon = '📖',
  classNum,
  subject,
  difficulty = 'beginner',
}: LessonCardProps) => {
  const href = classNum && subject
    ? `/class/${classNum}/${subject}/${id}`
    : `/play/${id}`;

  const diff = difficultyConfig[difficulty];

  return (
    <Link href={href} className="block group">
      <div
        className="rounded-2xl bg-card h-full transition-all duration-200 group-hover:-translate-y-1 overflow-hidden"
        style={{ border: '1px solid var(--ws-border)', boxShadow: `0 0 0 0 ${diff.glow}`, transition: 'transform 0.2s, box-shadow 0.2s' }}
        onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.boxShadow = `0 6px 24px ${diff.glow}`; }}
        onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.boxShadow = `0 0 0 0 ${diff.glow}`; }}
      >
        {/* top accent bar */}
        <div className="h-1 w-full" style={{ background: diff.color, opacity: 0.7 }} />

        <div className="p-4 flex flex-col gap-3">
          {/* Icon & Title */}
          <div className="flex items-start gap-3">
            <div className="text-3xl flex-shrink-0 leading-none">{icon}</div>
            <div className="flex-1 min-w-0">
              <h3 className="font-black text-theme text-sm leading-snug">{title}</h3>
              {description && (
                <p className="text-xs text-muted mt-1 line-clamp-2">{description}</p>
              )}
            </div>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between">
            <span
              className="text-xs font-bold px-2.5 py-1 rounded-full"
              style={{ background: diff.bg, color: diff.color }}
            >
              {diff.label}
            </span>
            <span className="text-muted text-xs font-bold group-hover:text-purple transition-colors">Start →</span>
          </div>
        </div>
      </div>
    </Link>
  );
};
