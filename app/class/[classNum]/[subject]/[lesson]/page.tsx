import { readFileSync } from 'fs';
import { join } from 'path';
import { Metadata } from 'next';
import Link from 'next/link';
import { lessonSchema, breadcrumbSchema } from '@/components/seo/SchemaMarkup';
import { Nav } from '@/components/layout';
import ReviewCard from '@/components/srs/ReviewCard';
import type { LessonData } from '@/lib/engine/types';

function classFolder(classNum: string) {
  return classNum === 'jlpt' ? 'jlpt' : `class-${classNum}`;
}

function loadLesson(classNum: string, subject: string, lesson: string): LessonData | null {
  try {
    const filePath = join(process.cwd(), 'data', 'classes', classFolder(classNum), subject, `${lesson}.json`);
    return JSON.parse(readFileSync(filePath, 'utf-8')) as LessonData;
  } catch {
    return null;
  }
}

export async function generateStaticParams() {
  const { readdirSync, existsSync } = await import('fs');
  const { join } = await import('path');
  const params: { classNum: string; subject: string; lesson: string }[] = [];
  const classesDir = join(process.cwd(), 'data', 'classes');
  if (!existsSync(classesDir)) return params;
  for (const classFolder of readdirSync(classesDir)) {
    const classNum = classFolder.replace('class-', '');
    const classPath = join(classesDir, classFolder);
    for (const subject of readdirSync(classPath)) {
      const subjectPath = join(classPath, subject);
      for (const file of readdirSync(subjectPath)) {
        if (file.endsWith('.json') && file !== 'index.json') {
          params.push({ classNum, subject, lesson: file.replace('.json', '') });
        }
      }
    }
  }
  return params;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ classNum: string; subject: string; lesson: string }>;
}): Promise<Metadata> {
  const { classNum, subject, lesson } = await params;
  const lessonData = loadLesson(classNum, subject, lesson);

  if (!lessonData) {
    return { title: 'Lesson - Sikshya', description: 'Interactive lesson' };
  }

  const title = `${lessonData.meta.title} - Class ${classNum} - Sikshya`;
  const description = lessonData.meta.description || `Learn about ${lessonData.meta.title} in Class ${classNum}`;
  return {
    title,
    description,
    keywords: [lessonData.meta.subject, `class ${classNum}`, 'educational game', 'kids learning'],
    openGraph: { title, description, type: 'website' },
  };
}

interface PageProps {
  params: Promise<{ classNum: string; subject: string; lesson: string }>;
}

const modeCards = [
  {
    mode: 'teach',
    label: 'Teach',
    icon: '📚',
    description: 'Learn with interactive flashcards and hints',
    gradient: 'linear-gradient(135deg,#a78bfa,#60a5fa)',
    glow: 'rgba(167,139,250,0.35)',
    tag: 'Start here!',
    tagColor: '#a78bfa',
    tagBg: 'rgba(167,139,250,0.2)',
  },
  {
    mode: 'practice',
    label: 'Practice',
    icon: '✏️',
    description: 'Test your knowledge with questions and feedback',
    gradient: 'linear-gradient(135deg,#34d399,#60a5fa)',
    glow: 'rgba(52,211,153,0.35)',
    tag: 'No time limit',
    tagColor: '#34d399',
    tagBg: 'rgba(52,211,153,0.2)',
  },
  {
    mode: 'challenge',
    label: 'Challenge',
    icon: '⚡',
    description: 'Race the clock and earn points!',
    gradient: 'linear-gradient(135deg,#fbbf24,#f87171)',
    glow: 'rgba(251,191,36,0.35)',
    tag: 'Timed!',
    tagColor: '#fbbf24',
    tagBg: 'rgba(251,191,36,0.2)',
  },
];

