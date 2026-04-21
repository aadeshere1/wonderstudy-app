'use client';

import { useState } from 'react';
import Link from 'next/link';
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

interface HomePageProps {
  games: GameCard[];
  classLessons: ClassLessonsMap;
}

export default function HomePage({ games, classLessons }: HomePageProps) {
  const [selectedClass, setSelectedClass] = useState<number | null>(6);
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);

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

        {/* ── Languages entry card ──────────────────────── */}
        <section className="mb-5">
          <div className="font-display text-2xl mb-1">🌍 Languages</div>
          <div className="text-muted text-xs mb-4">Learn a new language step by step</div>
          <Link
            href="/japanese"
            className="flex items-center gap-4 rounded-2xl px-5 py-4 transition-all"
            style={{
              background: 'linear-gradient(135deg, rgba(225,29,72,0.12), rgba(249,115,22,0.08))',
              border: '1px solid rgba(225,29,72,0.25)',
              textDecoration: 'none',
              display: 'flex',
            }}
            onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.borderColor = 'rgba(225,29,72,0.6)'; }}
            onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.borderColor = 'rgba(225,29,72,0.25)'; }}
          >
            <div className="text-4xl flex-shrink-0">🇯🇵</div>
            <div className="flex-1 min-w-0">
              <div className="font-bold text-base" style={{ color: 'var(--ws-text)' }}>Japanese</div>
              <div className="text-xs mt-0.5" style={{ color: 'var(--ws-text-muted)' }}>
                JLPT N5–N1 · Minna no Nihongo · 25 chapters
              </div>
            </div>
            <div className="flex-shrink-0 text-sm font-bold" style={{ color: '#e11d48' }}>
              Study →
            </div>
          </Link>
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
