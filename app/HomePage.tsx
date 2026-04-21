'use client';

import { useState } from 'react';
import { Nav } from '@/components/layout';
import {
  ClassChips,
  SubjectTabs,
  LessonCard,
  QuickGameCard,
} from '@/components/lesson-browser';
import SRSDueWidget from '@/components/srs/SRSDueWidget';

type GameCard = { id: string; title: string; icon: string; subtitle: string; gradient: string; glow: string };

type LessonEntry = {
  id: string;
  title: string;
  icon: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
};

type ClassLessonsMap = Record<string, Record<string, LessonEntry[]>>;
type JapaneseLessonsMap = Record<string, LessonEntry[]>;

interface HomePageProps {
  games: GameCard[];
  classLessons: ClassLessonsMap;
  japaneseLessons: JapaneseLessonsMap;
}

// ── Chapter grouping helpers ──────────────────────────────────────────────

/** Extract chapter number from ids like "ch01-vocabulary" → 1 */
function chapterNum(id: string): number {
  const m = id.match(/^ch(\d+)-/);
  return m ? parseInt(m[1], 10) : 0;
}

/** Extract lesson type label from ids like "ch01-vocabulary" → "Vocabulary" */
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

/** Extract the chapter title from the full lesson title.
 *  "Ch1: Vocabulary – Meeting people" → "Meeting people" */
function chapterTitle(title: string): string {
  const m = title.match(/–\s*(.+)$/);
  return m ? m[1].trim() : title;
}

/** Group a flat lesson list into chapters */
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

