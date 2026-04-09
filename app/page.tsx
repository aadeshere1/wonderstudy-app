import { readFileSync } from 'fs';
import { join } from 'path';
import { Metadata } from 'next';
import { siteMetadata } from './metadata';
import HomePage from './HomePage';
export const metadata: Metadata = siteMetadata;

// Visual styles per game ID — full Tailwind strings so Tailwind scans them at build time
const GAME_STYLES: Record<string, { gradient: string; glow: string; subtitle: string }> = {
  'multiplication':             { gradient: 'from-purple to-coral',    glow: 'rgba(167,139,250,0.35)', subtitle: 'Practice times tables' },
  'division':                   { gradient: 'from-gold to-orange-400', glow: 'rgba(251,191,36,0.35)',  subtitle: 'Master division facts' },
  'general-addition':           { gradient: 'from-mint to-cyan-600',   glow: 'rgba(52,211,153,0.35)',  subtitle: 'Add numbers fast!' },
  'general-subtraction':        { gradient: 'from-blue to-purple',     glow: 'rgba(96,165,250,0.35)',  subtitle: 'Subtract with confidence' },
  'general-solar-system':       { gradient: 'from-purple to-blue',     glow: 'rgba(167,139,250,0.35)', subtitle: 'Explore space & planets' },
  'general-human-body':         { gradient: 'from-coral to-pink',      glow: 'rgba(248,113,113,0.35)', subtitle: 'Learn about your body' },
  'general-animals-world':      { gradient: 'from-gold to-mint',       glow: 'rgba(251,191,36,0.35)',  subtitle: 'Discover amazing animals' },
  'general-spelling-bee':       { gradient: 'from-pink to-purple',     glow: 'rgba(236,72,153,0.35)',  subtitle: 'Spell every word right' },
  'general-countries-capitals': { gradient: 'from-mint to-blue',       glow: 'rgba(52,211,153,0.35)',  subtitle: 'Travel the world!' },
  'general-food-nutrition':     { gradient: 'from-coral to-gold',      glow: 'rgba(248,113,113,0.35)', subtitle: 'Eat well, feel great' },
};

type GameCard = { id: string; title: string; icon: string; subtitle: string; gradient: string; glow: string };

export default function Page() {
  let games: GameCard[] = [];

  try {
    const indexPath = join(process.cwd(), 'data', 'general', 'index.json');
    const index = JSON.parse(readFileSync(indexPath, 'utf-8')) as {
      lessons: Array<{ id: string; title: string; icon: string }>;
    };
    games = index.lessons.map((lesson) => {
      const styles = GAME_STYLES[lesson.id] ?? {
        gradient: 'from-purple to-coral' as const,
        glow: 'rgba(167,139,250,0.35)',
        subtitle: 'Play now!',
      };
      return { id: lesson.id, title: lesson.title, icon: lesson.icon, ...styles };
    });
  } catch {
    games = [
      { id: 'multiplication', title: 'Multiplication', icon: '✖️', subtitle: 'Practice times tables', gradient: 'from-purple to-coral',    glow: 'rgba(167,139,250,0.35)' },
      { id: 'division',       title: 'Division',       icon: '÷',  subtitle: 'Master division facts', gradient: 'from-gold to-orange-400', glow: 'rgba(251,191,36,0.35)' },
    ];
  }

  return <HomePage games={games} />;
}
