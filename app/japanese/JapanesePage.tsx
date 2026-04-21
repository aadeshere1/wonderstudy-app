'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Nav } from '@/components/layout';

export type LessonEntry = {
  id: string;
  title: string;
  icon: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
};

export type JapaneseLessonsMap = Record<string, LessonEntry[]>;

// ── Chapter grouping helpers ──────────────────────────────────────────────

function chapterNum(id: string): number {
  const m = id.match(/^ch(\d+)-/);
  return m ? parseInt(m[1], 10) : 0;
}

function lessonTypeLabel(id: string): string {
  if (id.endsWith('-vocabulary')) return 'Vocabulary';
  if (id.endsWith('-grammar'))    return 'Grammar';
  if (id.endsWith('-examples'))   return 'Dialogue';
  return id;
}

function lessonTypeIcon(id: string): string {
  if (id.endsWith('-vocabulary')) return '📚';
  if (id.endsWith('-grammar'))    return '📝';
  if (id.endsWith('-examples'))   return '💬';
  return '📖';
}

function chapterTitle(title: string): string {
  const m = title.match(/–\s*(.+)$/);
  return m ? m[1].trim() : title;
}

function groupByChapter(lessons: LessonEntry[]): { num: number; title: string; lessons: LessonEntry[] }[] {
  const map = new Map<number, { num: number; title: string; lessons: LessonEntry[] }>();
  for (const l of lessons) {
    const num = chapterNum(l.id);
    if (!map.has(num)) {
      map.set(num, { num, title: chapterTitle(l.title), lessons: [] });
    }
    map.get(num)!.lessons.push(l);
  }
  return Array.from(map.values()).sort((a, b) => a.num - b.num);
}

// ── Chapter accordion ─────────────────────────────────────────────────────