/** Renders the 25-chapter accordion list */
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
              <div
                className="grid grid-cols-1 sm:grid-cols-3 gap-2 px-3 pb-3"
              >
                {chLessons.map((lesson) => (
                  <a
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
                    <div
                      className="mt-auto text-xs font-bold"
                      style={{ color: '#e11d48' }}
                    >
                      Start →
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

const JLPT_LEVELS = [
  { level: 'n5', label: 'N5', available: true },
  { level: 'n4', label: 'N4', available: false },
  { level: 'n3', label: 'N3', available: false },
  { level: 'n2', label: 'N2', available: false },
  { level: 'n1', label: 'N1', available: false },
];

export default function HomePage({ games, classLessons, japaneseLessons }: HomePageProps) {
  const [selectedClass, setSelectedClass] = useState<number | null>(6);
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);
  const [selectedJlptLevel, setSelectedJlptLevel] = useState<string>('n5');

  const lessons: LessonEntry[] =
    selectedClass && selectedSubject
      ? (classLessons[String(selectedClass)]?.[selectedSubject] ?? [])
      : [];

  return (
    <>
      <Nav title="WonderStudy" />

      <main className="relative z-10 max-w-3xl mx-auto px-4 pb-16">

        {/* ── Hero ─────────────────────────────────────── */}
        <div className="text-center pt-10 pb-6">
          <div className="text-5xl mb-3 animate-bounce">🌟</div>
          <h1 className="font-display text-4xl md:text-5xl bg-gradient-to-r from-gold via-coral to-purple bg-clip-text text-transparent mb-2 leading-tight">
            Welcome to WonderStudy!
          </h1>
          <p className="text-muted text-sm">Learn with fun games &amp; interactive lessons</p>
        </div>

        {/* ── SRS Due Widget ───────────────────────────── */}
        <SRSDueWidget />

        {/* ── Quick Games ───────────────────────────────── */}
        <section className="mb-5">
          <div className="font-display text-2xl mb-1">🚀 Quick Games</div>
          <div className="text-muted text-xs mb-4">Jump straight in and start practising</div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {games.map((game) => (
              <QuickGameCard key={game.id} {...game} />
            ))}
          </div>
        </section>

        {/* ── Divider ──────────────────────────────────── */}
        <div className="h-px bg-white/7 my-6" />

        {/* ── Learn Japanese ───────────────────────────── */}
        <section className="mb-5">
          <div className="font-display text-2xl mb-1">🇯🇵 Learn Japanese</div>
          <div className="text-muted text-xs mb-4">Study for JLPT — vocabulary, kanji, and grammar</div>

          {/* JLPT Level chips */}
          <div className="flex flex-wrap gap-2 mb-4">
            {JLPT_LEVELS.map(({ level, label, available }) => (
              <button
                key={level}
                onClick={() => available && setSelectedJlptLevel(level)}
                disabled={!available}
                className="relative px-4 py-1.5 rounded-full text-sm font-bold transition-all duration-150"
                style={
                  available && selectedJlptLevel === level
                    ? { background: 'linear-gradient(135deg,#e11d48,#f97316)', color: '#fff', boxShadow: '0 2px 12px rgba(225,29,72,0.35)' }
                    : available
                    ? { background: 'var(--ws-card2)', color: 'var(--ws-text)', border: '1px solid var(--ws-border)' }
                    : { background: 'var(--ws-card2)', color: 'var(--ws-text-dim)', border: '1px solid var(--ws-border)', opacity: 0.5, cursor: 'not-allowed' }
                }
              >
                {label}
                {!available && (
                  <span className="ml-1.5 text-xs font-normal opacity-75">soon</span>
                )}
              </button>
            ))}
          </div>

          {/* Lessons grouped by chapter */}
          {japaneseLessons[selectedJlptLevel] && japaneseLessons[selectedJlptLevel].length > 0 ? (
            <ChapterList lessons={japaneseLessons[selectedJlptLevel]} level={selectedJlptLevel} />
          ) : (
            <div className="card text-center py-10">
              <div className="text-4xl mb-3">🔜</div>
              <p className="text-muted text-sm mb-1">{selectedJlptLevel.toUpperCase()} content coming soon!</p>
              <p className="text-xs" style={{ color: 'var(--ws-text-dim)' }}>Start with N5 to begin your journey</p>
            </div>
          )}
        </section>

        {/* ── Divider ──────────────────────────────────── */}
        <div className="h-px bg-white/7 my-6" />

        {/* ── Structured Learning ──────────────────────── */}
        <section className="mb-5">
          <div className="font-display text-2xl mb-1">📚 Structured Learning</div>
          <div className="text-muted text-xs mb-4">Choose your class to browse lessons</div>
          <ClassChips
            selectedClass={selectedClass}
            onSelect={(n) => { setSelectedClass(n); setSelectedSubject(null); }}
          />
        </section>

        {/* ── Subject Selector ─────────────────────────── */}
        {selectedClass && (
          <section className="mb-5 animate-fadeUp">
            <div className="font-display text-2xl mb-1">📖 Choose Subject</div>
            <div className="text-muted text-xs mb-4">Class {selectedClass} — pick a subject to explore</div>
            <SubjectTabs
              selectedSubject={selectedSubject}
              onSelect={setSelectedSubject}
            />
          </section>
        )}

        {/* ── Lessons Grid ─────────────────────────────── */}
        {selectedClass && selectedSubject && (
          <section className="mb-5 animate-fadeUp">
            <div className="font-display text-2xl mb-1">🎓 Lessons</div>
            <div className="text-muted text-xs mb-4">
              Class {selectedClass} — {selectedSubject.charAt(0).toUpperCase() + selectedSubject.slice(1)}
            </div>

            {lessons.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {lessons.map((lesson) => (
                  <LessonCard
                    key={lesson.id}
                    {...lesson}
                    classNum={selectedClass}
                    subject={selectedSubject}
                  />
                ))}
              </div>
            ) : (
              <div className="card text-center py-10">
                <div className="text-4xl mb-3">🔭</div>
                <p className="text-muted text-sm mb-1">No lessons here yet!</p>
                <p className="text-xs" style={{ color: 'var(--ws-text-dim)' }}>More coming soon…</p>
              </div>
            )}
          </section>
        )}

        {/* ── How to Play ──────────────────────────────── */}
        <div className="card mt-6" style={{ background: 'linear-gradient(135deg, rgba(167,139,250,0.15), rgba(96,165,250,0.12))', borderColor: 'rgba(167,139,250,0.3)' }}>
          <div className="font-display text-xl text-center mb-4 bg-gradient-to-r from-purple to-blue bg-clip-text text-transparent">
            ✨ How to Play
          </div>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <span className="text-2xl flex-shrink-0">📖</span>
              <div>
                <div className="font-black text-theme text-sm">Teach</div>
                <div className="text-muted text-xs">Learn new concepts with interactive flashcards</div>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl flex-shrink-0">✏️</span>
              <div>
                <div className="font-black text-theme text-sm">Practice</div>
                <div className="text-muted text-xs">Test your knowledge at your own pace</div>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-2xl flex-shrink-0">🏆</span>
              <div>
                <div className="font-black text-theme text-sm">Challenge</div>
                <div className="text-muted text-xs">Race against time and beat your own record!</div>
              </div>
            </div>
          </div>
        </div>

      </main>
    </>
  );
}
