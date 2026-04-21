import { readFileSync } from 'fs';
import { join } from 'path';
import { Metadata } from 'next';
import { gameSchema } from '@/components/seo/SchemaMarkup';
import type { LessonData } from '@/lib/engine/types';
import GameLoader from './GameLoader';

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
  const lessons: { classNum: string; subject: string; lesson: string }[] = [];
  const classesDir = join(process.cwd(), 'data', 'classes');
  if (existsSync(classesDir)) {
    for (const classFolder of readdirSync(classesDir)) {
      const classNum = classFolder.replace('class-', '');
      const classPath = join(classesDir, classFolder);
      for (const subject of readdirSync(classPath)) {
        const subjectPath = join(classPath, subject);
        for (const file of readdirSync(subjectPath)) {
          if (file.endsWith('.json') && file !== 'index.json') {
            lessons.push({ classNum, subject, lesson: file.replace('.json', '') });
          }
        }
      }
    }
  }
  const modes = ['teach', 'practice', 'challenge'];
  return lessons.flatMap((l) => modes.map((mode) => ({ ...l, mode })));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ classNum: string; subject: string; lesson: string; mode: string }>;
}): Promise<Metadata> {
  const { classNum, subject, lesson, mode } = await params;
  const lessonData = loadLesson(classNum, subject, lesson);

  if (!lessonData) {
    return {
      title: 'Play Lesson - Sikshya',
      description: 'Interactive learning game',
    };
  }

  const modeLabel = mode.charAt(0).toUpperCase() + mode.slice(1);
  const title = `${lessonData.meta.title} - ${modeLabel} Mode - Sikshya`;
  const description = `${modeLabel} mode for "${lessonData.meta.title}" - Class ${classNum} ${subject}`;

  return {
    title,
    description,
    keywords: [
      lessonData.meta.subject,
      `class ${classNum}`,
      `${mode} mode`,
      'educational game',
      'kids learning',
    ],
    openGraph: {
      title,
      description,
      type: 'website',
    },
  };
}

interface PageProps {
  params: Promise<{
    classNum: string;
    subject: string;
    lesson: string;
    mode: string;
  }>;
}

export default async function LessonPage({ params }: PageProps) {
  const { classNum, subject, lesson, mode } = await params;
  const lessonData = loadLesson(classNum, subject, lesson);

  let schemaMarkup = null;
  if (lessonData) {
    const modeLabel = mode.charAt(0).toUpperCase() + mode.slice(1);
    schemaMarkup = gameSchema(
      `${lessonData.meta.title} - ${modeLabel} Mode`,
      `${modeLabel} mode for "${lessonData.meta.title}" - Class ${classNum} ${subject}`
    );
  }

  return (
    <>
      {schemaMarkup && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaMarkup) }}
        />
      )}
      <GameLoader
        classNum={classNum}
        subject={subject}
        lesson={lesson}
        mode={mode}
        initialLesson={lessonData}
      />
    </>
  );
}
