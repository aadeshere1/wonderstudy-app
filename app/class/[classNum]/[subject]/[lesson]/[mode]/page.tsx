import { readFileSync } from 'fs';
import { join } from 'path';
import { Metadata } from 'next';
import { gameSchema } from '@/components/seo/SchemaMarkup';
import type { LessonData } from '@/lib/engine/types';
import GameLoader from './GameLoader';

function loadLesson(classNum: string, subject: string, lesson: string): LessonData | null {
  try {
    const filePath = join(process.cwd(), 'data', 'classes', `class-${classNum}`, subject, `${lesson}.json`);
    return JSON.parse(readFileSync(filePath, 'utf-8')) as LessonData;
  } catch {
    return null;
  }
}

export async function generateStaticParams() {
  const lessons = [
    { classNum: '1', subject: 'science', lesson: 'living-nonliving' },
    { classNum: '1', subject: 'math', lesson: 'addition-subtraction' },
    { classNum: '1', subject: 'english', lesson: 'animals-vocabulary' },
    { classNum: '6', subject: 'math', lesson: 'sets-introduction' },
    { classNum: '6', subject: 'math', lesson: 'whole-numbers' },
  ];
  const modes = ['teach', 'practice', 'challenge'];

  return lessons.flatMap((lesson) =>
    modes.map((mode) => ({
      ...lesson,
      mode,
    }))
  );
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
      title: 'Play Lesson - WonderStudy',
      description: 'Interactive learning game',
    };
  }

  const modeLabel = mode.charAt(0).toUpperCase() + mode.slice(1);
  const title = `${lessonData.meta.title} - ${modeLabel} Mode - WonderStudy`;
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