function ChapterList({ lessons, level }: { lessons: LessonEntry[]; level: string }) {
  const chapters = groupByChapter(lessons);
  const [openChapter, setOpenChapter] = useState<number | null>(null);

  return (
    <div className="flex flex-col gap-2">
      {chapters.map(({ num, title, lessons: chLessons }) => {
        const isOpen = openChapter === num;
        return (
          <div
            key={num}
            className="rounded-2xl overflow-hidden"
            style={{ border: '1px solid var(--ws-border)', background: 'var(--ws-card)' }}
          >
            {/* Chapter header row */}
            <button
              className="w-full flex items-center gap-3 px-4 py-3 text-left transition-all"
              style={{ background: isOpen ? 'rgba(225,29,72,0.06)' : 'transparent' }}
              onClick={() => setOpenChapter(isOpen ? null : num)}
            >
              <span
                className="flex-shrink-0 font-bold text-xs rounded-full flex items-center justify-center"
                style={{
                  width: 32, height: 32,
                  background: isOpen
                    ? 'linear-gradient(135deg,#e11d48,#f97316)'
                    : 'var(--ws-card2)',
                  color: isOpen ? '#fff' : 'var(--ws-text-muted)',
                  border: isOpen ? 'none' : '1px solid var(--ws-border)',
                }}
              >
                {num}
              </span>
              <div className="flex-1 min-w-0">
                <div className="font-bold text-sm truncate" style={{ color: 'var(--ws-text)' }}>
                  {title}
                </div>
                <div className="text-xs" style={{ color: 'var(--ws-text-muted)' }}>
                  {chLessons.map(l => lessonTypeLabel(l.id)).join(' · ')}
                </div>
              </div>
              <span
                className="flex-shrink-0 text-xs transition-transform duration-200"
                style={{
                  color: 'var(--ws-text-muted)',
                  transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                }}
              >
                ▾
              </span>
            </button>

            {/* Expanded lesson cards */}
            {isOpen && (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 px-3 pb-3">
                {chLessons.map((lesson) => (
                  <Link
                    key={lesson.id}
                    href={`/class/jlpt/${level}/${lesson.id}`}
                    className="flex flex-col gap-1 rounded-xl px-3 py-3 transition-all"
                    style={{
                      background: 'var(--ws-card2)',
                      border: '1px solid var(--ws-border)',
                      textDecoration: 'none',
                    }}
                    onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.borderColor = '#e11d48'; }}
                    onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--ws-border)'; }}
                  >
                    <div className="text-xl">{lessonTypeIcon(lesson.id)}</div>
                    <div className="font-bold text-sm" style={{ color: 'var(--ws-text)' }}>
                      {lessonTypeLabel(lesson.id)}
                    </div>
                    <div className="text-xs" style={{ color: 'var(--ws-text-muted)' }}>
                      {lesson.description}
                    </div>
                    <div className="mt-auto text-xs font-bold" style={{ color: '#e11d48' }}>
                      Start →
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ── JLPT level chips ──────────────────────────────────────────────────────

const JLPT_LEVELS = [
  { level: 'n5', label: 'N5', available: true },
  { level: 'n4', label: 'N4', available: false },
  { level: 'n3', label: 'N3', available: false },
  { level: 'n2', label: 'N2', available: false },
  { level: 'n1', label: 'N1', available: false },
];

// ── Page component ────────────────────────────────────────────────────────

export default function JapanesePage({ japaneseLessons }: { japaneseLessons: JapaneseLessonsMap }) {
  const [selectedLevel, setSelectedLevel] = useState<string>('n5');

  return (
    <>
      <Nav title="WonderStudy" />

      <main className="relative z-10 max-w-3xl mx-auto px-4 pb-16">

        {/* ── Header ───────────────────────────────────── */}
        <div className="pt-8 pb-6">
          <div className="flex items-center gap-2 mb-1">
            <Link
              href="/"
              className="text-xs font-bold px-3 py-1 rounded-full transition-all"
              style={{ background: 'var(--ws-card2)', color: 'var(--ws-text-muted)', border: '1px solid var(--ws-border)', textDecoration: 'none' }}
            >
              ← Home
            </Link>
          </div>
          <div className="mt-4">
            <h1 className="font-display text-4xl bg-gradient-to-r from-red-500 via-orange-400 to-yellow-400 bg-clip-text text-transparent mb-1 leading-tight">
              🇯🇵 Learn Japanese
            </h1>
            <p className="text-muted text-sm">Study for JLPT — vocabulary, grammar, and real-life dialogue</p>
          </div>
        </div>

        {/* ── JLPT Level chips ──────────────────────────── */}
        <div className="flex flex-wrap gap-2 mb-5">
          {JLPT_LEVELS.map(({ level, label, available }) => (
            <button
              key={level}
              onClick={() => available && setSelectedLevel(level)}
              disabled={!available}
              className="relative px-4 py-1.5 rounded-full text-sm font-bold transition-all duration-150"
              style={
                available && selectedLevel === level
                  ? { background: 'linear-gradient(135deg,#e11d48,#f97316)', color: '#fff', boxShadow: '0 2px 12px rgba(225,29,72,0.35)' }
                  : available
                  ? { background: 'var(--ws-card2)', color: 'var(--ws-text)', border: '1px solid var(--ws-border)' }
                  : { background: 'var(--ws-card2)', color: 'var(--ws-text-dim)', border: '1px solid var(--ws-border)', opacity: 0.5, cursor: 'not-allowed' }
              }
            >
              {label}
              {!available && <span className="ml-1.5 text-xs font-normal opacity-75">soon</span>}
            </button>
          ))}
        </div>

        {/* ── Chapter list ──────────────────────────────── */}
        {japaneseLessons[selectedLevel] && japaneseLessons[selectedLevel].length > 0 ? (
          <ChapterList lessons={japaneseLessons[selectedLevel]} level={selectedLevel} />
        ) : (
          <div className="card text-center py-10">
            <div className="text-4xl mb-3">🔜</div>
            <p className="text-muted text-sm mb-1">{selectedLevel.toUpperCase()} content coming soon!</p>
            <p className="text-xs" style={{ color: 'var(--ws-text-dim)' }}>Start with N5 to begin your journey</p>
          </div>
        )}
      </main>
    </>
  );
}
