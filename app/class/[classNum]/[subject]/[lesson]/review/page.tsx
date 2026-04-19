import { readFileSync } from 'fs';
import { join } from 'path';
import type { LessonData } from '@/lib/engine/types';
import ReviewLoader from './ReviewLoader';

function loadLesson(classNum: string, subject: string, lesson: string): LessonData | null {
  try {
    const filePath = join(process.cwd(), 'data', 'classes', `class-${classNum}`, subject, `${lesson}.json`);
    return JSON.parse(readFileSync(filePath, 'utf-8')) as LessonData;
  } catch { return null; }
}

export async function generateStaticParams() {
  return [
    { classNum: '6', subject: 'math', lesson: 'sets-introduction' },
    { classNum: '6', subject: 'math', lesson: 'whole-numbers' },
    { classNum: '1', subject: 'science', lesson: 'living-nonliving' },
    { classNum: '1', subject: 'math', lesson: 'addition-subtraction' },
    { classNum: '1', subject: 'english', lesson: 'animals-vocabulary' },
  ];
}

interface PageProps {
  params: Promise<{ classNum: string; subject: string; lesson: string }>;
}

export default async function ReviewPage({ params }: PageProps) {
  const { classNum, subject, lesson } = await params;
  const lessonData = loadLesson(classNum, subject, lesson);
  return (
    <ReviewLoader
      classNum={classNum}
      subject={subject}
      lesson={lesson}
      initialLesson={lessonData}
    />
  );
}
