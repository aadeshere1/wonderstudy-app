import { readFileSync, readdirSync, existsSync } from 'fs';
import { join } from 'path';
import type { Metadata } from 'next';
import JapanesePage, { type JapaneseLessonsMap } from './JapanesePage';

export const metadata: Metadata = {
  title: 'Learn Japanese | Sikshya',
  description: 'Study for JLPT N5–N1 with Minna no Nihongo — vocabulary, grammar, and dialogue.',
};

function loadJapaneseLessons(): JapaneseLessonsMap {
  const result: JapaneseLessonsMap = {};
  const jlptDir = join(process.cwd(), 'data', 'classes', 'jlpt');
  if (!existsSync(jlptDir)) return result;

  try {
    const levels = readdirSync(jlptDir);
    for (const level of levels) {
      const indexPath = join(jlptDir, level, 'index.json');
      if (!existsSync(indexPath)) continue;
      try {
        const raw = JSON.parse(readFileSync(indexPath, 'utf-8')) as {
          lessons: Array<{ id: string; title: string; icon: string; subtopics?: string[] }>;
        };
        result[level] = raw.lessons.map((l) => ({
          id: l.id,
          title: l.title,
          icon: l.icon,
          description: l.subtopics?.join(' · ') ?? '',
          difficulty: 'beginner' as const,
        }));
      } catch { /* skip bad index */ }
    }
  } catch { /* skip if jlpt dir unreadable */ }

  return result;
}

export default function Page() {
  const japaneseLessons = loadJapaneseLessons();
  return <JapanesePage japaneseLessons={japaneseLessons} />;
}