export default async function LessonPage({ params }: PageProps) {
  const { classNum, subject, lesson } = await params;
  const lessonData = loadLesson(classNum, subject, lesson);

  if (!lessonData) {
    return (
      <div className="fixed inset-0 flex items-center justify-center" style={{ background: 'var(--ws-bg)' }}>
        <div className="text-center">
          <div className="text-4xl mb-4">😬</div>
          <h1 className="font-display text-2xl mb-4" style={{ color: 'var(--ws-text)' }}>Lesson not found</h1>
          <Link href="/" style={{ color: '#a78bfa', fontWeight: 800 }}>← Back to home</Link>
        </div>
      </div>
    );
  }

  const breadcrumbData = breadcrumbSchema([
    { name: 'Home', url: '/' },
    { name: `Class ${classNum}`, url: '/' },
    { name: lessonData.meta.subject.charAt(0).toUpperCase() + lessonData.meta.subject.slice(1), url: '/' },
    { name: lessonData.meta.title, url: '' },
  ]);
  const lessonSchemaData = lessonSchema(
    lessonData.meta.title,
    lessonData.meta.description || '',
    lessonData.meta.class ?? undefined,
    lessonData.meta.subject
  );

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbData) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(lessonSchemaData) }} />

      <Nav title="Sikshya" />

      <main className="relative z-10 max-w-2xl mx-auto px-4 pb-16">

        {/* ── Lesson header ── */}
        <div className="text-center pt-10 pb-8">
          <div className="text-5xl mb-3">{lessonData.meta.icon || '📖'}</div>
          <h1
            className="font-display text-3xl md:text-4xl mb-2"
            style={{
              background: 'linear-gradient(135deg,#fbbf24,#f87171)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            {lessonData.meta.title}
          </h1>
          <p className="text-sm font-bold" style={{ color: 'var(--ws-text-muted)' }}>
            Class {classNum} &bull; {subject.charAt(0).toUpperCase() + subject.slice(1)}
          </p>
          {lessonData.meta.description && (
            <p className="text-sm mt-2 max-w-md mx-auto" style={{ color: 'var(--ws-text-muted)' }}>
              {lessonData.meta.description}
            </p>
          )}
        </div>

        {/* ── Section title ── */}
        <div className="font-display text-xl mb-1">🎮 Choose a Mode</div>
        <div className="text-xs mb-5" style={{ color: 'var(--ws-text-muted)' }}>
          Pick how you want to learn today
        </div>

        {/* ── Mode cards ── */}
        <div className="flex flex-col gap-4">
          {modeCards.map((card) => (
            <Link
              key={card.mode}
              href={`/class/${classNum}/${subject}/${lesson}/${card.mode}`}
              className="block group"
            >
              <div
                className="rounded-2xl p-px transition-all duration-200 group-hover:-translate-y-0.5"
                style={{ boxShadow: `0 4px 20px ${card.glow}`, border: '1px solid var(--ws-border)' }}
              >
                <div
                  className="rounded-2xl flex items-center gap-5 px-6 py-5"
                  style={{ background: 'var(--ws-card-inner)' }}
                >
                  {/* Icon circle */}
                  <div
                    className="flex-shrink-0 w-14 h-14 rounded-2xl flex items-center justify-center text-3xl"
                    style={{ background: card.gradient, boxShadow: `0 4px 14px ${card.glow}` }}
                  >
                    {card.icon}
                  </div>

                  {/* Text */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-display text-xl" style={{ color: 'var(--ws-text)' }}>{card.label}</span>
                      <span
                        className="text-xs font-bold px-2 py-0.5 rounded-full"
                        style={{ background: card.tagBg, color: card.tagColor }}
                      >
                        {card.tag}
                      </span>
                    </div>
                    <p className="text-xs" style={{ color: 'var(--ws-text-muted)' }}>
                      {card.description}
                    </p>
                  </div>

                  {/* Arrow */}
                  <div
                    className="flex-shrink-0 font-display text-xl transition-transform duration-200 group-hover:translate-x-1"
                    style={{ color: 'var(--ws-text-dim)' }}
                  >
                    →
                  </div>
                </div>
              </div>
            </Link>
          ))}

          {/* ── Review card (SRS) ── */}
          <ReviewCard
            classNum={classNum}
            subject={subject}
            lesson={lesson}
            lessonId={lessonData.id}
          />
        </div>

        {/* ── Back link ── */}
        <div className="mt-8 text-center">
          <Link
            href="/"
            className="text-sm font-bold transition-colors"
            style={{ color: 'var(--ws-text-dim)' }}
          >
            ← Back to all lessons
          </Link>
        </div>
      </main>
    </>
  );
}
